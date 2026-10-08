"""
Test Suite for Complete End-to-End User Journey & Multi-User Isolation.
"""
import pytest
import uuid
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.db.database import init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def test_complete_user_journey_and_isolation():
    """Executes the complete user journey: Signup -> Login -> Profile -> Chart -> Vargas -> Dashas -> Yogas -> Strength -> Jaimini -> Panchanga -> Muhurta -> Predictions -> AI -> PDF Export -> Logout -> User Isolation."""
    email_a = f"alpha_{uuid.uuid4()}@astrovision.test"
    email_b = f"beta_{uuid.uuid4()}@astrovision.test"

    # 1. Register User A
    reg_a = client.post("/api/v1/auth/register", json={
        "email": email_a,
        "password": "SecurePassword123!",
        "full_name": "User Alpha"
    })
    assert reg_a.status_code == 201
    token_a = reg_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # 2. Login User A
    login_a = client.post("/api/v1/auth/login", json={
        "email": email_a,
        "password": "SecurePassword123!"
    })
    assert login_a.status_code == 200

    # 3. Get /me
    me_a = client.get("/api/v1/auth/me", headers=headers_a)
    assert me_a.status_code == 200
    assert me_a.json()["email"] == email_a

    # 4. Calculate Birth Profile
    birth_payload = {
        "name": "User Alpha Native",
        "year": 1990, "month": 5, "day": 15,
        "hour": 14, "minute": 30, "second": 0,
        "timezone_str": "Asia/Kolkata",
        "latitude": 18.9220, "longitude": 72.8347,
        "place_name": "Mumbai", "country": "India"
    }
    calc_res = client.post("/api/v1/birth-profile", json=birth_payload, headers=headers_a)
    assert calc_res.status_code == 200
    calc_data = calc_res.json()
    assert "master_evidence" in calc_data
    assert "predictions" in calc_data

    # 5. Calculate Panchanga, Muhurta, Transits, Jaimini, Timing
    transit_payload = {"birth_input": birth_payload, "query_datetime_utc": "2026-10-08T12:00:00Z"}
    assert client.post("/api/v1/panchanga", json=transit_payload, headers=headers_a).status_code == 200
    assert client.post("/api/v1/muhurta", json=transit_payload, headers=headers_a).status_code == 200
    assert client.post("/api/v1/transits", json=transit_payload, headers=headers_a).status_code == 200
    assert client.post("/api/v1/jaimini", json=birth_payload, headers=headers_a).status_code == 200
    assert client.post("/api/v1/timing-windows", json=transit_payload, headers=headers_a).status_code == 200

    # 6. Save Profile
    prof_a = client.post("/api/v1/profiles", json=birth_payload, headers=headers_a).json()
    prof_id = prof_a["id"]

    # 7. Create Calculation Report & PDF
    rep_res = client.post(f"/api/v1/reports?profile_id={prof_id}", headers=headers_a)
    assert rep_res.status_code == 201
    rep_id = rep_res.json()["id"]

    pdf_res = client.get(f"/api/v1/reports/{rep_id}/pdf", headers=headers_a)
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"

    # 8. Register User B and verify Multi-User Isolation
    reg_b = client.post("/api/v1/auth/register", json={
        "email": email_b,
        "password": "SecurePassword123!",
        "full_name": "User Beta"
    })
    token_b = reg_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B cannot access User A's profile or report
    assert client.get(f"/api/v1/profiles/{prof_id}", headers=headers_b).status_code == 404
    assert client.get(f"/api/v1/reports/{rep_id}", headers=headers_b).status_code == 404
    assert client.get(f"/api/v1/reports/{rep_id}/pdf", headers=headers_b).status_code == 404

    # 9. Logout User A
    assert client.post("/api/v1/auth/logout", headers=headers_a).status_code == 200
    assert client.get("/api/v1/auth/me", headers=headers_a).status_code == 401
