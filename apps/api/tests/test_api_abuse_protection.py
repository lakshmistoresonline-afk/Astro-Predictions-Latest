"""
Test Suite for API Abuse Protection, Payload Bounds, and Input Validation.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.db.database import init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def get_auth_token(email: str = "abuse_test_user@astrovision.test") -> str:
    res = client.post("/api/v1/auth/register", json={
        "email": email, "password": "Password123!", "full_name": "Abuse Protection User"
    })
    if res.status_code == 201:
        return res.json()["access_token"]
    login = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    return login.json()["access_token"]

def test_latitude_out_of_bounds_rejected():
    """Latitude > 90.0 must be rejected with 400 or 422."""
    token = get_auth_token()
    payload = {
        "name": "Bad Lat", "year": 1995, "month": 1, "day": 1, "hour": 12, "minute": 0,
        "timezone_str": "Asia/Kolkata", "latitude": 150.0, "longitude": 77.2090,
        "place_name": "Delhi", "country": "India"
    }
    response = client.post("/api/v1/birth-profile", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [400, 422]

def test_longitude_out_of_bounds_rejected():
    """Longitude > 180.0 must be rejected with 400 or 422."""
    token = get_auth_token()
    payload = {
        "name": "Bad Lon", "year": 1995, "month": 1, "day": 1, "hour": 12, "minute": 0,
        "timezone_str": "Asia/Kolkata", "latitude": 28.6139, "longitude": 250.0,
        "place_name": "Delhi", "country": "India"
    }
    response = client.post("/api/v1/birth-profile", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [400, 422]

def test_year_outside_ephemeris_range_rejected():
    """Year > 2150 must be rejected with 400 or 422."""
    token = get_auth_token()
    payload = {
        "name": "Bad Year", "year": 2300, "month": 1, "day": 1, "hour": 12, "minute": 0,
        "timezone_str": "Asia/Kolkata", "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "Delhi", "country": "India"
    }
    response = client.post("/api/v1/birth-profile", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [400, 422]
