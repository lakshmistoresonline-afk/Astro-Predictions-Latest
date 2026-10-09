"""
Test Suite for Structured API Error Handling, HTTP Status Code Mapping, and Request Correlation IDs.
"""
import os
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.config import settings

client = TestClient(app)

def test_request_correlation_id_middleware_attaches_header():
    """X-Request-ID header must be returned on every response."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"].startswith("req_")

def test_custom_request_correlation_id_preserved():
    """Caller-supplied X-Request-ID must be preserved in response headers and error objects."""
    custom_id = "req_custom_trace_99999"
    response = client.get("/health", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == custom_id

def test_validation_error_http_400():
    """Invalid timezone string must return HTTP 400 with VALIDATION_ERROR or TIMEZONE_ERROR code."""
    payload = {
        "name": "Jane",
        "year": 1995, "month": 1, "day": 1,
        "hour": 12, "minute": 0,
        "timezone_str": "Invalid/Timezone_Name",
        "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "New Delhi", "country": "India"
    }
    response = client.post("/api/v1/birth-profile", json=payload, headers={"X-Request-ID": "req_val_001"})
    assert response.status_code == 400
    data = response.json()

    assert data["request_id"] == "req_val_001"
    assert "error_code" in data
    assert data["error_code"] in ["TIMEZONE_ERROR", "VALIDATION_ERROR", "HTTP_ERROR_400"]
    assert "timestamp_iso" in data

def test_out_of_range_coordinate_validation_error():
    """Latitude out of range [-90, 90] must return HTTP 400 validation error."""
    payload = {
        "name": "Jane",
        "year": 1995, "month": 1, "day": 1,
        "hour": 12, "minute": 0,
        "timezone_str": "Asia/Kolkata",
        "latitude": 195.0, "longitude": 77.2090,
        "place_name": "Invalid", "country": "India"
    }
    response = client.post("/api/v1/birth-profile", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] in ["VALIDATION_ERROR", "HTTP_ERROR_400"]

def test_admin_authentication_unauthorized_401():
    """Missing admin credentials must return HTTP 401 Unauthorized."""
    response = client.get("/api/v1/admin/stats", headers={"X-Request-ID": "req_auth_001"})
    assert response.status_code == 401
    data = response.json()

    assert data["request_id"] == "req_auth_001"
    assert "Missing administrative credentials" in data["detail"]
    assert "timestamp_iso" in data

def test_admin_authorization_forbidden_403():
    """Invalid admin key must return HTTP 403 Forbidden."""
    os.environ["ADMIN_API_KEY"] = "valid_admin_secret_key_12345"
    response = client.get("/api/v1/admin/stats", headers={"X-Admin-Key": "wrong_key", "X-Request-ID": "req_auth_002"})
    assert response.status_code == 403
    data = response.json()

    assert data["request_id"] == "req_auth_002"
    assert "Invalid administrative key" in data["detail"]

def test_resource_not_found_404():
    """Non-existent birth profile ID query must return HTTP 404 Not Found."""
    reg = client.post("/api/v1/auth/register", json={"email": "notfound_user@test.com", "password": "Password123!", "full_name": "NF User"})
    if reg.status_code == 201:
        tok = reg.json()["access_token"]
    else:
        tok = client.post("/api/v1/auth/login", json={"email": "notfound_user@test.com", "password": "Password123!"}).json()["access_token"]

    response = client.get("/api/v1/profiles/non_existent_profile_id_999", headers={"Authorization": f"Bearer {tok}", "X-Request-ID": "req_404_001"})
    assert response.status_code == 404
    data = response.json()

    assert data["request_id"] == "req_404_001"
    assert "not found or access denied" in data["detail"]

def test_unsupported_ai_domain_validation_400():
    """Unsupported prediction domain request must return HTTP 400 validation error."""
    payload = {
        "birth_input": {
            "name": "Jane",
            "year": 1995, "month": 1, "day": 1,
            "hour": 12, "minute": 0,
            "timezone_str": "Asia/Kolkata",
            "latitude": 28.6139, "longitude": 77.2090,
            "place_name": "New Delhi", "country": "India"
        },
        "prompt": "Explain domain",
        "domain": "UNSUPPORTED_INVALID_DOMAIN"
    }
    response = client.post("/api/v1/interpret-evidence", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "Unsupported domain" in data["detail"]
