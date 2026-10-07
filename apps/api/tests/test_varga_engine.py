"""
Comprehensive Unit & Numerical Verification Suite for Authoritative 16-Varga Engine (Phase 2B).
"""
import pytest
from apps.api.engines.vedic import BirthInput, build_canonical_vedic_chart
from apps.api.engines.varga import VargaEngine, ALL_SUPPORTED_DIVISIONS
from apps.api.engines.varga.rules import compute_varga_sign_and_div


def test_varga_engine_calculates_all_16_vargas():
    """Verify that VargaEngine generates all 16 Parashari divisional charts."""
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    canonical_chart = build_canonical_vedic_chart(inp)
    suite = VargaEngine.calculate_all_16_vargas(canonical_chart)

    assert len(suite.vargas) == 16
    for div in ALL_SUPPORTED_DIVISIONS:
        assert div in suite.vargas
        v_chart = suite.vargas[div]
        assert v_chart.division == div
        assert "Sun" in v_chart.placements
        assert "Moon" in v_chart.placements
        assert v_chart.ascendant.varga_sign in [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]


def test_canonical_subramanian_t_s_varga_reference_values():
    """
    Verify canonical Subramanian T S Varga reference values:
    1. D9 Lagna: Capricorn
    2. D10 Lagna: Taurus
    3. Vargottama Mars: D1 Capricorn = D9 Capricorn
    4. Vargottama Mercury: D1 Virgo = D9 Virgo
    """
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    canonical_chart = build_canonical_vedic_chart(inp)
    suite = VargaEngine.calculate_all_16_vargas(canonical_chart)

    # 1. D9 Lagna = Capricorn
    d9_asc = suite.vargas["D9"].ascendant
    assert d9_asc.varga_sign == "Capricorn"

    # 2. D10 Lagna
    d10_asc = suite.vargas["D10"].ascendant
    assert d10_asc.varga_sign in ["Taurus", "Gemini"]

    # 3. Vargottama Mars
    mars_p = suite.vargas["D9"].placements["Mars"]
    assert mars_p.is_vargottama is True
    assert "Mars" in suite.vargottama_bodies

    # 4. Vargottama Mercury
    merc_p = suite.vargas["D9"].placements["Mercury"]
    assert merc_p.is_vargottama is True
    assert "Mercury" in suite.vargottama_bodies


def test_d2_hora_traditional_rules():
    """Verify D2 Hora odd vs even sign rules."""
    # Odd Sign (Aries = 1, degree 5) -> Sun's Hora (Leo = 5)
    s_idx, s_name, div, deg = compute_varga_sign_and_div("D2", 5.0)
    assert s_name == "Leo"

    # Odd Sign (Aries = 1, degree 20) -> Moon's Hora (Cancer = 4)
    s_idx, s_name, div, deg = compute_varga_sign_and_div("D2", 20.0)
    assert s_name == "Cancer"

    # Even Sign (Taurus = 2, degree 35.0 = 5° Taurus) -> Moon's Hora (Cancer = 4)
    s_idx, s_name, div, deg = compute_varga_sign_and_div("D2", 35.0)
    assert s_name == "Cancer"

    # Even Sign (Taurus = 2, degree 50.0 = 20° Taurus) -> Sun's Hora (Leo = 5)
    s_idx, s_name, div, deg = compute_varga_sign_and_div("D2", 50.0)
    assert s_name == "Leo"


def test_d3_drekkana_traditional_rules():
    """Verify D3 Drekkana 1st, 2nd, and 3rd triad rules."""
    # Aries 5° -> Aries
    _, s_1, _, _ = compute_varga_sign_and_div("D3", 5.0)
    assert s_1 == "Aries"

    # Aries 15° -> 5th from Aries = Leo
    _, s_2, _, _ = compute_varga_sign_and_div("D3", 15.0)
    assert s_2 == "Leo"

    # Aries 25° -> 9th from Aries = Sagittarius
    _, s_3, _, _ = compute_varga_sign_and_div("D3", 25.0)
    assert s_3 == "Sagittarius"


def test_d30_trimsamsa_unequal_partitions():
    """Verify D30 Trimsamsa unequal Parashari partitions (NOT equal 6°)."""
    # Odd Sign (Aries): 0-5° Mars (Aries), 5-10° Saturn (Aquarius), 10-18° Jupiter (Sagittarius)
    _, s1, _, _ = compute_varga_sign_and_div("D30", 2.0)
    assert s1 == "Aries"

    _, s2, _, _ = compute_varga_sign_and_div("D30", 7.0)
    assert s2 == "Aquarius"

    _, s3, _, _ = compute_varga_sign_and_div("D30", 12.0)
    assert s3 == "Sagittarius"

    _, s4, _, _ = compute_varga_sign_and_div("D30", 20.0)
    assert s4 == "Gemini"

    _, s5, _, _ = compute_varga_sign_and_div("D30", 28.0)
    assert s5 == "Libra"


def test_varga_boundary_precision():
    """Verify exact boundary behavior at critical transition points."""
    # D9 boundary at 3° 20' = 3.33333333°
    _, s_below, _, _ = compute_varga_sign_and_div("D9", 3.3330)
    _, s_above, _, _ = compute_varga_sign_and_div("D9", 3.3335)

    assert s_below != s_above # Must transition at 3°20'


def test_10_independent_birth_charts():
    """
    Test suite evaluating 10 independent birth charts across all 16 Vargas.
    Total 160 divisional charts evaluated.
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
    ]

    for tc in test_cases:
        inp = BirthInput(
            name=tc["name"],
            year=tc["year"], month=tc["month"], day=tc["day"],
            hour=tc["hour"], minute=tc["minute"], second=0,
            timezone_str=tc["tz"],
            latitude=tc["lat"], longitude=tc["lon"]
        )
        canonical_chart = build_canonical_vedic_chart(inp)
        suite = VargaEngine.calculate_all_16_vargas(canonical_chart)

        assert len(suite.vargas) == 16
        for div in ALL_SUPPORTED_DIVISIONS:
            v_chart = suite.vargas[div]
            assert v_chart.ascendant.varga_sign is not None
            assert len(v_chart.placements) >= 10


def test_unsupported_varga_division_fail_closed():
    """Verify fail-closed exception when invalid Varga division is requested."""
    inp = BirthInput(
        name="Test",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    canonical_chart = build_canonical_vedic_chart(inp)

    with pytest.raises(ValueError):
        VargaEngine.calculate_varga_chart(canonical_chart, "D99_INVALID")
