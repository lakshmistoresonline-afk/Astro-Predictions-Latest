import pytest
from apps.api.engines.birth_engine import BirthDataEngine
from apps.api.engines.vedic_engine import VedicEngine
from apps.api.engines.dasha_engine import DashaEngine
from apps.api.engines.yoga_engine import YogaEngine

def test_julian_day_calculation():
    # Test JD calculation for Jan 1, 2000, 12:00 UTC
    jd = BirthDataEngine.calculate_julian_day(2000, 1, 1, 12.0)
    assert jd == 2451545.0

def test_birth_data_processing():
    result = BirthDataEngine.process_birth_data(
        name="Test User",
        year=1990,
        month=5,
        day=15,
        hour=10,
        minute=30,
        latitude=28.6139,
        longitude=77.2090,
        place_name="New Delhi",
        country="India"
    )
    assert result["name"] == "Test User"
    assert result["timezone_name"] == "Asia/Kolkata"
    assert "julian_day" in result

def test_nakshatra_calculation():
    # Longitude 15.0 degrees -> Nakshatra index 1 (Bharani)
    info = VedicEngine.get_nakshatra_info(15.0)
    assert "nakshatra" in info
    assert info["pada"] in [1, 2, 3, 4]

def test_dasha_calculation():
    dasha = DashaEngine.calculate_vimshottari_dasha("1990-05-15", "Rohini", 1)
    assert "current_mahadasha" in dasha
    assert len(dasha["all_mahadashas"]) == 9

def test_yoga_detection():
    positions = {
        "Sun": {"sign": "Aries", "longitude": 10.0},
        "Mercury": {"sign": "Aries", "longitude": 15.0}
    }
    yogas = YogaEngine.detect_yogas(positions)
    assert len(yogas) == 1
    assert yogas[0]["id"] == "budha_aditya"
