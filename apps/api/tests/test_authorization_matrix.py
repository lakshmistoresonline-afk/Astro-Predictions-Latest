"""
Authorization Matrix Test Suite for Public, Authenticated User, Owner-Only, and Admin-Only Scopes.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.config import settings

client = TestClient(app)

# Helper to register user and obtain Bearer JWT token
def get_auth_token(email: str, name: str) -> str:
    res = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "SecurePassword123!",
        "full_name": name
    })
    return res.json()["access_token"]

def test_public_scope_endpoints_accessible():
    """Public scope routes (/health, /ready, /version, /register, /login) must be accessible without auth."""
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200
    assert client.get("/version").status_code == 200

def test_authenticated_user_scope_unauthenticated_fails_401():
    """Authenticated user scope endpoints must return HTTP 401 when unauthenticated."""
    assert client.get("/api/v1/auth/me").status_code == 401
    assert client.post("/api/v1/compatibility", json={"person_a_nakshatra": "Ashwini", "person_b_nakshatra": "Rohini"}).status_code == 401
    assert client.post("/api/v1/export/pdf", json={
        "name": "Jane", "year": 1995, "month": 1, "day": 1, "hour": 12, "minute": 0,
        "latitude": 28.6139, "longitude": 77.2090, "place_name": "Delhi", "country": "India", "timezone_str": "Asia/Kolkata"
    }).status_code == 401

def test_authenticated_user_scope_authenticated_succeeds():
    """Authenticated user scope endpoints succeed when valid Bearer JWT token is supplied."""
    token = get_auth_token("auth_scope_user@astrovision.test", "Scope User")
    headers = {"Authorization": f"Bearer {token}"}

    res_me = client.get("/api/v1/auth/me", headers=headers)
    assert res_me.status_code == 200

    res_compat = client.post("/api/v1/compatibility", json={
        "person_a_nakshatra": "Ashwini", "person_b_nakshatra": "Rohini"
    }, headers=headers)
    assert res_compat.status_code == 200
    assert res_compat.json()["system"] == "Ashtakoota Vedic Matching (36 Points)"

def test_owner_only_scope_idor_protection():
    """Owner-only scope endpoints must enforce server-side user ownership (User B cannot access User A resources)."""
    token_a = get_auth_token("owner_a@astrovision.test", "Owner A")
    token_b = get_auth_token("owner_b@astrovision.test", "Owner B")

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A creates a profile
    profile_a = client.post("/api/v1/profiles", json={
        "name": "User A Profile", "year": 1990, "month": 5, "day": 15,
        "hour": 14, "minute": 30, "timezone_str": "Asia/Kolkata",
        "latitude": 18.9220, "longitude": 72.8347, "place_name": "Mumbai", "country": "India"
    }, headers=headers_a).json()
    prof_id = profile_a["id"]

    # User B attempts to access User A's profile -> 404
    assert client.get(f"/api/v1/profiles/{prof_id}", headers=headers_b).status_code == 404
    assert client.delete(f"/api/v1/profiles/{prof_id}", headers=headers_b).status_code == 404

    # User A CAN access their own profile
    assert client.get(f"/api/v1/profiles/{prof_id}", headers=headers_a).status_code == 200

def test_admin_only_scope_authorization():
    """Admin-only scope endpoints must enforce verify_admin_key (401 on missing, 403 on invalid)."""
    # Missing admin key -> 401
    assert client.get("/api/v1/admin/stats").status_code == 401

    # Invalid admin key -> 403
    assert client.get("/api/v1/admin/stats", headers={"X-Admin-Key": "invalid_key"}).status_code == 403

    # Valid admin key -> 200
    res_admin = client.get("/api/v1/admin/stats", headers={"X-Admin-Key": settings.admin_api_key})
    assert res_admin.status_code == 200
    assert res_admin.json()["admin_status"] == "authenticated"
