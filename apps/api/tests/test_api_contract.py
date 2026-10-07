"""
Test Suite for Versioned /api/v1 OpenAPI Contract, Request/Response Schemas, and Structured Error Shapes.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

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
    payload = {
        "name": "John Doe",
        "year": 1995, "month": 1, "day": 1,
        "hour": 12, "minute": 0, "second": 0,
        "timezone_str": "Asia/Kolkata",
        "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "New Delhi", "country": "India",
        "zodiac_system": "sidereal", "ayanamsha": "lahiri"
    }
    response = client.post("/api/v1/birth-profile", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert "birth_input" in data
    assert "master_evidence" in data
    assert "predictions" in data
    assert "svg_chart" in data
    assert "report" in data

    assert data["birth_input"]["timezone_str"] == "Asia/Kolkata"
    assert data["master_evidence"]["master_evidence_hash"] is not None

def test_structured_error_response_shape():
    """Validation errors must return a structured JSON error shape with detail, error_code, and timestamp_iso."""
    payload = {
        "name": "Jane",
        "year": 1995, "month": 1, "day": 1,
        "hour": 12, "minute": 0,
        "timezone_str": "Invalid/Timezone_That_Does_Not_Exist",
        "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "New Delhi", "country": "India"
    }
    response = client.post("/api/v1/birth-profile", json=payload)
    assert response.status_code == 400
    data = response.json()

    assert "detail" in data
    assert "error_code" in data
    assert "timestamp_iso" in data
    assert data["error_code"] in ["VALIDATION_ERROR", "HTTP_ERROR_400"]
