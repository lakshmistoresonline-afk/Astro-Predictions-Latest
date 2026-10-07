"""
Security Test Suite for Server-Side Admin Authorization, User Scopes, and Admin Route Verification.
"""
import pytest
import uuid
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.config import settings, validate_and_init_secrets
from apps.api.db.database import init_db

@pytest.fixture(autouse=True)
def setup_database_and_secrets():
    validate_and_init_secrets()
    init_db()

client = TestClient(app)

def get_auth_token(email: str, name: str) -> str:
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": "SecurePassword123!"})
    if login_res.status_code == 200:
        return login_res.json()["access_token"]

    reg_res = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "SecurePassword123!",
        "full_name": name
    })
    if reg_res.status_code == 201:
        return reg_res.json()["access_token"]

    raise RuntimeError(f"Failed to obtain auth token for {email}: {reg_res.text}")

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
    admin_key = settings.admin_api_key
    assert admin_key is not None
    response = client.get("/api/v1/admin/stats", headers={"X-Admin-Key": admin_key})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["admin_status"] == "authenticated"

def test_admin_stats_authorized_valid_bearer_token():
    """Valid Authorization Bearer token header must grant HTTP 200 OK access for admin key."""
    admin_key = settings.admin_api_key
    assert admin_key is not None
    response = client.get("/api/v1/admin/stats", headers={"Authorization": f"Bearer {admin_key}"})
    assert response.status_code == 200
    data = response.json()
    assert data["admin_status"] == "authenticated"

def test_user_compatibility_endpoint_requires_auth():
    """Ashtakoota compatibility endpoint requires valid Bearer JWT token."""
    payload = {
        "person_a_nakshatra": "Ashwini",
        "person_b_nakshatra": "Rohini"
    }
    # Unauthenticated -> 401
    assert client.post("/api/v1/compatibility", json=payload).status_code == 401

    # Authenticated -> 200
    token = get_auth_token("compat_user@astrovision.test", "Compat User")
    response = client.post("/api/v1/compatibility", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["system"] == "Ashtakoota Vedic Matching (36 Points)"

def test_user_rectification_endpoint_requires_auth():
    """User birth time rectification endpoint requires valid Bearer JWT token."""
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
    # Unauthenticated -> 401
    assert client.post("/api/v1/rectification", json=payload).status_code == 401

    # Authenticated -> 200
    token = get_auth_token("rect_user@astrovision.test", "Rect User")
    response = client.post("/api/v1/rectification", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["best_candidate_offset_minutes"] in [-5, 0, 5]

def test_user_pdf_export_endpoint_requires_auth():
    """User PDF export endpoint requires valid Bearer JWT token."""
    payload = {
        "name": "Jane Doe",
        "year": 1995, "month": 1, "day": 1,
        "hour": 12, "minute": 0,
        "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "New Delhi", "country": "India",
        "timezone_str": "Asia/Kolkata"
    }
    # Unauthenticated -> 401
    assert client.post("/api/v1/export/pdf", json=payload).status_code == 401

    # Authenticated -> 200
    token = get_auth_token("pdf_user@astrovision.test", "PDF User")
    response = client.post("/api/v1/export/pdf", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
