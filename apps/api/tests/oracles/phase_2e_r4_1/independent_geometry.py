"""
Independent Astronomical & Astrological Geometry Utilities for R4 Oracle.
Does NOT import production engines.
"""
import math

def independent_angular_distance(lon1: float, lon2: float) -> float:
    """Returns shortest angular distance between two longitudes on a 360-degree circle."""
    delta = abs(lon1 - lon2) % 360.0
    return min(delta, 360.0 - delta)

def independent_declination(sidereal_lon: float, ayanamsha: float) -> float:
    """Calculates approximate declination (Kranti) in degrees from sidereal longitude and ayanamsha."""
    tropical_lon = (sidereal_lon + ayanamsha) % 360.0
    return 23.44 * math.sin(math.radians(tropical_lon))

def independent_drishti_pinda(source_planet: str, source_lon: float, target_lon: float) -> float:
    """
    Independent BPHS Drishti Pinda calculation from aspecting planet to target longitude.
    Returns 0.0 to 60.0 shashtiamsas.
    """
    dist = (target_lon - source_lon) % 360.0

    drishti = 0.0
    if 30.0 <= dist <= 60.0:
        drishti = (dist - 30.0) * 0.5
    elif 60.0 < dist <= 90.0:
        drishti = (dist - 60.0) + 15.0
    elif 90.0 < dist <= 120.0:
        drishti = (120.0 - dist) * 1.5
    elif 120.0 < dist <= 150.0:
        drishti = 0.0
    elif 150.0 < dist <= 180.0:
        drishti = (dist - 150.0) * 2.0
    elif 180.0 < dist <= 300.0:
        drishti = (300.0 - dist) / 2.0

    # Special aspect additions per BPHS
    if source_planet == "Mars":
        if 90.0 <= dist <= 120.0 or 210.0 <= dist <= 240.0:
            drishti += 15.0
    elif source_planet == "Jupiter":
        if 120.0 <= dist <= 150.0 or 240.0 <= dist <= 270.0:
            drishti += 30.0
    elif source_planet == "Saturn":
        if 60.0 <= dist <= 90.0 or 270.0 <= dist <= 300.0:
            drishti += 45.0

    return min(60.0, drishti)
