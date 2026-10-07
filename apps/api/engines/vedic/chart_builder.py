"""
Canonical Vedic Chart Builder Engine for Astrovision.
Orchestrates: Birth Input -> Time Normalization -> Skyfield Provider -> Lahiri Sidereal -> Rashi -> Nakshatra -> Pada -> Ascendant -> MC -> Whole Sign Houses.
Section 1, 2 & 3 Compliance:
- Perfectly matches CanonicalVedicChart schema contract (input_data, time_normalization, whole_sign_houses, metadata).
- Sidereal Time (GMST/LMST) calculated using Universal Time (julian_day_utc) for Earth rotation accuracy!
"""
import math
import hashlib
import json
from datetime import datetime
from typing import Dict, Optional

from apps.api.engines.astronomy.provider import BaseAstronomyProvider
from apps.api.engines.astronomy.providers.skyfield_jpl import SkyfieldJPLProvider
from apps.api.engines.vedic.models import (
    BirthInput,
    TimeNormalization,
    RashiPosition,
    NakshatraPada,
    PlanetaryVedicPlacement,
    WholeSignHouse,
    CanonicalVedicChart
)
from apps.api.engines.vedic.time_normalization import normalize_birth_time
from apps.api.engines.vedic.rashi import calculate_rashi
from apps.api.engines.vedic.nakshatra import calculate_nakshatra_pada
from apps.api.engines.vedic.houses import generate_whole_sign_houses
from apps.api.engines.vedic.nodes import calculate_canonical_mean_nodes


def build_canonical_vedic_chart(
    birth_input: BirthInput,
    astronomy_provider: Optional[BaseAstronomyProvider] = None
) -> CanonicalVedicChart:
    """
    Builds the complete canonical Vedic chart object.
    Source separation enforced: Vedic modules never call Skyfield directly, but consume the astronomy provider.
    """
    # 1. Time Normalization (Local Civil Time -> UTC & TT)
    time_norm = normalize_birth_time(birth_input)
    utc_dt = datetime.fromisoformat(time_norm.utc_datetime_iso)

    # 2. Astronomy Provider Execution (passed UTC datetime)
    if not astronomy_provider:
        astronomy_provider = SkyfieldJPLProvider()

    astro_res = astronomy_provider.calculate_astronomical_state(
        year=utc_dt.year,
        month=utc_dt.month,
        day=utc_dt.day,
        hour=utc_dt.hour,
        minute=utc_dt.minute,
        second=utc_dt.second,
        lat=birth_input.latitude,
        lon=birth_input.longitude,
        elevation=birth_input.elevation_m,
        ayanamsha_mode="Lahiri"
    )

    ayanamsha_val = astro_res.sidereal_state.ayanamsha_value_deg
    placements: Dict[str, PlanetaryVedicPlacement] = {}

    # 3. Process Celestial Bodies
    for body_name, pos in astro_res.raw_ephemeris.bodies.items():
        sid_lon = astro_res.sidereal_state.sidereal_longitudes[body_name]
        rashi = calculate_rashi(sid_lon)
        nak_pada = calculate_nakshatra_pada(sid_lon)

        placements[body_name] = PlanetaryVedicPlacement(
            body_name=body_name,
            geocentric_tropical_lon=pos.geocentric_longitude,
            geocentric_latitude=pos.geocentric_latitude,
            distance_au=pos.distance_au,
            velocity_deg_day=pos.velocity_lon_deg_day,
            retrograde=pos.retrograde,
            sidereal_longitude=sid_lon,
            rashi=rashi,
            nakshatra_pada=nak_pada
        )

    # 4. Explicit Centralized Mean Nodes: Rahu and Ketu
    rahu_sid_lon, ketu_sid_lon, node_vel = calculate_canonical_mean_nodes(
        astro_res.raw_ephemeris.julian_day_tt,
        ayanamsha_val
    )

    rahu_rashi = calculate_rashi(rahu_sid_lon)
    rahu_nak_pada = calculate_nakshatra_pada(rahu_sid_lon)
    ketu_rashi = calculate_rashi(ketu_sid_lon)
    ketu_nak_pada = calculate_nakshatra_pada(ketu_sid_lon)

    # Reconstruct Rahu tropical longitude for complete record
    rahu_trop_lon = (rahu_sid_lon + ayanamsha_val) % 360.0

    placements["Rahu"] = PlanetaryVedicPlacement(
        body_name="Rahu",
        geocentric_tropical_lon=round(rahu_trop_lon, 6),
        geocentric_latitude=0.0,
        distance_au=0.0,
        velocity_deg_day=node_vel,
        retrograde=True,
        sidereal_longitude=rahu_sid_lon,
        rashi=rahu_rashi,
        nakshatra_pada=rahu_nak_pada
    )

    placements["Ketu"] = PlanetaryVedicPlacement(
        body_name="Ketu",
        geocentric_tropical_lon=round((rahu_trop_lon + 180.0) % 360.0, 6),
        geocentric_latitude=0.0,
        distance_au=0.0,
        velocity_deg_day=node_vel,
        retrograde=True,
        sidereal_longitude=ketu_sid_lon,
        rashi=ketu_rashi,
        nakshatra_pada=ketu_nak_pada
    )

    # 5. Ascendant (Lagna) and Midheaven (MC) Calculation
    sin_eps = 0.397777156 # sin(obliquity)
    cos_eps = 0.917482062 # cos(obliquity)

    # Sidereal Time (GMST/LMST) calculation using Universal Time (julian_day_utc)
    jd_ut = time_norm.julian_day_utc
    D = jd_ut - 2451545.0
    GMST_deg = (280.46061837 + 360.98564736629 * D) % 360.0
    LMST_deg = (GMST_deg + birth_input.longitude) % 360.0

    rad_lmst = math.radians(LMST_deg)
    rad_lat = math.radians(birth_input.latitude)

    # Tropical Ascendant
    num = math.cos(rad_lmst)
    den = - (math.sin(rad_lat) * math.tan(0.4090926) + math.cos(rad_lat) * math.sin(rad_lmst))
    asc_trop_rad = math.atan2(num, den)
    asc_trop_deg = math.degrees(asc_trop_rad) % 360.0

    asc_sid_deg = (asc_trop_deg - ayanamsha_val) % 360.0
    asc_rashi = calculate_rashi(asc_sid_deg)

    # Tropical Midheaven (MC)
    mc_trop_rad = math.atan2(math.sin(rad_lmst), math.cos(rad_lmst) * cos_eps)
    mc_trop_deg = math.degrees(mc_trop_rad) % 360.0
    mc_sid_deg = (mc_trop_deg - ayanamsha_val) % 360.0
    mc_rashi = calculate_rashi(mc_sid_deg)

    # 6. Whole Sign Houses
    whole_houses = generate_whole_sign_houses(asc_rashi, placements)

    payload = {
        "birth_input": birth_input.model_dump(),
        "julian_day_utc": time_norm.julian_day_utc,
        "julian_day_tt": astro_res.raw_ephemeris.julian_day_tt,
        "ascendant_sidereal_longitude": round(asc_sid_deg, 6),
        "ayanamsha": round(ayanamsha_val, 6)
    }
    calc_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    return CanonicalVedicChart(
        input_data=birth_input,
        time_normalization=time_norm,
        ayanamsha_mode="Lahiri",
        ayanamsha_value_deg=round(ayanamsha_val, 6),
        ascendant=asc_rashi,
        mc=mc_rashi,
        placements=placements,
        whole_sign_houses=whole_houses,
        calculation_hash=calc_hash,
        metadata={
            "engine_version": "2026.1_CANONICAL_CHARTS_V1",
            "ephemeris_kernel": astro_res.metadata.ephemeris_kernel,
            "ephemeris_checksum": astro_res.metadata.kernel_checksum
        }
    )
