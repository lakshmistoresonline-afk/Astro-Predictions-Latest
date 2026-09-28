"""
Deterministic Nakshatra and Pada Classification Module for Astrovision.
Calculates full precision Nakshatra (1-27) and Pada (1-4) from absolute sidereal longitude.
"""
from apps.api.engines.vedic.models import NakshatraPada

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

NAKSHATRA_SPAN_DEG = 360.0 / 27.0 # 13.333333333333334 degrees (13° 20')
PADA_SPAN_DEG = NAKSHATRA_SPAN_DEG / 4.0 # 3.3333333333333335 degrees (3° 20')

def calculate_nakshatra_pada(sidereal_longitude_deg: float) -> NakshatraPada:
    """
    Classifies absolute sidereal longitude into Nakshatra (1-27) and Pada (1-4).
    Does not round prior to classification.
    """
    lon = sidereal_longitude_deg % 360.0
    nak_idx = int(lon / NAKSHATRA_SPAN_DEG) % 27
    nak_name = NAKSHATRAS[nak_idx]

    start_deg = nak_idx * NAKSHATRA_SPAN_DEG
    end_deg = (nak_idx + 1) * NAKSHATRA_SPAN_DEG

    deg_in_nak = lon % NAKSHATRA_SPAN_DEG
    pada = min(int(deg_in_nak / PADA_SPAN_DEG) + 1, 4)

    return NakshatraPada(
        nakshatra=nak_name,
        nakshatra_index=nak_idx + 1,
        absolute_start_deg=round(start_deg, 6),
        absolute_end_deg=round(end_deg, 6),
        degree_within_nakshatra=round(deg_in_nak, 6),
        pada=pada
    )
