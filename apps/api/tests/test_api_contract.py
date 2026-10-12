"""
Test Suite for Versioned /api/v1 OpenAPI Contract, Request/Response Schemas, and Structured Error Shapes.
"""
import uuid
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.middleware.rate_limiter import heavy_endpoint_limiter

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_rate_limiter():
    heavy_endpoint_limiter._requests.clear()
    yield
    heavy_endpoint_limiter._requests.clear()

def get_auth_headers(email_prefix: str = "contract_user") -> dict:
    email = f"{email_prefix}_{uuid.uuid4()}@astrovision.test"
    reg = client.post("/api/v1/auth/register", json={
        "email": email, "password": "Password123!", "full_name": "Contract Test User"
    })
    if reg.status_code == 201:
        token = reg.json()["access_token"]
    else:
        login = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
        token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_openapi_schema_endpoint():
    """OpenAPI schema /openapi.json must be accessible and contain /api/v1 routes."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema

    paths = schema["paths"]
    assert "/api/v1/birth-profile" in paths
    assert "/api/v1/panchanga" in paths
    assert "/api/v1/muhurta" in paths
    assert "/api/v1/transits" in paths
    assert "/api/v1/jaimini" in paths
    assert "/api/v1/timing-windows" in paths
    assert "/api/v1/interpret-evidence" in paths

def test_birth_profile_request_and_response_contract():
    """Birth profile calculation endpoint contract validation."""
    headers = get_auth_headers("contract_profile")
    payload = {
        "name": "John Doe",
        "year": 1995, "month": 1, "day": 1,
        "hour": 12, "minute": 0, "second": 0,
        "timezone_str": "Asia/Kolkata",
        "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "New Delhi", "country": "India",
        "zodiac_system": "sidereal", "ayanamsha": "lahiri"
    }
    response = client.post("/api/v1/birth-profile", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert data["status"].upper() == "SUCCESS"
    assert data["birth_input"]["name"] == "John Doe"
    assert "canonical_chart" in data["master_evidence"]
    assert "predictions" in data

def test_structured_error_response_shape():
    """Validation errors must return a structured JSON error shape with detail, error_code, and timestamp_iso."""
    headers = get_auth_headers("contract_error")
    payload = {
        "name": "Jane",
        "year": 1995, "month": 1, "day": 1,
        "hour": 12, "minute": 0,
        "timezone_str": "Invalid/Timezone_That_Does_Not_Exist",
        "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "New Delhi", "country": "India"
    }
    response = client.post("/api/v1/birth-profile", json=payload, headers=headers)
    assert response.status_code == 400
    data = response.json()

    assert "detail" in data
    assert "error_code" in data
    assert "timestamp_iso" in data
