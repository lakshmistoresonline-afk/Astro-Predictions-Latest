import copy
from typing import Dict, Any
from apps.api.engines.vedic.models import CanonicalVedicChart, PlanetaryVedicPlacement, RashiPosition, NakshatraPada, BirthInput, TimeNormalization
from apps.api.engines.vedic.rashi import ZODIAC_SIGNS

def get_base_chart() -> CanonicalVedicChart:
    """Creates a dummy valid canonical chart that can be mutated for testing. Bypasses Skyfield."""
    inp = BirthInput(name="Synthetic", year=2000, month=1, day=1, hour=12, minute=0, timezone_str="UTC", latitude=0.0, longitude=0.0)
    tn = TimeNormalization(local_datetime_iso="2000-01-01T12:00:00+00:00", timezone_identifier="UTC", utc_datetime_iso="2000-01-01T12:00:00+00:00", utc_offset_hours=0, julian_day_utc=2451545.0, julian_day_tt=2451545.0, time_scale="UTC / TT")

    asc = RashiPosition(absolute_longitude=0.0, sign="Aries", sign_index=1, degree=0, minute=0, second=0.0)
    mc = RashiPosition(absolute_longitude=90.0, sign="Cancer", sign_index=4, degree=0, minute=0, second=0.0)

    placements = {}
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        placements[p] = PlanetaryVedicPlacement(
            body_name=p, geocentric_tropical_lon=0.0, geocentric_latitude=0.0, distance_au=1.0,
            velocity_deg_day=1.0, retrograde=False, sidereal_longitude=0.0,
            rashi=asc, nakshatra_pada=NakshatraPada(nakshatra="Ashwini", nakshatra_index=1, absolute_start_deg=0.0, absolute_end_deg=13.33, degree_within_nakshatra=0.0, pada=1)
        )

    chart = CanonicalVedicChart(
        input_data=inp, time_normalization=tn, ayanamsha_mode="Lahiri", ayanamsha_value_deg=23.85,
        ascendant=asc, mc=mc, placements=placements, whole_sign_houses=[], calculation_hash="synthetic", metadata={}
    )
    set_ascendant(chart, 0.0)
    return chart

def set_planet(chart: CanonicalVedicChart, planet: str, longitude: float):
    lon = longitude % 360.0
    idx = int(lon / 30.0) % 12
    chart.placements[planet].sidereal_longitude = lon
    chart.placements[planet].rashi = RashiPosition(absolute_longitude=lon, sign=ZODIAC_SIGNS[idx], sign_index=idx+1, degree=int(lon%30), minute=0, second=0)

def set_ascendant(chart: CanonicalVedicChart, longitude: float):
    lon = longitude % 360.0
    idx = int(lon / 30.0) % 12
    chart.ascendant = RashiPosition(absolute_longitude=lon, sign=ZODIAC_SIGNS[idx], sign_index=idx+1, degree=int(lon%30), minute=0, second=0)

    # Update houses based on ascendant
    from apps.api.engines.vedic.houses import generate_whole_sign_houses
    chart.whole_sign_houses = generate_whole_sign_houses(chart.ascendant)
