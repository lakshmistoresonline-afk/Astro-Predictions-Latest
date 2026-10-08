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
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/dbname")
    monkeypatch.setenv("OLLAMA_BASE_URL", "https://ollama.yourdomain.com")

    with pytest.raises(RuntimeError) as exc_info:
        validate_and_init_secrets()

    assert "CRITICAL SECURITY ERROR: Production deployment refused" in str(exc_info.value)
    assert "ADMIN_API_KEY" in str(exc_info.value)

def test_production_mode_refuses_default_jwt_key(monkeypatch):
    """Production mode MUST refuse to start if JWT_SECRET_KEY is missing or set to a default secret."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("ADMIN_API_KEY", "a_valid_long_production_admin_api_key_888")
    monkeypatch.setenv("JWT_SECRET_KEY", "change_me")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/dbname")
    monkeypatch.setenv("OLLAMA_BASE_URL", "https://ollama.yourdomain.com")

    with pytest.raises(RuntimeError) as exc_info:
        validate_and_init_secrets()

    assert "CRITICAL SECURITY ERROR: Production deployment refused" in str(exc_info.value)
    assert "JWT_SECRET_KEY" in str(exc_info.value)

def test_production_mode_refuses_sqlite_database_url(monkeypatch):
    """Production mode MUST refuse to start if DATABASE_URL is missing or uses local SQLite."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("ADMIN_API_KEY", "a_valid_long_production_admin_api_key_888")
    monkeypatch.setenv("JWT_SECRET_KEY", "a_valid_long_production_jwt_secret_key_999")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./astrovision.db")
    monkeypatch.setenv("OLLAMA_BASE_URL", "https://ollama.yourdomain.com")

    with pytest.raises(RuntimeError) as exc_info:
        validate_and_init_secrets()

    assert "CRITICAL PERSISTENCE ERROR: Production deployment refused" in str(exc_info.value)
    assert "DATABASE_URL" in str(exc_info.value)

def test_production_mode_refuses_localhost_ollama_url(monkeypatch):
    """Production mode MUST refuse to start if AI_PROVIDER=ollama and OLLAMA_BASE_URL=http://localhost:11434."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("ADMIN_API_KEY", "a_valid_long_production_admin_api_key_888")
    monkeypatch.setenv("JWT_SECRET_KEY", "a_valid_long_production_jwt_secret_key_999")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/dbname")
    monkeypatch.setenv("AI_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")

    with pytest.raises(RuntimeError) as exc_info:
        validate_and_init_secrets()

    assert "CRITICAL DEPLOYMENT ERROR: Production deployment refused" in str(exc_info.value)
    assert "OLLAMA_BASE_URL" in str(exc_info.value)

def test_development_mode_generates_ephemeral_keys(monkeypatch):
    """In development, missing secrets generate process-bound ephemeral random keys."""
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.delenv("ADMIN_API_KEY", raising=False)
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    validate_and_init_secrets()

    assert settings.admin_api_key.startswith("dev_admin_key_")
    assert settings.jwt_secret_key.startswith("dev_jwt_key_")
    assert settings.database_url == "sqlite:///./astrovision.db"
