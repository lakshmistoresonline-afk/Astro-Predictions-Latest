"""
Test Suite for Health & Readiness Diagnostics Endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_health_check_returns_subsystem_breakdown():
    """GET /health must return complete status breakdown for API, DB, Ephemeris, and AI provider."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()

    assert data["status"] in ["healthy", "degraded"]
    assert "api_status" in data
    assert "database_status" in data
    assert "ephemeris_status" in data
    assert "ai_provider" in data
    assert "ai_provider_status" in data

def test_readiness_check_returns_ready():
    """GET /ready must return ready=True when DE440s kernel is verified."""
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.json()["ready"] is True
