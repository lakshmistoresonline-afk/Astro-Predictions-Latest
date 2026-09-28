"""
Custom Exceptions for Astrovision Strength & Ashtakavarga Engine.
Enforces strict fail-closed validation on missing input states or evaluation errors.
"""

class StrengthEngineError(Exception):
    """Base exception for all Strength and Ashtakavarga engine operational errors."""
    pass

class MissingCanonicalStateError(StrengthEngineError):
    """Raised when canonical chart or required placement state is missing."""
    pass

class UnsupportedPlanetError(StrengthEngineError):
    """Raised when attempting to calculate classical strength/ashtakavarga for an unsupported planet (e.g., outer planets)."""
    pass

class InvalidCalculationStateError(StrengthEngineError):
    """Raised when an invalid mathematical state prevents strength calculation."""
    pass
