"""
Custom Exceptions for Astrovision Astronomy Provider Engine.
Enforces fail-closed behavior on ephemeris initialization or calculation failures.
"""

class AstronomyProviderError(Exception):
    """Base exception for all astronomy provider operational errors."""
    pass

class KernelNotFoundError(AstronomyProviderError):
    """Raised when the specified JPL ephemeris kernel file is missing, corrupted, or unreadable."""
    pass

class ProviderInitializationError(AstronomyProviderError):
    """Raised when the astronomy provider software dependency (e.g. Skyfield) fails to load."""
    pass

class CalculationError(AstronomyProviderError):
    """Raised when an astronomical calculation fails due to out-of-range dates or numerical error."""
    pass
