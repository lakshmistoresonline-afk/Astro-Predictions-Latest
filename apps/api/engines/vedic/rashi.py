"""
Deterministic Rashi (Zodiac Sign) Module for Astrovision.
Calculates full precision Rashi placement (Sign, Degree, Minute, Second) from absolute sidereal longitude.
Sections 4, 6 & 29 Compliance: Centralized single authoritative sign lords, exaltations, debilitations, and own signs mappings!
"""
import math
from apps.api.engines.vedic.models import RashiPosition

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
RASHI_NAMES = ZODIAC_SIGNS

# 1-based Rashi index (1 = Aries ... 12 = Pisces) to ruling planet name
RASHI_LORDS = {
    1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
    5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
    9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
}

# Exaltation & Debilitation Signs (1-based Rashi index)
EXALTATION_SIGNS = {
    "Sun": 1, "Moon": 2, "Mars": 10, "Mercury": 6,
    "Jupiter": 4, "Venus": 12, "Saturn": 7, "Rahu": 2, "Ketu": 8
}

DEBILITATION_SIGNS = {
    "Sun": 7, "Moon": 8, "Mars": 4, "Mercury": 12,
    "Jupiter": 10, "Venus": 6, "Saturn": 1, "Rahu": 8, "Ketu": 2
}

OWN_SIGNS = {
    "Sun": [5],
    "Moon": [4],
    "Mars": [1, 8],
    "Mercury": [3, 6],
    "Jupiter": [9, 12],
    "Venus": [2, 7],
    "Saturn": [10, 11]
}

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
