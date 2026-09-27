import pytest
from apps.api.engines.report_engine import ReportGeneratorEngine

def test_personalization_differential():
    # User A: Kochi, India (1990-01-15 08:30)
    report_a = ReportGeneratorEngine.generate_comprehensive_report(
        name="User A",
        year=1990,
        month=1,
        day=15,
        hour=8,
        minute=30,
        latitude=9.9312,
        longitude=76.2673,
        place_name="Kochi",
        country="India",
        zodiac_system="sidereal",
        ayanamsha="lahiri"
    )

    # User B: London, UK (1985-07-22 18:45)
    report_b = ReportGeneratorEngine.generate_comprehensive_report(
        name="User B",
        year=1985,
        month=7,
        day=22,
        hour=18,
        minute=45,
        latitude=51.5074,
        longitude=-0.1278,
        place_name="London",
        country="United Kingdom",
        zodiac_system="sidereal",
        ayanamsha="lahiri"
    )

    # Assertions for Personalization & Non-Identity
    assert report_a["metadata"]["native_name"] == "User A"
    assert report_b["metadata"]["native_name"] == "User B"

    hash_a = report_a["chapter_12_audit_trail"]["calculation_hash"]
    hash_b = report_b["chapter_12_audit_trail"]["calculation_hash"]

    # Calculation hashes must be different for different birth profiles
    assert hash_a != hash_b

    # Ascendants / Planetary positions must differ
    sun_a = report_a["chapter_3_planetary_positions"]["data"]["Sun"]["sign"]
    sun_b = report_b["chapter_3_planetary_positions"]["data"]["Sun"]["sign"]

    moon_a = report_a["chapter_3_planetary_positions"]["data"]["Moon"]["sign"]
    moon_b = report_b["chapter_3_planetary_positions"]["data"]["Moon"]["sign"]

    # At least one major astrological factor must differ
    assert (sun_a != sun_b) or (moon_a != moon_b) or (hash_a != hash_b)
