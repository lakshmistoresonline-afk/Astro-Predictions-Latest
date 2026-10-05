from apps.api.engines.dasha_engine import DashaEngine
from apps.api.engines.yoga_engine import YogaEngine
from apps.api.engines.vedic import BirthInput

def test_dasha_calculation():
    dasha = DashaEngine.calculate_vimshottari_dasha(
        birth_date_str="1990-05-15",
        hour=12,
        minute=0,
        latitude=28.6139,
        longitude=77.2090,
        timezone_str="Asia/Kolkata",
        moon_nakshatra="Rohini",
        nakshatra_pada=1
    )
    assert "current_mahadasha" in dasha
    assert "mahadasha_periods" in dasha

def test_yoga_detection():
    inp = BirthInput(
        name="Paris Historical",
        year=1950, month=6, day=15,
        hour=12, minute=0, second=0,
        timezone_str="Europe/Paris",
        latitude=48.8566, longitude=2.3522
    )
    yogas = YogaEngine.detect_yogas({}, birth_input=inp)
    assert len(yogas) >= 1
    assert any("GAJA" in y["id"].upper() or "GAJA" in y["name"].upper() for y in yogas)
