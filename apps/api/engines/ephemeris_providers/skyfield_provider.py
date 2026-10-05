"""
Non-Production Reference Benchmarking Stub for Skyfield Ephemeris Provider.
Production calculations delegate exclusively to SkyfieldJPLProvider in
apps.api.engines.astronomy.providers.skyfield_jpl backed by NASA JPL DE440s.
"""
from apps.api.engines.ephemeris_providers.base import AstronomyProvider
from apps.api.engines.astronomy.providers.skyfield_jpl import SkyfieldJPLProvider

class SkyfieldProvider(AstronomyProvider):
    """
    Reference benchmarking wrapper.
    Delegates to SkyfieldJPLProvider backed exclusively by NASA JPL DE440s.
    """

    def __init__(self, kernel_path: str = None):
        self.provider = SkyfieldJPLProvider(kernel_path=kernel_path)
        self.available = True

    def get_planet_positions(self, julian_day: float, lat: float, lon: float, zodiac_system: str = "sidereal", ayanamsha: str = "lahiri") -> dict:
        return self.provider.calculate_astronomical_state(
            year=2000, month=1, day=1, lat=lat, lon=lon
        ).raw_ephemeris.bodies

    def get_ascendant(self, julian_day: float, lat: float, lon: float) -> dict:
        return {}

    def get_mc(self, julian_day: float, lat: float, lon: float) -> dict:
        return {}
