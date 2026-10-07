"""
Test Suite for Geocoding Location Search, Tier 2/3 Indian Towns, Global Metros, and Custom Coordinate Validation.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.engines.geocoding_engine import GeocodingEngine

client = TestClient(app)

def test_geocoding_search_india_towns():
    """Geocoding search must find tier-2 and tier-3 Indian towns (e.g. Palakkad, Kochi, Madurai)."""
    results_palakkad = GeocodingEngine.search_location("Palakkad")
    assert len(results_palakkad) > 0
    p = results_palakkad[0]
    assert p["place_name"] == "Palakkad"
    assert p["country"] == "India"
    assert p["timezone_str"] == "Asia/Kolkata"

    results_kochi = GeocodingEngine.search_location("Kochi")
    assert len(results_kochi) > 0
    assert results_kochi[0]["place_name"] == "Kochi"

def test_geocoding_search_global_cities():
    """Geocoding search must find global metropolitan areas with exact IANA timezones."""
    results_london = GeocodingEngine.search_location("London")
    assert len(results_london) > 0
    assert results_london[0]["timezone_str"] == "Europe/London"

    results_tokyo = GeocodingEngine.search_location("Tokyo")
    assert len(results_tokyo) > 0
    assert results_tokyo[0]["timezone_str"] == "Asia/Tokyo"

def test_custom_location_coordinate_validation():
    """GeocodingEngine validates latitude [-90, 90], longitude [-180, 180], and valid IANA timezone string."""
    assert GeocodingEngine.validate_coordinates_and_timezone(28.6139, 77.2090, "Asia/Kolkata") is True
    assert GeocodingEngine.validate_coordinates_and_timezone(51.5074, -0.1278, "Europe/London") is True

    # Invalid latitude > 90
    assert GeocodingEngine.validate_coordinates_and_timezone(195.0, 77.2090, "Asia/Kolkata") is False

    # Invalid timezone string
    assert GeocodingEngine.validate_coordinates_and_timezone(28.6139, 77.2090, "Invalid/Timezone_Key") is False

def test_location_search_api_router_endpoint():
    """GET /api/v1/location/search?query=palakkad returns HTTP 200 with matching location items."""
    response = client.get("/api/v1/location/search?query=palakkad")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["place_name"] == "Palakkad"
    assert data[0]["timezone_str"] == "Asia/Kolkata"

def test_location_validate_api_router_endpoint():
    """POST /api/v1/location/validate validates custom manual coordinates & IANA timezone."""
    payload = {
        "latitude": 10.7867,
        "longitude": 76.6548,
        "timezone_str": "Asia/Kolkata"
    }
    response = client.post("/api/v1/location/validate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True
    assert data["latitude"] == 10.7867
