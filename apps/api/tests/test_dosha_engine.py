"""
Comprehensive Unit & Forensic Verification Suite for Authoritative Dosha Evaluator Engine (Phase 2D).
"""
import pytest
from apps.api.engines.vedic import BirthInput, build_canonical_vedic_chart
from apps.api.engines.doshas import DoshaEvaluator


def test_canonical_subramanian_t_s_doshas():
    """Verify Dosha detection for canonical Subramanian T S chart."""
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    canonical_chart = build_canonical_vedic_chart(inp)
    dosha_suite = DoshaEvaluator.evaluate_all_doshas(canonical_chart)

    assert len(dosha_suite.all_evaluated_doshas) == 3
    assert dosha_suite.rule_set_version == "dosha_rules_v1"

    # Check status values are valid
    for d in dosha_suite.all_evaluated_doshas:
        assert d.status in ["DETECTED", "NOT_DETECTED", "CANCELLED", "INDETERMINATE"]


def test_20_independent_birth_charts_dosha_suite():
    """
    Test suite evaluating 20 independent birth charts across all supported Doshas.
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
        dosha_suite = DoshaEvaluator.evaluate_all_doshas(chart)

        assert len(dosha_suite.all_evaluated_doshas) == 3
        assert "manglik_status" in dosha_suite.summary_counts
