"""
Test Suite for Persistent Models, User Ownership, and IDOR Prevention.
Verifies two different users CANNOT read, update, delete, or export each other's birth profiles, calculation reports, or saved charts.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

TOKEN_USER_A = "token_user_alpha_123"
TOKEN_USER_B = "token_user_beta_456"

HEADER_A = {"X-User-Token": TOKEN_USER_A}
HEADER_B = {"X-User-Token": TOKEN_USER_B}

@pytest.fixture
def profile_user_a():
    """Creates a birth profile owned by User A."""
    payload = {
        "name": "User A Birth Profile",
        "year": 1990, "month": 5, "day": 15,
        "hour": 14, "minute": 30, "second": 0,
        "timezone_str": "Asia/Kolkata",
        "latitude": 18.9220, "longitude": 72.8347,
        "place_name": "Mumbai", "country": "India"
    }
    resp = client.post("/api/v1/profiles", json=payload, headers=HEADER_A)
    assert resp.status_code == 201
    return resp.json()

def test_health_reports_real_persistent_database_status():
    """GET /health must report real persistent database status."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "database_status" in data
    assert "persistent" in data["database_status"]
    assert data["database_status"] != "standalone_in_memory"

def test_user_a_can_create_and_read_own_profile(profile_user_a):
    """User A can retrieve their own birth profile."""
    profile_id = profile_user_a["id"]
    resp = client.get(f"/api/v1/profiles/{profile_id}", headers=HEADER_A)
    assert resp.status_code == 200
    assert resp.json()["name"] == "User A Birth Profile"

def test_idor_user_b_cannot_read_user_a_profile(profile_user_a):
    """IDOR Check: User B MUST NOT read User A's birth profile."""
    profile_id = profile_user_a["id"]
    resp = client.get(f"/api/v1/profiles/{profile_id}", headers=HEADER_B)
    assert resp.status_code == 404
    assert "not found or access denied" in resp.json()["detail"]

def test_idor_user_b_cannot_update_user_a_profile(profile_user_a):
    """IDOR Check: User B MUST NOT update User A's birth profile."""
    profile_id = profile_user_a["id"]
    payload = {
        "name": "Hacked Name",
        "year": 1990, "month": 5, "day": 15,
        "hour": 14, "minute": 30, "second": 0,
        "timezone_str": "Asia/Kolkata",
        "latitude": 18.9220, "longitude": 72.8347,
        "place_name": "Mumbai", "country": "India"
    }
    resp = client.put(f"/api/v1/profiles/{profile_id}", json=payload, headers=HEADER_B)
    assert resp.status_code == 404
    assert "not found or access denied" in resp.json()["detail"]

def test_idor_user_b_cannot_delete_user_a_profile(profile_user_a):
    """IDOR Check: User B MUST NOT delete User A's birth profile."""
    profile_id = profile_user_a["id"]
    resp = client.delete(f"/api/v1/profiles/{profile_id}", headers=HEADER_B)
    assert resp.status_code == 404

    # Verify profile still exists for User A
    check = client.get(f"/api/v1/profiles/{profile_id}", headers=HEADER_A)
    assert check.status_code == 200

def test_idor_user_b_cannot_access_user_a_report(profile_user_a):
    """IDOR Check: User B MUST NOT access or export User A's calculation reports."""
    profile_id = profile_user_a["id"]

    # User A creates a report
    rep_resp = client.post(f"/api/v1/reports?profile_id={profile_id}", headers=HEADER_A)
    assert rep_resp.status_code == 201
    report_id = rep_resp.json()["id"]

    # User B attempts to read User A's report -> 404
    read_resp = client.get(f"/api/v1/reports/{report_id}", headers=HEADER_B)
    assert read_resp.status_code == 404

    # User B attempts to export User A's report as PDF -> 404
    pdf_resp = client.get(f"/api/v1/reports/{report_id}/pdf", headers=HEADER_B)
    assert pdf_resp.status_code == 404

    # User A CAN access their own report
    owner_read = client.get(f"/api/v1/reports/{report_id}", headers=HEADER_A)
    assert owner_read.status_code == 200

def test_profiles_list_returns_only_owned_records(profile_user_a):
    """User B's profile list MUST NOT contain User A's birth profile."""
    list_a = client.get("/api/v1/profiles", headers=HEADER_A).json()
    list_b = client.get("/api/v1/profiles", headers=HEADER_B).json()

    user_a_ids = [p["id"] for p in list_a]
    user_b_ids = [p["id"] for p in list_b]

    assert profile_user_a["id"] in user_a_ids
    assert profile_user_a["id"] not in user_b_ids
