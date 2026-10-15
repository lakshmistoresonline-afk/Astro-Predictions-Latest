"""
Automated Test Suite for Strict Gregorian Date/Time Validation, Leap Years,
Ephemeris Horizon Boundaries, and HTTP Error Responses.
"""
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.time_normalization import normalize_birth_time

client = TestClient(app)

def test_invalid_february_31_raises_value_error():
    """31 February must raise explicit ValueError/ValidationError and never reach calculation engines."""
    with pytest.raises(ValidationError) as exc_info:
        BirthInput(
            name="Invalid Feb 31",
            year=1995, month=2, day=31,
            hour=12, minute=0, second=0,
            timezone_str="Asia/Kolkata",
            latitude=28.6139, longitude=77.2090
        )
    assert "maximum allowed days in month: 28" in str(exc_info.value)

def test_non_leap_year_february_29_raises_value_error():
    """29 February in non-leap year 2025 must raise explicit validation error."""
    with pytest.raises(ValidationError) as exc_info:
        BirthInput(
            name="Non-leap Feb 29",
            year=2025, month=2, day=29,
            hour=12, minute=0, second=0,
            timezone_str="Asia/Kolkata",
            latitude=28.6139, longitude=77.2090
        )
    assert "maximum allowed days in month: 28" in str(exc_info.value)

def test_leap_year_february_29_is_valid():
    """29 February in leap year 2024 and 2000 must pass validation successfully."""
    inp_2024 = BirthInput(
        name="Leap Year 2024",
        year=2024, month=2, day=29,
        hour=12, minute=0, second=0,
        timezone_str="Asia/Kolkata",
        latitude=28.6139, longitude=77.2090
    )
    norm = normalize_birth_time(inp_2024)
    assert norm.utc_datetime_iso is not None

    inp_2000 = BirthInput(
        name="Leap Year 2000",
        year=2000, month=2, day=29,
        hour=12, minute=0, second=0,
        timezone_str="Asia/Kolkata",
        latitude=28.6139, longitude=77.2090
    )
    norm_2000 = normalize_birth_time(inp_2000)
    assert norm_2000.utc_datetime_iso is not None

def test_ephemeris_horizon_boundary_validation():
    """Birth year outside 1850-2150 horizon or past 2150-01-22 boundary must raise validation error."""
    with pytest.raises(ValidationError) as exc_1849:
        BirthInput(
            name="Too Early",
            year=1849, month=12, day=31,
            hour=12, minute=0, second=0,
            timezone_str="Asia/Kolkata",
            latitude=28.6139, longitude=77.2090
        )
    assert "supported ephemeris horizon" in str(exc_1849.value)

    with pytest.raises(ValidationError) as exc_2151:
        BirthInput(
            name="Too Late",
            year=2151, month=1, day=1,
            hour=12, minute=0, second=0,
            timezone_str="Asia/Kolkata",
            latitude=28.6139, longitude=77.2090
        )
    assert "supported ephemeris horizon" in str(exc_2151.value)

def test_api_endpoint_invalid_date_http_400():
    """API endpoint /api/v1/birth-profile must return HTTP 400 for invalid dates."""
    payload = {
        "name": "Invalid Date Test",
        "year": 1995, "month": 2, "day": 31,
        "hour": 12, "minute": 0, "second": 0,
        "timezone_str": "Asia/Kolkata",
        "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "New Delhi", "country": "India"
    }
    response = client.post("/api/v1/birth-profile", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
