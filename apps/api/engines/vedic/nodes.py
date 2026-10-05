"""
Centralized Authoritative Mean Node (Rahu & Ketu) Module.
Section 8 Compliance: Provides a single canonical Mean Node model for Rahu and Ketu across:
  - Natal chart builder
  - Transit engine
  - Nakshatras & Vargas
  - Dasha & Yogas/Doshas
  - Prediction evidence
Enforces Ketu = (Rahu + 180 deg) % 360 deg.
"""
from typing import Tuple

def calculate_canonical_mean_nodes(julian_day_tt: float, ayanamsha_deg: float) -> Tuple[float, float, float]:
    """
    Calculates canonical Mean Rahu sidereal longitude, Mean Ketu sidereal longitude, and daily velocity.
    Formula: T = (JD_TT - 2451545.0) / 36525.0
    Rahu Tropical Lon = (125.04452 - 1934.136261 * T) % 360.0
    Rahu Sidereal Lon = (Rahu Tropical Lon - Ayanamsha) % 360.0
    Ketu Sidereal Lon = (Rahu Sidereal Lon + 180.0) % 360.0
    Returns: (rahu_sidereal_lon, ketu_sidereal_lon, velocity_deg_day)
    """
    T = (julian_day_tt - 2451545.0) / 36525.0
    rahu_trop_lon = (125.04452 - 1934.136261 * T) % 360.0
    rahu_sid_lon = (rahu_trop_lon - ayanamsha_deg) % 360.0
    ketu_sid_lon = (rahu_sid_lon + 180.0) % 360.0

    # Mean Node mean daily motion: -1934.136261 deg / 36525 days = -0.0529538 deg/day
    velocity_deg_day = -1934.136261 / 36525.0

    return (
        round(rahu_sid_lon, 6),
        round(ketu_sid_lon, 6),
        round(velocity_deg_day, 6)
    )
