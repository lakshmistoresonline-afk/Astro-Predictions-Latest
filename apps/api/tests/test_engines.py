from apps.api.engines.dasha_engine import DashaEngine
from apps.api.engines.yoga_engine import YogaEngine
from apps.api.engines.vedic import BirthInput

def test_dasha_calculation():
    dasha = DashaEngine.calculate_vimshottari_dasha("1990-05-15", "Rohini", 1)
    assert "current_mahadasha" in dasha
    assert len(dasha["all_mahadashas"]) == 9

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
