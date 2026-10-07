"""
Security Test Suite for Server-Side Admin Authorization, Public Scopes, and IDOR Controls.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.config import settings

client = TestClient(app)

def test_admin_stats_unauthorized_missing_header():
    """Missing administrative credentials header must return HTTP 401 Unauthorized."""
    response = client.get("/api/v1/admin/stats")
    assert response.status_code == 401
    assert "Missing administrative credentials" in response.json()["detail"]

def test_admin_stats_unauthorized_invalid_key():
    """Invalid administrative key must return HTTP 403 Forbidden."""
    response = client.get("/api/v1/admin/stats", headers={"X-Admin-Key": "invalid_malicious_key"})
    assert response.status_code == 403
    assert "Invalid administrative key" in response.json()["detail"]

def test_admin_stats_authorized_valid_x_admin_key():
    """Valid X-Admin-Key header must grant HTTP 200 OK access."""
    response = client.get("/api/v1/admin/stats", headers={"X-Admin-Key": settings.admin_api_key})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["admin_status"] == "authenticated"

def test_admin_stats_authorized_valid_bearer_token():
    """Valid Authorization Bearer token header must grant HTTP 200 OK access."""
    response = client.get("/api/v1/admin/stats", headers={"Authorization": f"Bearer {settings.admin_api_key}"})
    assert response.status_code == 200
    data = response.json()
    assert data["admin_status"] == "authenticated"

def test_public_compatibility_endpoint_accessible():
    """Public Ashtakoota compatibility endpoint must remain accessible to non-admin users."""
    payload = {
        "person_a_nakshatra": "Ashwini",
        "person_b_nakshatra": "Rohini"
    }
    response = client.post("/api/v1/compatibility", json=payload)
    assert response.status_code == 200
    assert response.json()["system"] == "Ashtakoota Vedic Matching (36 Points)"

def test_user_rectification_endpoint_accessible():
    """User birth time rectification endpoint must remain accessible without admin key."""
    payload = {
        "birth_input": {
            "name": "Jane",
            "year": 1995, "month": 1, "day": 1,
            "hour": 12, "minute": 0,
            "timezone_str": "Asia/Kolkata",
            "latitude": 28.6139, "longitude": 77.2090
        },
        "events": [],
        "candidate_offsets_minutes": [-5, 0, 5]
    }
    response = client.post("/api/v1/rectification", json=payload)
    assert response.status_code == 200
    assert response.json()["best_candidate_offset_minutes"] in [-5, 0, 5]

def test_user_pdf_export_endpoint_accessible():
    """User PDF export endpoint must process valid request payloads without administrative headers."""
    payload = {
        "name": "Jane Doe",
        "year": 1995, "month": 1, "day": 1,
        "hour": 12, "minute": 0,
        "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "New Delhi", "country": "India",
        "timezone_str": "Asia/Kolkata"
    }
    response = client.post("/api/v1/export/pdf", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
