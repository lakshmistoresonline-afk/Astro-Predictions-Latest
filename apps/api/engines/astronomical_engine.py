"""
Legacy Adapter Wrapper for Astronomical Engine.
Delegates exclusively to SkyfieldJPLProvider backed by NASA JPL DE440s ephemeris.
Zero Meeus approximations, zero synthetic planetary positions, zero independent Rahu/Ketu formulas.
"""
from datetime import datetime, timedelta, timezone
from apps.api.engines.astronomy.providers.skyfield_jpl import SkyfieldJPLProvider
from apps.api.engines.vedic.nodes import calculate_canonical_mean_nodes

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

class AstronomicalEngine:
    """
    Adapter wrapper ensuring single source of truth delegation to SkyfieldJPLProvider and canonical nodes.
    """

    @classmethod
    def calculate_positions(
        cls,
        julian_day: float,
        lat: float,
        lon: float,
        zodiac_system: str = "sidereal",
        ayanamsha: str = "lahiri"
    ) -> dict:
        provider = SkyfieldJPLProvider()

        # Convert JD to UTC datetime
        days_from_j2000 = julian_day - 2451545.0
        dt_utc = datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc) + timedelta(days=days_from_j2000)

        res = provider.calculate_astronomical_state(
            year=dt_utc.year,
            month=dt_utc.month,
            day=dt_utc.day,
            hour=dt_utc.hour,
            minute=dt_utc.minute,
            second=dt_utc.second,
            lat=lat,
            lon=lon,
            elevation=0.0,
            ayanamsha_mode="Lahiri"
        )

        positions = {}
        for body_name, pos in res.raw_ephemeris.bodies.items():
            sid_lon = res.sidereal_state.sidereal_longitudes[body_name]
            s_idx = int(sid_lon / 30.0) % 12
            deg = sid_lon % 30.0

            positions[body_name] = {
                "longitude": round(sid_lon, 4),
                "latitude": round(pos.geocentric_latitude, 4),
                "speed": round(pos.velocity_lon_deg_day, 4),
                "retrograde": pos.retrograde,
                "sign": SIGNS[s_idx],
                "degree": round(deg, 2)
            }

        # Delegates Mean Node calculation exclusively to canonical nodes module
        ayanamsha_val = res.sidereal_state.ayanamsha_value_deg
        rahu_sid_lon, ketu_sid_lon, node_vel = calculate_canonical_mean_nodes(
            res.raw_ephemeris.julian_day_tt,
            ayanamsha_val
        )

        r_idx = int(rahu_sid_lon / 30.0) % 12
        positions["Rahu"] = {
            "longitude": round(rahu_sid_lon, 4),
            "latitude": 0.0,
            "speed": node_vel,
            "retrograde": True,
            "sign": SIGNS[r_idx],
            "degree": round(rahu_sid_lon % 30.0, 2)
        }

        k_idx = int(ketu_sid_lon / 30.0) % 12
        positions["Ketu"] = {
            "longitude": round(ketu_sid_lon, 4),
            "latitude": 0.0,
            "speed": node_vel,
            "retrograde": True,
            "sign": SIGNS[k_idx],
            "degree": round(ketu_sid_lon % 30.0, 2)
        }

        return positions
