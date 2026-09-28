"""
Mathematical Calculation Module for Vimshottari Dasha Engine.
Implements exact Parashari Nakshatra progress, remaining birth balance, and 5-level nested duration formulas.
"""
from typing import Tuple, Dict, List
from apps.api.engines.dasha.exceptions import InvalidMoonStateError
from apps.api.engines.dasha.models import BirthNakshatraInfo, BirthDashaBalance

DASHA_YEARS: Dict[str, float] = {
    "Ketu": 7.0,
    "Venus": 20.0,
    "Sun": 6.0,
    "Moon": 10.0,
    "Mars": 7.0,
    "Rahu": 18.0,
    "Jupiter": 16.0,
    "Saturn": 19.0,
    "Mercury": 17.0
}

DASHA_SEQUENCE: List[str] = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

NAKSHATRA_NAMES: List[str] = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

TOTAL_VIMSHOTTARI_YEARS: float = 120.0
DAYS_PER_YEAR: float = 365.25 # Tropical solar year calendar standard
NAKSHATRA_SPAN_DEG: float = 360.0 / 27.0 # 13.333333333333334 degrees
PADA_SPAN_DEG: float = NAKSHATRA_SPAN_DEG / 4.0 # 3.3333333333333335 degrees

def calculate_birth_nakshatra_info(moon_sidereal_lon_deg: float) -> BirthNakshatraInfo:
    """Calculates full precision Nakshatra, Pada, progress fractions, and lord from Moon longitude."""
    if moon_sidereal_lon_deg is None or not (0.0 <= moon_sidereal_lon_deg <= 360.0):
        raise InvalidMoonStateError(f"Moon sidereal longitude '{moon_sidereal_lon_deg}' is invalid or out of range [0, 360).")

    lon = moon_sidereal_lon_deg % 360.0
    nak_idx = int(lon / NAKSHATRA_SPAN_DEG) % 27
    nak_name = NAKSHATRA_NAMES[nak_idx]

    start_lon = nak_idx * NAKSHATRA_SPAN_DEG
    end_lon = (nak_idx + 1) * NAKSHATRA_SPAN_DEG

    elapsed_deg = lon - start_lon
    remaining_deg = NAKSHATRA_SPAN_DEG - elapsed_deg

    elapsed_frac = elapsed_deg / NAKSHATRA_SPAN_DEG
    remaining_frac = remaining_deg / NAKSHATRA_SPAN_DEG

    pada = min(int(elapsed_deg / PADA_SPAN_DEG) + 1, 4)

    lord_idx = nak_idx % 9
    nak_lord = DASHA_SEQUENCE[lord_idx]

    return BirthNakshatraInfo(
        nakshatra_index=nak_idx + 1,
        nakshatra_name=nak_name,
        nakshatra_lord=nak_lord,
        pada=pada,
        start_longitude_deg=round(start_lon, 6),
        end_longitude_deg=round(end_lon, 6),
        moon_sidereal_longitude_deg=round(lon, 6),
        elapsed_degrees=round(elapsed_deg, 6),
        remaining_degrees=round(remaining_deg, 6),
        elapsed_fraction=round(elapsed_frac, 6),
        remaining_fraction=round(remaining_frac, 6)
    )

def calculate_child_duration_days(parent_days: float, child_lord: str) -> float:
    """
    Computes exact duration in days for a nested sub-period.
    Formula: Child Duration = Parent Duration * (Child Lord Vimshottari Years / 120.0)
    """
    if child_lord not in DASHA_YEARS:
        raise ValueError(f"Unknown planetary lord identifier: '{child_lord}'")

    child_years = DASHA_YEARS[child_lord]
    return parent_days * (child_years / TOTAL_VIMSHOTTARI_YEARS)
