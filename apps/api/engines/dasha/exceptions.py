"""
Custom Exceptions for Authoritative Vimshottari Dasha Engine (Phase 2C).
Enforces fail-closed error handling on invalid astronomical inputs or calculation errors.
"""

class DashaEngineError(Exception):
    """Base exception for all Dasha engine operational errors."""
    pass

class InvalidMoonStateError(DashaEngineError):
    """Raised when canonical Moon longitude is missing, invalid, or out of range [0, 360)."""
    pass

class OutOfQueryRangeError(DashaEngineError):
    """Raised when query datetime is outside the engine's valid 120-year Vimshottari timeline."""
    pass

class DashaCalculationError(DashaEngineError):
    """Raised when nested Dasha calculation fails or encounters numerical instability."""
    pass
