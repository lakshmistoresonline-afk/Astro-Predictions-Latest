"""
Deterministic Sidereal Layer for Astrovision.
Implements IAU/NFA Chitrapaksha (Lahiri) Ayanamsha conversion from Tropical longitudes.
"""

def calculate_lahiri_ayanamsha(julian_day_tt: float) -> float:
    """
    Computes Lahiri Ayanamsha for a given Julian Day (Terrestrial Time).
    Epoch: J2000.0 (JD 2451545.0)
    Base value at J2000.0: 23.8530556 degrees (23° 51' 11")
    Linear precession drift: ~50.29" / year = 0.0139688 deg/year
    """
    T = (julian_day_tt - 2451545.0) / 365.25
    return 23.8530556 + 0.0139688 * T

def convert_tropical_to_sidereal(tropical_lon_deg: float, ayanamsha_deg: float) -> float:
    """Converts a tropical ecliptic longitude to sidereal longitude in [0, 360)."""
    return (tropical_lon_deg - ayanamsha_deg) % 360.0
