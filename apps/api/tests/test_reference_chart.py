import pytest
from apps.api.engines.report_engine import ReportGeneratorEngine

def test_subramanian_ts_reference_chart():
    # Subramanian T S: 28 September 1986, 16:30 IST, Palakkad (10.7867, 76.6548)
    report = ReportGeneratorEngine.generate_comprehensive_report(
        name="Subramanian T S",
        year=1986,
        month=9,
        day=28,
        hour=16,
        minute=30,
        latitude=10.7867,
        longitude=76.6548,
        place_name="Palakkad",
        country="India",
        zodiac_system="sidereal",
        ayanamsha="lahiri"
    )

    assert report["metadata"]["native_name"] == "Subramanian T S"
    assert "chapter_3_planetary_positions" in report
    positions = report["chapter_3_planetary_positions"]["data"]

    # Verify core grahas are present and calculated
    assert "Sun" in positions
    assert "Moon" in positions
    assert "Mars" in positions
    assert "Mercury" in positions
    assert "Jupiter" in positions
    assert "Venus" in positions
    assert "Saturn" in positions
    assert "Rahu" in positions
    assert "Ketu" in positions
