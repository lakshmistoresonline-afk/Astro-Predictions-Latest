"""
Astronomy Provider Interface for Phase 1C Provider Comparison.
"""
from abc import ABC, abstractmethod

class AstronomyProvider(ABC):

    @abstractmethod
    def get_planet_positions(self, julian_day: float, lat: float, lon: float, zodiac_system: str = "sidereal", ayanamsha: str = "lahiri") -> dict:
        pass

    @abstractmethod
    def get_ascendant(self, julian_day: float, lat: float, lon: float) -> dict:
        pass

    @abstractmethod
    def get_mc(self, julian_day: float, lat: float, lon: float) -> dict:
        pass
