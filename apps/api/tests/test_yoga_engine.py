"""
Comprehensive Unit & Forensic Verification Suite for Authoritative Yoga Evaluator Engine (Phase 2D-R2).
"""
import pytest
from apps.api.engines.vedic import BirthInput, build_canonical_vedic_chart
from apps.api.engines.yogas import YogaEvaluator, casts_aspect


def test_aspect_engine_rules():
    """Verify Parashari house aspect calculations (Conjunctions are NOT aspects)."""
    # 7th house aspect (180° = 6 houses away in 0-based distance)
    assert casts_aspect("Sun", 1, 7) is True
    assert casts_aspect("Sun", 1, 2) is False
    assert casts_aspect("Sun", 1, 1) is False # Conjunction is not an aspect

    # Mars special aspects: 4th, 7th, 8th
    assert casts_aspect("Mars", 1, 4) is True
    assert casts_aspect("Mars", 1, 7) is True
    assert casts_aspect("Mars", 1, 8) is True
    assert casts_aspect("Mars", 1, 5) is False
    assert casts_aspect("Mars", 1, 1) is False

    # Jupiter special aspects: 5th, 7th, 9th
    assert casts_aspect("Jupiter", 1, 5) is True
    assert casts_aspect("Jupiter", 1, 7) is True
    assert casts_aspect("Jupiter", 1, 9) is True
    assert casts_aspect("Jupiter", 1, 4) is False
    assert casts_aspect("Jupiter", 1, 1) is False

    # Saturn special aspects: 3rd, 7th, 10th
    assert casts_aspect("Saturn", 1, 3) is True
    assert casts_aspect("Saturn", 1, 7) is True
    assert casts_aspect("Saturn", 1, 10) is True
    assert casts_aspect("Saturn", 1, 4) is False
    assert casts_aspect("Saturn", 1, 1) is False


def test_canonical_subramanian_t_s_yogas():
    """Verify Yoga detection for canonical Subramanian T S chart."""
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    canonical_chart = build_canonical_vedic_chart(inp)
    yoga_suite = YogaEvaluator.evaluate_all_yogas(canonical_chart)

    assert len(yoga_suite.all_evaluated_yogas) >= 15
    assert yoga_suite.rule_set_version == "yoga_rules_v1"
    assert len(yoga_suite.summary_counts) > 0

    # Verify Budha Aditya Yoga in Subramanian T S chart
    # Note: In Phase 2A canonical chart, Sun is ~161.54 deg, Mercury is ~178.28 deg
    # Their orb is ~16.74 degrees. Since 16.74 > 12.0, Budha Aditya is NOT_DETECTED in this specific chart.
    budha_aditya = next((y for y in yoga_suite.all_evaluated_yogas if y.rule_id == "YOGA_BUDHA_ADITYA"), None)
    assert budha_aditya is not None
    assert budha_aditya.status == "NOT_DETECTED"
    assert budha_aditya.conditions[0].evidence_details["orb_deg"] > 12.0


def test_20_independent_birth_charts_yoga_suite():
    """
    Test suite evaluating 20 independent birth charts across all supported Yogas.
    """
    test_cases = [
        {"name": "Palakkad", "year": 1986, "month": 9, "day": 28, "hour": 16, "minute": 30, "tz": "Asia/Kolkata", "lat": 10.7867, "lon": 76.6548},
        {"name": "Kochi", "year": 1990, "month": 1, "day": 15, "hour": 8, "minute": 30, "tz": "Asia/Kolkata", "lat": 9.9312, "lon": 76.2673},
        {"name": "London", "year": 1985, "month": 7, "day": 22, "hour": 18, "minute": 45, "tz": "Europe/London", "lat": 51.5074, "lon": -0.1278},
        {"name": "Greenwich", "year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0, "tz": "UTC", "lat": 51.4769, "lon": 0.0005},
        {"name": "New York", "year": 2026, "month": 9, "day": 27, "hour": 12, "minute": 0, "tz": "America/New_York", "lat": 40.7128, "lon": -74.0060},
        {"name": "Tokyo", "year": 2050, "month": 1, "day": 1, "hour": 12, "minute": 0, "tz": "Asia/Tokyo", "lat": 35.6762, "lon": 139.6503},
        {"name": "Paris", "year": 1950, "month": 6, "day": 15, "hour": 12, "minute": 0, "tz": "Europe/Paris", "lat": 48.8566, "lon": 2.3522},
        {"name": "Sydney", "year": 1995, "month": 12, "day": 25, "hour": 12, "minute": 0, "tz": "Australia/Sydney", "lat": -33.8688, "lon": 151.2093},
        {"name": "Singapore", "year": 2010, "month": 3, "day": 20, "hour": 12, "minute": 0, "tz": "Asia/Singapore", "lat": 1.3521, "lon": 103.8198},
        {"name": "Reykjavik", "year": 2015, "month": 6, "day": 21, "hour": 12, "minute": 0, "tz": "Atlantic/Reykjavik", "lat": 64.1466, "lon": -21.9426},
        {"name": "Mumbai", "year": 1975, "month": 3, "day": 10, "hour": 10, "minute": 15, "tz": "Asia/Kolkata", "lat": 19.0760, "lon": 72.8777},
        {"name": "Delhi", "year": 1980, "month": 11, "day": 5, "hour": 14, "minute": 20, "tz": "Asia/Kolkata", "lat": 28.6139, "lon": 77.2090},
        {"name": "San Francisco", "year": 1992, "month": 8, "day": 18, "hour": 21, "minute": 10, "tz": "America/Los_Angeles", "lat": 37.7749, "lon": -122.4194},
        {"name": "Berlin", "year": 1968, "month": 4, "day": 12, "hour": 6, "minute": 45, "tz": "Europe/Berlin", "lat": 52.5200, "lon": 13.4050},
        {"name": "Rome", "year": 1988, "month": 2, "day": 28, "hour": 11, "minute": 30, "tz": "Europe/Rome", "lat": 41.9028, "lon": 12.4964},
        {"name": "Cairo", "year": 2005, "month": 10, "day": 14, "hour": 15, "minute": 0, "tz": "Africa/Cairo", "lat": 30.0444, "lon": 31.2357},
        {"name": "Bangkok", "year": 2002, "month": 5, "day": 9, "hour": 7, "minute": 50, "tz": "Asia/Bangkok", "lat": 13.7563, "lon": 100.5018},
        {"name": "Buenos Aires", "year": 1978, "month": 12, "day": 1, "hour": 19, "minute": 25, "tz": "America/Argentina/Buenos_Aires", "lat": -34.6037, "lon": -58.3816},
        {"name": "Cape Town", "year": 1998, "month": 9, "day": 3, "hour": 4, "minute": 15, "tz": "Africa/Johannesburg", "lat": -33.9249, "lon": 18.4241},
        {"name": "Auckland", "year": 2012, "month": 11, "day": 20, "hour": 16, "minute": 40, "tz": "Pacific/Auckland", "lat": -36.8485, "lon": 174.7633},
    ]

    for tc in test_cases:
        inp = BirthInput(
            name=tc["name"], year=tc["year"], month=tc["month"], day=tc["day"],
            hour=tc["hour"], minute=tc["minute"], second=0, timezone_str=tc["tz"],
            latitude=tc["lat"], longitude=tc["lon"]
        )
        chart = build_canonical_vedic_chart(inp)
        yoga_suite = YogaEvaluator.evaluate_all_yogas(chart)

        assert len(yoga_suite.all_evaluated_yogas) >= 15
        assert yoga_suite.summary_counts["total_evaluated"] >= 15


def test_partial_chart_indeterminate_status():
    """Verify that a partial chart missing required planets resolves to INDETERMINATE."""
    inp = BirthInput(
        name="Test Missing Moon",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    canonical_chart = build_canonical_vedic_chart(inp)

    # Intentionally remove the Moon to simulate partial evidence
    del canonical_chart.placements["Moon"]

    yoga_suite = YogaEvaluator.evaluate_all_yogas(canonical_chart)

    # Gaja Kesari requires Moon. Should be INDETERMINATE.
    gaja_kesari = next(y for y in yoga_suite.all_evaluated_yogas if y.rule_id == "YOGA_GAJA_KESARI")
    assert gaja_kesari.status == "INDETERMINATE"

    # Chandra Yogas (Sunapha, Anapha, Durudhara) require Moon. Should be INDETERMINATE.
    chandra_yogas = [y for y in yoga_suite.all_evaluated_yogas if y.category == "Chandra"]
    for y in chandra_yogas:
        assert y.status == "INDETERMINATE"
