"""
Test Suite for Secret Management, Production Secret Startup Validation, and Secret Scanning.
"""
import os
import pytest
from apps.api.config import settings, validate_and_init_secrets

def test_production_mode_refuses_default_admin_key(monkeypatch):
    """Production mode MUST refuse to start if ADMIN_API_KEY is missing or set to a default secret."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("ADMIN_API_KEY", "change_me")
    monkeypatch.setenv("JWT_SECRET_KEY", "a_valid_long_production_jwt_secret_key_999")

    with pytest.raises(RuntimeError) as exc_info:
        validate_and_init_secrets()

    assert "CRITICAL SECURITY ERROR: Production deployment refused" in str(exc_info.value)
    assert "ADMIN_API_KEY" in str(exc_info.value)

def test_production_mode_refuses_default_jwt_key(monkeypatch):
    """Production mode MUST refuse to start if JWT_SECRET_KEY is missing or set to a default secret."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("ADMIN_API_KEY", "a_valid_long_production_admin_api_key_888")
    monkeypatch.setenv("JWT_SECRET_KEY", "change_me")

    with pytest.raises(RuntimeError) as exc_info:
        validate_and_init_secrets()

    assert "CRITICAL SECURITY ERROR: Production deployment refused" in str(exc_info.value)
    assert "JWT_SECRET_KEY" in str(exc_info.value)

def test_development_mode_generates_ephemeral_keys(monkeypatch):
    """In development, missing secrets generate process-bound ephemeral random keys."""
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.delenv("ADMIN_API_KEY", raising=False)
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    validate_and_init_secrets()

    assert settings.admin_api_key.startswith("dev_admin_key_")
    assert settings.jwt_secret_key.startswith("dev_jwt_key_")
