"""
Deterministic Rashi (Zodiac Sign) Module for Astrovision.
Calculates full precision Rashi placement (Sign, Degree, Minute, Second) from absolute sidereal longitude.
"""
import math
from apps.api.engines.vedic.models import RashiPosition

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def calculate_rashi(sidereal_longitude_deg: float) -> RashiPosition:
    """
    Converts an absolute sidereal longitude in [0.0, 360.0) into a full-precision RashiPosition.
    Does not round prior to classification.
    """
    lon = sidereal_longitude_deg % 360.0
    sign_idx = int(lon / 30.0) % 12
    sign_name = ZODIAC_SIGNS[sign_idx]

    rem_deg = lon % 30.0
    deg = int(rem_deg)

    rem_min = (rem_deg - deg) * 60.0
    minute = int(rem_min)

    sec = (rem_min - minute) * 60.0

    return RashiPosition(
        absolute_longitude=round(lon, 6),
        sign=sign_name,
        sign_index=sign_idx + 1,
        degree=deg,
        minute=minute,
        second=round(sec, 4)
    )
