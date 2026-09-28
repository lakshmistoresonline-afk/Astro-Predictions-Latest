"""
Canonical Vedic Chart Builder Engine for Astrovision.
Orchestrates: Birth Input -> Time Normalization -> Skyfield Provider -> Lahiri Sidereal -> Rashi -> Nakshatra -> Pada -> Ascendant -> MC -> Whole Sign Houses.
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


def build_canonical_vedic_chart(
    birth_input: BirthInput,
    astronomy_provider: Optional[BaseAstronomyProvider] = None
) -> CanonicalVedicChart:
    """
    Builds the complete canonical Vedic chart object.
    Source separation enforced: Vedic modules never call Skyfield directly, but consume the astronomy provider.
    """
    # 1. Time Normalization (Local Civil Time -> UTC)
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

    # 4. Explicit Mean Node Models: Rahu and Ketu
    T = (astro_res.raw_ephemeris.julian_day_tt - 2451545.0) / 36525.0
    rahu_trop_lon = (125.04452 - 1934.136261 * T) % 360.0
    rahu_sid_lon = (rahu_trop_lon - ayanamsha_val) % 360.0
    ketu_sid_lon = (rahu_sid_lon + 180.0) % 360.0

    rahu_rashi = calculate_rashi(rahu_sid_lon)
    rahu_nak_pada = calculate_nakshatra_pada(rahu_sid_lon)
    ketu_rashi = calculate_rashi(ketu_sid_lon)
    ketu_nak_pada = calculate_nakshatra_pada(ketu_sid_lon)

    placements["Rahu"] = PlanetaryVedicPlacement(
        body_name="Rahu",
        geocentric_tropical_lon=round(rahu_trop_lon, 6),
        geocentric_latitude=0.0,
        distance_au=0.0,
        velocity_deg_day=-0.05295,
        retrograde=True,
        sidereal_longitude=round(rahu_sid_lon, 6),
        rashi=rahu_rashi,
        nakshatra_pada=rahu_nak_pada
    )

    placements["Ketu"] = PlanetaryVedicPlacement(
        body_name="Ketu",
        geocentric_tropical_lon=round((rahu_trop_lon + 180.0) % 360.0, 6),
        geocentric_latitude=0.0,
        distance_au=0.0,
        velocity_deg_day=-0.05295,
        retrograde=True,
        sidereal_longitude=round(ketu_sid_lon, 6),
        rashi=ketu_rashi,
        nakshatra_pada=ketu_nak_pada
    )

    # 5. Ascendant & MC Processing
    asc_sid_lon = astro_res.sidereal_state.ascendant_sidereal_deg
    mc_sid_lon = astro_res.sidereal_state.mc_sidereal_deg

    asc_rashi = calculate_rashi(asc_sid_lon)
    mc_rashi = calculate_rashi(mc_sid_lon)

    # 6. Whole Sign Houses
    whole_sign_houses = generate_whole_sign_houses(asc_rashi)

    # 7. Cryptographic SHA-256 Calculation Hash
    payload = {
        "birth_input": birth_input.model_dump(),
        "utc_datetime": time_norm.utc_datetime_iso,
        "julian_day_tt": time_norm.julian_day_tt,
        "astronomy_hash": astro_res.metadata.calculation_hash,
        "ascendant_sidereal": round(asc_sid_lon, 6),
        "moon_sidereal": round(placements["Moon"].sidereal_longitude, 6)
    }
    canonical_json = json.dumps(payload, sort_keys=True)
    chart_hash = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    # 8. Audit Metadata
    metadata = {
        "provider": astro_res.metadata.provider,
        "provider_version": astro_res.metadata.provider_version,
        "ephemeris_kernel": astro_res.metadata.ephemeris_kernel,
        "kernel_checksum": astro_res.metadata.kernel_checksum,
        "ayanamsha_mode": "Lahiri",
        "house_system": "Whole Sign",
        "node_model": "Mean Node"
    }

    return CanonicalVedicChart(
        input_data=birth_input,
        time_normalization=time_norm,
        ayanamsha_mode="Lahiri",
        ayanamsha_value_deg=round(ayanamsha_val, 6),
        ascendant=asc_rashi,
        mc=mc_rashi,
        placements=placements,
        whole_sign_houses=whole_sign_houses,
        calculation_hash=chart_hash,
        metadata=metadata
    )
