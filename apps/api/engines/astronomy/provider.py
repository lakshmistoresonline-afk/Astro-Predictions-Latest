"""
Provider-Neutral Abstract Interface for Astrovision Astronomy Providers.
"""
import os
import hashlib
from abc import ABC, abstractmethod
from typing import Tuple
from apps.api.engines.astronomy.models import CalculationResult

EXPECTED_DE440S_SHA256 = "c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2"

def verify_de440s_kernel_status() -> Tuple[bool, str]:
    """Verifies that the NASA JPL DE440s kernel exists, exceeds 30MB, and matches SHA-256."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    kernel_path = os.path.join(base_dir, "de440s.bsp")
    if not os.path.exists(kernel_path):
        return False, f"DE440s kernel missing at {kernel_path}"
    if os.path.getsize(kernel_path) < 30000000:
        return False, "DE440s kernel file corrupted or size less than 30MB"

    try:
        with open(kernel_path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        if h == EXPECTED_DE440S_SHA256:
            return True, "DE440s Verified"
        return False, f"Kernel SHA-256 mismatch: got {h}"
    except Exception as e:
        return False, str(e)

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
