"""
Custom Domain Exception Hierarchy for Astrovision.
Provides strongly typed domain exceptions mapped to HTTP status codes, error codes, and sanitization policies.
"""
from typing import Optional

class AstrovisionException(Exception):
    """Base exception for all domain errors in Astrovision."""
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_SERVER_ERROR"
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

class AstrovisionValidationError(AstrovisionException):
    """Raised for input validation failures (out-of-range coordinates, invalid dates)."""
    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(message, status_code=400, error_code=error_code)

class TimezoneError(AstrovisionValidationError):
    """Raised for unresolvable or missing IANA timezone strings."""
    def __init__(self, message: str):
        super().__init__(message, error_code="TIMEZONE_ERROR")

class ResourceNotFoundError(AstrovisionException):
    """Raised when a requested resource is missing or access is denied (IDOR protection)."""
    def __init__(self, message: str):
        super().__init__(message, status_code=404, error_code="RESOURCE_NOT_FOUND")

class AuthenticationError(AstrovisionException):
    """Raised for missing or malformed authentication credentials."""
    def __init__(self, message: str):
        super().__init__(message, status_code=401, error_code="AUTHENTICATION_FAILED")

class AuthorizationError(AstrovisionException):
    """Raised for forbidden resource or admin endpoint access."""
    def __init__(self, message: str):
        super().__init__(message, status_code=403, error_code="AUTHORIZATION_FAILED")

class ResourceConflictError(AstrovisionException):
    """Raised for duplicate resource creation conflicts."""
    def __init__(self, message: str):
        super().__init__(message, status_code=409, error_code="RESOURCE_CONFLICT")

class RateLimitExceededError(AstrovisionException):
    """Raised when user exceeds daily request governance quota."""
    def __init__(self, message: str):
        super().__init__(message, status_code=429, error_code="RATE_LIMIT_EXCEEDED")

class AstronomyKernelError(AstrovisionException):
    """Raised when the NASA JPL DE440s ephemeris kernel is missing, unreadable, or invalid."""
    def __init__(self, message: str):
        super().__init__(message, status_code=503, error_code="ASTRONOMY_KERNEL_UNAVAILABLE")

class CalculationEngineError(AstrovisionException):
    """Raised when an internal deterministic calculation engine encounters an unrecoverable mathematical error."""
    def __init__(self, message: str):
        super().__init__(message, status_code=500, error_code="CALCULATION_ENGINE_ERROR")
