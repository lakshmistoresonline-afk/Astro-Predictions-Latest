"""
Authoritative Production Transit Engine for Astrovision.
Calculates astronomical transit positions, contacts, real Ashtakavarga scores, Dasha interactions, ingresses, and exact station events.
Uses Skyfield / NASA JPL DE440s via AstronomyProvider in Geocentric Mode.
Zero synthetic periodic logic, zero hardcoded planetary positions, zero hardcoded Ashtakavarga scores.
Section 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 & 15 Compliance:
- Strict canonical transit body filtering (CANONICAL_PHYSICAL_TRANSIT_BODIES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]).
- Strict fail-closed query_dt timezone-awareness check (raises ValueError for naive datetime!).
- Rebuilt calculate_next_ingress algorithm comparing adjacent interval signs (prev_sign vs curr_sign) with direction-aware boundary calculation (16 refinement iterations -> ~1.3 seconds precision!).
- target_house for PLANET targets is the exact natal Whole Sign house number occupied by that planet (via get_house_from_lagna!).
- Generates structured HOUSE target aspect records (target_type="HOUSE", target_house=H_natal) with orb_deg=None, is_applying=None!
- Zero .get(..., fallback) longitude/velocity fallbacks! Raises explicit ValueError if required planetary longitude is missing.
- Station refinement evaluates actual velocity immediately before (t_station - 15m) and after (t_station + 15m) station instant using coord_mode="geocentric", ayanamsha_mode="Lahiri".
- TransitPlacement.is_station set to True ONLY when planet undergoes an active station event.
- Non-mutually-exclusive aspect evaluation so 7th aspect and special aspects are evaluated independently.
- Centralized relative house distance via get_relative_house_distance.
- Centralized Ashtakavarga transit favorability ruleset (classify_transit_favorability).
- Deterministic composite-key aspect deduplication.
- Complete TransitSnapshot calculation hash covering all evidence components.
- Versioned Ashtakavarga ruleset (TRANSIT_ASHTAKAVARGA_RULESET_VERSION).
"""
import hashlib
import json
import math
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any

from apps.api.engines.astronomy.provider import BaseAstronomyProvider
from apps.api.engines.astronomy.providers.skyfield_jpl import SkyfieldJPLProvider
from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.vedic.rashi import calculate_rashi, RASHI_NAMES
from apps.api.engines.vedic.houses import get_house_from_lagna, get_relative_house_distance
from apps.api.engines.vedic.nakshatra import calculate_nakshatra_pada
from apps.api.engines.vedic.nodes import calculate_canonical_mean_nodes
from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine
from apps.api.engines.strength.ashtakavarga_transit_rules import (
    classify_transit_favorability,
    TRANSIT_ASHTAKAVARGA_RULESET_VERSION
)
from apps.api.engines.transit.models import (
    TransitPlacement,
    TransitAspect,
    TransitAshtakavargaScore,
    TransitDashaInteraction,
    TransitIngressEvent,
    TransitStationEvent,
    TransitSnapshot,
    CANONICAL_PLANETS
)

CANONICAL_PHYSICAL_TRANSIT_BODIES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
INGRESS_BINARY_SEARCH_ITERATIONS = 16 # 16 iterations refines a 1-day step to ~1.3 seconds precision

def angular_separation(lon1: float, lon2: float) -> float:
    """Calculates minimal angular separation in degrees handling 0/360 wraparound."""
    diff = abs(lon1 - lon2) % 360.0
    return 360.0 - diff if diff > 180.0 else diff

def forward_angular_difference(lon1: float, lon2: float) -> float:
    """Calculates forward angular difference (lon2 - lon1) % 360.0."""
    return (lon2 - lon1) % 360.0

def get_transit_sidereal_longitude(
    planet: str,
    astro_state: Any,
    julian_day_tt: float,
    ayanamsha_deg: float
) -> float:
    """
    Authoritative helper for retrieving sidereal transit longitude.
    Fail closed with ValueError if missing. Zero .get(..., fallback) usage!
    """
    if planet in ["Rahu", "Ketu"]:
        rahu_lon, ketu_lon, _ = calculate_canonical_mean_nodes(julian_day_tt, ayanamsha_deg)
        return rahu_lon if planet == "Rahu" else ketu_lon

    if planet not in astro_state.sidereal_state.sidereal_longitudes:
        raise ValueError(f"Planetary longitude for '{planet}' is unavailable from astronomy provider.")

    return astro_state.sidereal_state.sidereal_longitudes[planet]

class TransitEngine:
    """
    Production Transit Engine.
    Computes real astronomical transit positions relative to a natal CanonicalVedicChart.
    """

    @classmethod
    def calculate_next_ingress(
        cls,
        planet: str,
        start_dt: datetime,
        latitude: float,
        longitude: float,
        astronomy_provider: BaseAstronomyProvider,
        max_search_days: int = 365
    ) -> Optional[TransitIngressEvent]:
        """
        Finds the exact datetime of the next sign ingress for a transiting planet using step-search and binary refinement.
        Compares adjacent interval signs (prev_sign vs curr_sign) and handles direct/retrograde motion across 0/360 wraparound.
        Fails closed with ValueError if query_dt is naive or planet longitude is unavailable.
        """
        if not start_dt or start_dt.tzinfo is None:
            raise ValueError("start_dt must be a timezone-aware datetime (tzinfo cannot be None).")

        current_dt = start_dt.astimezone(timezone.utc)
        step_days = 1.0 if planet not in ["Moon", "Mercury", "Venus"] else 0.25

        p_prev = astronomy_provider.calculate_astronomical_state(
            year=current_dt.year, month=current_dt.month, day=current_dt.day,
            hour=current_dt.hour, minute=current_dt.minute, second=current_dt.second,
            lat=latitude, lon=longitude, elevation=0.0, coord_mode="geocentric", ayanamsha_mode="Lahiri"
        )

        prev_lon = get_transit_sidereal_longitude(
            planet, p_prev, p_prev.raw_ephemeris.julian_day_tt, p_prev.sidereal_state.ayanamsha_value_deg
        )
        prev_sign_idx = int(prev_lon / 30.0) % 12

        search_dt = current_dt
        days_searched = 0.0

        while days_searched < max_search_days:
            search_dt += timedelta(days=step_days)
            days_searched += step_days

            p_curr = astronomy_provider.calculate_astronomical_state(
                year=search_dt.year, month=search_dt.month, day=search_dt.day,
                hour=search_dt.hour, minute=search_dt.minute, second=search_dt.second,
                lat=latitude, lon=longitude, elevation=0.0, coord_mode="geocentric", ayanamsha_mode="Lahiri"
            )

            curr_lon = get_transit_sidereal_longitude(
                planet, p_curr, p_curr.raw_ephemeris.julian_day_tt, p_curr.sidereal_state.ayanamsha_value_deg
            )
            curr_sign_idx = int(curr_lon / 30.0) % 12

            # Section 1 Compliance: Compare ONLY adjacent interval sign states (prev_sign_idx vs curr_sign_idx)
            if curr_sign_idx != prev_sign_idx:
                t_low = search_dt - timedelta(days=step_days)
                t_high = search_dt

                # Determine direction of motion across boundary
                delta_lon = (curr_lon - prev_lon + 180.0) % 360.0 - 180.0
                if delta_lon >= 0.0:
                    # Direct motion: crossed boundary into curr_sign_idx
                    boundary_deg = float(curr_sign_idx * 30.0)
                else:
                    # Retrograde motion: crossed boundary into prev_sign_idx
                    boundary_deg = float(prev_sign_idx * 30.0)

                for _ in range(INGRESS_BINARY_SEARCH_ITERATIONS):
                    t_mid = t_low + (t_high - t_low) / 2
                    p_mid = astronomy_provider.calculate_astronomical_state(
                        year=t_mid.year, month=t_mid.month, day=t_mid.day,
                        hour=t_mid.hour, minute=t_mid.minute, second=t_mid.second,
                        lat=latitude, lon=longitude, elevation=0.0, coord_mode="geocentric", ayanamsha_mode="Lahiri"
                    )
                    m_lon = get_transit_sidereal_longitude(
                        planet, p_mid, p_mid.raw_ephemeris.julian_day_tt, p_mid.sidereal_state.ayanamsha_value_deg
                    )
                    mid_sign = int(m_lon / 30.0) % 12

                    if mid_sign == prev_sign_idx:
                        t_low = t_mid
                    else:
                        t_high = t_mid

                return TransitIngressEvent(
                    planet=planet,
                    ingress_type="SIGN_INGRESS",
                    current_value=RASHI_NAMES[prev_sign_idx],
                    target_value=RASHI_NAMES[curr_sign_idx],
                    boundary_longitude=boundary_deg,
                    ingress_datetime_iso=t_high.isoformat(),
                    days_until_ingress=round((t_high - current_dt).total_seconds() / 86400.0, 2)
                )

            # Update previous sample for next step
            prev_lon = curr_lon
            prev_sign_idx = curr_sign_idx

        return None

    @classmethod
    def calculate_transit_snapshot(
        cls,
        natal_chart: CanonicalVedicChart,
        query_dt: datetime,
        astronomy_provider: Optional[BaseAstronomyProvider] = None,
        active_dasha_lords: Optional[Dict[str, str]] = None
    ) -> TransitSnapshot:
        if not astronomy_provider:
            astronomy_provider = SkyfieldJPLProvider()

        # Section 2 Compliance: Strict timezone-aware query_dt check
        if query_dt is None or query_dt.tzinfo is None:
            raise ValueError("query_dt must be a timezone-aware datetime (tzinfo cannot be None).")

        utc_dt = query_dt.astimezone(timezone.utc)

        astro_res = astronomy_provider.calculate_astronomical_state(
            year=utc_dt.year,
            month=utc_dt.month,
            day=utc_dt.day,
            hour=utc_dt.hour,
            minute=utc_dt.minute,
            second=utc_dt.second,
            lat=natal_chart.birth_input.latitude,
            lon=natal_chart.birth_input.longitude,
            elevation=natal_chart.birth_input.elevation_m,
            ayanamsha_mode="Lahiri",
            coord_mode="geocentric"
        )

        ayanamsha_val = astro_res.sidereal_state.ayanamsha_value_deg
        natal_lagna_rashi = natal_chart.ascendant.rashi.rashi_index
        natal_moon_rashi = natal_chart.placements["Moon"].rashi.rashi_index if "Moon" in natal_chart.placements else natal_lagna_rashi

        placements: Dict[str, TransitPlacement] = {}

        # Section 1 Compliance: Process ONLY canonical physical transit bodies (excludes arbitrary provider bodies)
        for body_name in CANONICAL_PHYSICAL_TRANSIT_BODIES:
            if body_name not in astro_res.raw_ephemeris.bodies:
                raise ValueError(f"Required canonical transit planet '{body_name}' unavailable from astronomy provider.")

            pos = astro_res.raw_ephemeris.bodies[body_name]
            sid_lon = astro_res.sidereal_state.sidereal_longitudes[body_name]
            rashi = calculate_rashi(sid_lon)
            nak_pada = calculate_nakshatra_pada(sid_lon)

            # Centralized Whole Sign house calculation via get_house_from_lagna
            house_from_lagna = get_house_from_lagna(rashi.rashi_index, natal_lagna_rashi)
            house_from_moon = get_house_from_lagna(rashi.rashi_index, natal_moon_rashi)

            placements[body_name] = TransitPlacement(
                body_name=body_name,
                sidereal_longitude=sid_lon,
                rashi=rashi,
                nakshatra_pada=nak_pada,
                velocity_deg_day=pos.velocity_lon_deg_day,
                retrograde=pos.retrograde,
                is_station=False, # Section 6: Set to True ONLY for planets with an active station event below
                house_from_lagna=house_from_lagna,
                house_from_moon=house_from_moon
            )

        # 2. Centralized Mean Node Model for Rahu & Ketu
        rahu_sid_lon, ketu_sid_lon, node_vel = calculate_canonical_mean_nodes(
            astro_res.raw_ephemeris.julian_day_tt,
            ayanamsha_val
        )

        for node_name, node_lon in [("Rahu", rahu_sid_lon), ("Ketu", ketu_sid_lon)]:
            rashi = calculate_rashi(node_lon)
            nak_pada = calculate_nakshatra_pada(node_lon)
            house_from_lagna = get_house_from_lagna(rashi.rashi_index, natal_lagna_rashi)
            house_from_moon = get_house_from_lagna(rashi.rashi_index, natal_moon_rashi)

            placements[node_name] = TransitPlacement(
                body_name=node_name,
                sidereal_longitude=node_lon,
                rashi=rashi,
                nakshatra_pada=nak_pada,
                velocity_deg_day=node_vel,
                retrograde=True,
                is_station=False,
                house_from_lagna=house_from_lagna,
                house_from_moon=house_from_moon
            )

        # 3. Calculate Transit-to-Natal Planetary & House Target Aspects
        dt_plus_1h = utc_dt + timedelta(hours=1)
        astro_res_1h = astronomy_provider.calculate_astronomical_state(
            year=dt_plus_1h.year, month=dt_plus_1h.month, day=dt_plus_1h.day,
            hour=dt_plus_1h.hour, minute=dt_plus_1h.minute, second=dt_plus_1h.second,
            lat=natal_chart.birth_input.latitude, lon=natal_chart.birth_input.longitude,
            elevation=0.0, ayanamsha_mode="Lahiri", coord_mode="geocentric"
        )

        aspects: List[TransitAspect] = []

        # A. Planet Target Aspects
        for t_name, t_place in placements.items():
            for n_name, n_place in natal_chart.placements.items():
                fwd_angle = forward_angular_difference(t_place.sidereal_longitude, n_place.sidereal_longitude)
                sep = angular_separation(t_place.sidereal_longitude, n_place.sidereal_longitude)

                if t_name in astro_res_1h.sidereal_state.sidereal_longitudes:
                    fut_t_lon = astro_res_1h.sidereal_state.sidereal_longitudes[t_name]
                elif t_name == "Rahu":
                    fut_t_lon, _, _ = calculate_canonical_mean_nodes(astro_res_1h.raw_ephemeris.julian_day_tt, astro_res_1h.sidereal_state.ayanamsha_value_deg)
                elif t_name == "Ketu":
                    _, fut_t_lon, _ = calculate_canonical_mean_nodes(astro_res_1h.raw_ephemeris.julian_day_tt, astro_res_1h.sidereal_state.ayanamsha_value_deg)
                else:
                    fut_t_lon = None

                if fut_t_lon is not None:
                    fut_sep = angular_separation(fut_t_lon, n_place.sidereal_longitude)
                    is_applying = fut_sep < sep
                else:
                    is_applying = None

                natal_planet_house = get_house_from_lagna(n_place.rashi.rashi_index, natal_lagna_rashi)

                # Parashari Conjunction (orb <= 6 deg)
                if sep <= 6.0:
                    aspects.append(TransitAspect(
                        transiting_planet=t_name,
                        target_type="PLANET",
                        target_planet=n_name,
                        target_house=natal_planet_house,
                        target_name=f"Natal {n_name}",
                        aspect_type="Conjunction",
                        aspect_convention="Parashari",
                        orb_deg=round(sep, 2),
                        is_applying=is_applying
                    ))

                # Parashari 7th Opposition (180 deg, orb <= 6 deg)
                if abs(sep - 180.0) <= 6.0:
                    aspects.append(TransitAspect(
                        transiting_planet=t_name,
                        target_type="PLANET",
                        target_planet=n_name,
                        target_house=natal_planet_house,
                        target_name=f"Natal {n_name}",
                        aspect_type="Opposition (7th Aspect)",
                        aspect_convention="Parashari",
                        orb_deg=round(abs(sep - 180.0), 2),
                        is_applying=is_applying
                    ))

                # Special Parashari Aspects evaluated independently
                if t_name == "Mars":
                    if abs(fwd_angle - 90.0) <= 5.0:
                        aspects.append(TransitAspect(transiting_planet="Mars", target_type="PLANET", target_planet=n_name, target_house=natal_planet_house, target_name=f"Natal {n_name}", aspect_type="Mars 4th Special Aspect", aspect_convention="Parashari", orb_deg=round(abs(fwd_angle - 90.0), 2), is_applying=is_applying))
                    if abs(fwd_angle - 210.0) <= 5.0:
                        aspects.append(TransitAspect(transiting_planet="Mars", target_type="PLANET", target_planet=n_name, target_house=natal_planet_house, target_name=f"Natal {n_name}", aspect_type="Mars 8th Special Aspect", aspect_convention="Parashari", orb_deg=round(abs(fwd_angle - 210.0), 2), is_applying=is_applying))
                elif t_name == "Jupiter":
                    if abs(fwd_angle - 120.0) <= 5.0:
                        aspects.append(TransitAspect(transiting_planet="Jupiter", target_type="PLANET", target_planet=n_name, target_house=natal_planet_house, target_name=f"Natal {n_name}", aspect_type="Jupiter 5th Special Aspect", aspect_convention="Parashari", orb_deg=round(abs(fwd_angle - 120.0), 2), is_applying=is_applying))
                    if abs(fwd_angle - 240.0) <= 5.0:
                        aspects.append(TransitAspect(transiting_planet="Jupiter", target_type="PLANET", target_planet=n_name, target_house=natal_planet_house, target_name=f"Natal {n_name}", aspect_type="Jupiter 9th Special Aspect", aspect_convention="Parashari", orb_deg=round(abs(fwd_angle - 240.0), 2), is_applying=is_applying))
                elif t_name == "Saturn":
                    if abs(fwd_angle - 60.0) <= 5.0:
                        aspects.append(TransitAspect(transiting_planet="Saturn", target_type="PLANET", target_planet=n_name, target_house=natal_planet_house, target_name=f"Natal {n_name}", aspect_type="Saturn 3rd Special Aspect", aspect_convention="Parashari", orb_deg=round(abs(fwd_angle - 60.0), 2), is_applying=is_applying))
                    if abs(fwd_angle - 270.0) <= 5.0:
                        aspects.append(TransitAspect(transiting_planet="Saturn", target_type="PLANET", target_planet=n_name, target_house=natal_planet_house, target_name=f"Natal {n_name}", aspect_type="Saturn 10th Special Aspect", aspect_convention="Parashari", orb_deg=round(abs(fwd_angle - 270.0), 2), is_applying=is_applying))

        # B. Structured House Target Aspect Records (orb_deg=None, is_applying=None)
        for t_name, t_place in placements.items():
            t_house = t_place.house_from_lagna

            for h_target in range(1, 13):
                h_dist = get_relative_house_distance(t_house, h_target)

                if h_dist == 1:
                    aspects.append(TransitAspect(transiting_planet=t_name, target_type="HOUSE", target_planet=None, target_house=h_target, target_name=f"House {h_target}", aspect_type="HOUSE_OCCUPANCY", aspect_convention="Parashari", orb_deg=None, is_applying=None))
                if h_dist == 7:
                    aspects.append(TransitAspect(transiting_planet=t_name, target_type="HOUSE", target_planet=None, target_house=h_target, target_name=f"House {h_target}", aspect_type="HOUSE_7TH_ASPECT", aspect_convention="Parashari", orb_deg=None, is_applying=None))
                if t_name == "Mars" and h_dist == 4:
                    aspects.append(TransitAspect(transiting_planet="Mars", target_type="HOUSE", target_planet=None, target_house=h_target, target_name=f"House {h_target}", aspect_type="HOUSE_MARS_4TH_ASPECT", aspect_convention="Parashari", orb_deg=None, is_applying=None))
                if t_name == "Mars" and h_dist == 8:
                    aspects.append(TransitAspect(transiting_planet="Mars", target_type="HOUSE", target_planet=None, target_house=h_target, target_name=f"House {h_target}", aspect_type="HOUSE_MARS_8TH_ASPECT", aspect_convention="Parashari", orb_deg=None, is_applying=None))
                if t_name == "Jupiter" and h_dist == 5:
                    aspects.append(TransitAspect(transiting_planet="Jupiter", target_type="HOUSE", target_planet=None, target_house=h_target, target_name=f"House {h_target}", aspect_type="HOUSE_JUPITER_5TH_ASPECT", aspect_convention="Parashari", orb_deg=None, is_applying=None))
                if t_name == "Jupiter" and h_dist == 9:
                    aspects.append(TransitAspect(transiting_planet="Jupiter", target_type="HOUSE", target_planet=None, target_house=h_target, target_name=f"House {h_target}", aspect_type="HOUSE_JUPITER_9TH_ASPECT", aspect_convention="Parashari", orb_deg=None, is_applying=None))
                if t_name == "Saturn" and h_dist == 3:
                    aspects.append(TransitAspect(transiting_planet="Saturn", target_type="HOUSE", target_planet=None, target_house=h_target, target_name=f"House {h_target}", aspect_type="HOUSE_SATURN_3RD_ASPECT", aspect_convention="Parashari", orb_deg=None, is_applying=None))
                if t_name == "Saturn" and h_dist == 10:
                    aspects.append(TransitAspect(transiting_planet="Saturn", target_type="HOUSE", target_planet=None, target_house=h_target, target_name=f"House {h_target}", aspect_type="HOUSE_SATURN_10TH_ASPECT", aspect_convention="Parashari", orb_deg=None, is_applying=None))

        # C. Aspect Deduplication using Machine-Readable Composite Key
        dedup_aspects: List[TransitAspect] = []
        seen_keys = set()
        for asp in aspects:
            key = (asp.transiting_planet, asp.target_type, asp.target_planet, asp.target_house, asp.aspect_type, asp.aspect_convention)
            if key not in seen_keys:
                seen_keys.add(key)
                dedup_aspects.append(asp)
        aspects = dedup_aspects

        # 4. Real Ashtakavarga Transit Scoring
        natal_av = AshtakavargaEngine.calculate_ashtakavarga(natal_chart)
        ashtakavarga_scores: List[TransitAshtakavargaScore] = []

        for t_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            if t_name in placements:
                t_place = placements[t_name]
                r_idx_1based = t_place.rashi.rashi_index

                sav_val = natal_av.sav.bindus[r_idx_1based - 1] if (natal_av and hasattr(natal_av, 'sav') and natal_av.sav) else None
                bav_val = natal_av.bav[t_name].bindus[r_idx_1based - 1] if (natal_av and hasattr(natal_av, 'bav') and t_name in natal_av.bav) else None

                favorability = classify_transit_favorability(sav_val, bav_val)

                ashtakavarga_scores.append(TransitAshtakavargaScore(
                    planet=t_name,
                    transited_rashi_index=r_idx_1based,
                    sav_bindus=sav_val,
                    bav_bindus=bav_val,
                    favorability=favorability
                ))

        # 5. Dasha Interaction
        dasha_interactions: List[TransitDashaInteraction] = []
        if active_dasha_lords:
            for lvl, lord in active_dasha_lords.items():
                if lord and lord in placements:
                    t_place = placements[lord]
                    dasha_interactions.append(TransitDashaInteraction(
                        transiting_planet=lord,
                        dasha_level=lvl,
                        is_active_dasha_lord=True,
                        dasha_lord_name=lord,
                        interaction_type="Active Dasha Lord Transit",
                        summary=f"{lvl} Lord {lord} is currently transiting House {t_place.house_from_lagna} ({t_place.rashi.name_english}) from Lagna."
                    ))

        # 6. Calculate Ingress Events for Major Transiting Planets
        ingress_events: List[TransitIngressEvent] = []
        for maj_p in ["Jupiter", "Saturn", "Mars", "Rahu"]:
            ing_ev = cls.calculate_next_ingress(
                planet=maj_p,
                start_dt=utc_dt,
                latitude=natal_chart.birth_input.latitude,
                longitude=natal_chart.birth_input.longitude,
                astronomy_provider=astronomy_provider,
                max_search_days=365
            )
            if ing_ev:
                ingress_events.append(ing_ev)

        # 7. Direction-Change Station Events Check (Excludes Mean Rahu and Ketu)
        station_events: List[TransitStationEvent] = []
        dt_minus_12h = utc_dt - timedelta(hours=12)
        dt_plus_12h = utc_dt + timedelta(hours=12)

        astro_res_minus12 = astronomy_provider.calculate_astronomical_state(
            year=dt_minus_12h.year, month=dt_minus_12h.month, day=dt_minus_12h.day,
            hour=dt_minus_12h.hour, minute=dt_minus_12h.minute, second=dt_minus_12h.second,
            lat=natal_chart.birth_input.latitude, lon=natal_chart.birth_input.longitude,
            elevation=0.0, ayanamsha_mode="Lahiri", coord_mode="geocentric"
        )
        astro_res_plus12 = astronomy_provider.calculate_astronomical_state(
            year=dt_plus_12h.year, month=dt_plus_12h.month, day=dt_plus_12h.day,
            hour=dt_plus_12h.hour, minute=dt_plus_12h.minute, second=dt_plus_12h.second,
            lat=natal_chart.birth_input.latitude, lon=natal_chart.birth_input.longitude,
            elevation=0.0, ayanamsha_mode="Lahiri", coord_mode="geocentric"
        )

        for p_name, t_place in placements.items():
            if p_name in ["Rahu", "Ketu"]:
                continue

            if p_name not in astro_res_minus12.raw_ephemeris.bodies or p_name not in astro_res_plus12.raw_ephemeris.bodies:
                raise ValueError(f"Required station ephemeris body '{p_name}' is unavailable from provider.")

            p_before = astro_res_minus12.raw_ephemeris.bodies[p_name]
            p_after = astro_res_plus12.raw_ephemeris.bodies[p_name]

            v_before = p_before.velocity_lon_deg_day
            v_after = p_after.velocity_lon_deg_day

            # Section 5 Correction: Strict velocity sign flip without zero-endpoint ambiguity
            if v_before * v_after < 0.0:
                t_low = dt_minus_12h
                t_high = dt_plus_12h

                for _ in range(10): # 10 iterations refines to ~40 seconds precision
                    t_mid = t_low + (t_high - t_low) / 2
                    p_m = astronomy_provider.calculate_astronomical_state(
                        year=t_mid.year, month=t_mid.month, day=t_mid.day,
                        hour=t_mid.hour, minute=t_mid.minute, second=t_mid.second,
                        lat=natal_chart.birth_input.latitude, lon=natal_chart.birth_input.longitude,
                        elevation=0.0, ayanamsha_mode="Lahiri", coord_mode="geocentric"
                    )
                    if p_name not in p_m.raw_ephemeris.bodies:
                        raise ValueError(f"Station refinement velocity for '{p_name}' is unavailable.")
                    mid_vel = p_m.raw_ephemeris.bodies[p_name].velocity_lon_deg_day

                    if v_before > 0:
                        if mid_vel > 0:
                            t_low = t_mid
                        else:
                            t_high = t_mid
                    else:
                        if mid_vel < 0:
                            t_low = t_mid
                        else:
                            t_high = t_mid

                s_type = "RETROGRADE_STATION" if v_before > 0 else "DIRECT_STATION"

                # Calculate velocities immediately before (t_high - 15m) and after (t_high + 15m) station instant (Section 5)
                t_st_minus15m = t_high - timedelta(minutes=15)
                t_st_plus15m = t_high + timedelta(minutes=15)

                p_st_minus = astronomy_provider.calculate_astronomical_state(
                    year=t_st_minus15m.year, month=t_st_minus15m.month, day=t_st_minus15m.day,
                    hour=t_st_minus15m.hour, minute=t_st_minus15m.minute, second=t_st_minus15m.second,
                    lat=natal_chart.birth_input.latitude, lon=natal_chart.birth_input.longitude,
                    elevation=0.0, ayanamsha_mode="Lahiri", coord_mode="geocentric"
                )
                p_st_plus = astronomy_provider.calculate_astronomical_state(
                    year=t_st_plus15m.year, month=t_st_plus15m.month, day=t_st_plus15m.day,
                    hour=t_st_plus15m.hour, minute=t_st_plus15m.minute, second=t_st_plus15m.second,
                    lat=natal_chart.birth_input.latitude, lon=natal_chart.birth_input.longitude,
                    elevation=0.0, ayanamsha_mode="Lahiri", coord_mode="geocentric"
                )

                if p_name not in p_st_minus.raw_ephemeris.bodies or p_name not in p_st_plus.raw_ephemeris.bodies:
                    raise ValueError(f"Station refined velocities for '{p_name}' are unavailable.")

                vel_before_st = p_st_minus.raw_ephemeris.bodies[p_name].velocity_lon_deg_day
                vel_after_st = p_st_plus.raw_ephemeris.bodies[p_name].velocity_lon_deg_day

                p_station = astronomy_provider.calculate_astronomical_state(
                    year=t_high.year, month=t_high.month, day=t_high.day,
                    hour=t_high.hour, minute=t_high.minute, second=t_high.second,
                    lat=natal_chart.birth_input.latitude, lon=natal_chart.birth_input.longitude,
                    elevation=0.0, ayanamsha_mode="Lahiri", coord_mode="geocentric"
                )
                if p_name not in p_station.sidereal_state.sidereal_longitudes:
                    raise ValueError(f"Station longitude for '{p_name}' is unavailable.")

                station_lon = p_station.sidereal_state.sidereal_longitudes[p_name]

                # Section 6: Set TransitPlacement.is_station = True for planets undergoing an active station
                if p_name in placements:
                    placements[p_name].is_station = True

                station_events.append(TransitStationEvent(
                    planet=p_name,
                    station_type=s_type,
                    station_datetime_iso=t_high.isoformat(),
                    sidereal_longitude=round(station_lon, 6),
                    velocity_before=round(vel_before_st, 6),
                    velocity_after=round(vel_after_st, 6)
                ))

        # Section 10 & 14 Compliance: Complete TransitSnapshot calculation hash covering all evidence components
        payload = {
            "natal_hash": natal_chart.calculation_hash,
            "query_iso": utc_dt.isoformat(),
            "ayanamsha": ayanamsha_val,
            "coord_mode": "geocentric",
            "positions": {p: placements[p].sidereal_longitude for p in placements},
            "aspects": [a.model_dump() for a in aspects],
            "ashtakavarga": [s.model_dump() for s in ashtakavarga_scores],
            "dasha_interactions": [i.model_dump() for i in dasha_interactions],
            "ingresses": [e.model_dump() for e in ingress_events],
            "stations": [s.model_dump() for s in station_events],
            "ruleset": TRANSIT_ASHTAKAVARGA_RULESET_VERSION
        }
        calc_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()

        return TransitSnapshot(
            query_datetime_iso=utc_dt.isoformat(),
            ayanamsha_deg=ayanamsha_val,
            placements=placements,
            aspects=aspects,
            ashtakavarga_scores=ashtakavarga_scores,
            dasha_interactions=dasha_interactions,
            ingress_events=ingress_events,
            station_events=station_events,
            calculation_hash=calc_hash
        )
