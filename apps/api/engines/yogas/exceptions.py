"""
Custom Exceptions for Astrovision Yoga & Dosha Engine Foundation.
Enforces fail-closed validation on missing input states or rule evaluation errors.
"""

class YogaEngineError(Exception):
    """Base exception for all Yoga and Dosha engine operational errors."""
    pass

class MissingCanonicalStateError(YogaEngineError):
    """Raised when canonical chart or required placement state is missing."""
    pass

class RuleEvaluationError(YogaEngineError):
    """Raised when a specific Yoga or Dosha rule evaluation encounters an unhandled exception."""
    pass
