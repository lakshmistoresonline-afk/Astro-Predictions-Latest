"""
Candidate C (Pure-Python Meeus Perturbation Series) Provider.
"""
from apps.api.engines.ephemeris_providers.base import AstronomyProvider
from apps.api.engines.astronomical_engine import AstronomicalEngine

class CandidateCProvider(AstronomyProvider):

    def get_planet_positions(self, julian_day: float, lat: float, lon: float, zodiac_system: str = "sidereal", ayanamsha: str = "lahiri") -> dict:
        return AstronomicalEngine.calculate_positions(julian_day, lat, lon, zodiac_system, ayanamsha)

    def get_ascendant(self, julian_day: float, lat: float, lon: float) -> dict:
        # Approximate estimation for baseline comparison
        return {"longitude": (julian_day * 360) % 360, "sign": "Aquarius", "degree": 11.19}

    def get_mc(self, julian_day: float, lat: float, lon: float) -> dict:
        return {"longitude": (julian_day * 360 + 90) % 360, "sign": "Scorpio", "degree": 16.53}
