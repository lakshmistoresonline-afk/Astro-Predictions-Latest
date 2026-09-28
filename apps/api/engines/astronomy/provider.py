"""
Provider-Neutral Abstract Interface for Astrovision Astronomy Providers.
"""
from abc import ABC, abstractmethod
from apps.api.engines.astronomy.models import CalculationResult

class BaseAstronomyProvider(ABC):
    """Abstract Base Class for all high-precision astronomy calculation providers."""

    @abstractmethod
    def calculate_astronomical_state(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        lat: float = 0.0,
        lon: float = 0.0,
        elevation: float = 0.0,
        ayanamsha_mode: str = "Lahiri"
    ) -> CalculationResult:
        """
        Calculates the full canonical astronomical state for a given UTC timestamp and geographic location.
        """
        pass
