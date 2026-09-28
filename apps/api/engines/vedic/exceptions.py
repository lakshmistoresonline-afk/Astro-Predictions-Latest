"""
Custom Exceptions for Astrovision Canonical Vedic Engine Foundation.
Enforces strict fail-closed validation on birth data, timezone, boundaries, and astronomical execution.
"""

class VedicEngineError(Exception):
    """Base exception for all canonical Vedic engine operational errors."""
    pass

class InvalidBirthDataError(VedicEngineError):
    """Raised when birth input contains missing, physically invalid, or unresolvable data."""
    pass

class TimezoneResolutionError(VedicEngineError):
    """Raised when timezone string cannot be resolved in the authoritative timezone database."""
    pass

class OutOfBoundaryError(VedicEngineError):
    """Raised when birth timestamp falls outside the supported astronomical horizon (1850 - 2150)."""
    pass

class AstronomyExecutionError(VedicEngineError):
    """Raised when underlying astronomy provider calculation fails."""
    pass
