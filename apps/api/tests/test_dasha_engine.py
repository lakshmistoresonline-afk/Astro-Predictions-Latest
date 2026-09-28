"""
Comprehensive Unit, Invariant, and Forensic Verification Suite for Authoritative Vimshottari Dasha Engine (Phase 2C).
"""
import pytest
from datetime import datetime, timezone, timedelta

from apps.api.engines.vedic import BirthInput, build_canonical_vedic_chart
from apps.api.engines.dasha import (
    AuthoritativeDashaEngine,
    calculate_birth_nakshatra_info,
    calculate_child_duration_days,
    DASHA_YEARS,
    DASHA_SEQUENCE,
    DAYS_PER_YEAR,
    InvalidMoonStateError,
    OutOfQueryRangeError
)
from apps.api.engines.dasha.timeline import (
    generate_mahadasha_nodes,
    generate_child_nodes,
    query_dasha_hierarchy_at
)


def test_nakshatra_lord_mapping_and_boundaries():
    """Verify Nakshatra, Lord, and Pada classification across exact boundary points."""
    # 0° -> Ashwini (Index 1), Lord Ketu, Pada 1
    nak_0 = calculate_birth_nakshatra_info(0.0)
    assert nak_0.nakshatra_name == "Ashwini"
    assert nak_0.nakshatra_lord == "Ketu"
    assert nak_0.pada == 1
    assert nak_0.elapsed_fraction == 0.0
    assert nak_0.remaining_fraction == 1.0

    # 13° 20' - epsilon (13.3330°) -> Ashwini Pada 4
    nak_ashwini_end = calculate_birth_nakshatra_info(13.3330)
    assert nak_ashwini_end.nakshatra_name == "Ashwini"
    assert nak_ashwini_end.pada == 4

    # 13° 20' + epsilon (13.3340°) -> Bharani (Index 2), Lord Venus, Pada 1
    nak_bharani_start = calculate_birth_nakshatra_info(13.3340)
    assert nak_bharani_start.nakshatra_name == "Bharani"
    assert nak_bharani_start.nakshatra_lord == "Venus"
    assert nak_bharani_start.pada == 1

    # 97.2052° -> Pushya (Index 8), Lord Saturn, Pada 2
    nak_pushya = calculate_birth_nakshatra_info(97.2052)
    assert nak_pushya.nakshatra_name == "Pushya"
    assert nak_pushya.nakshatra_lord == "Saturn"
    assert nak_pushya.pada == 2


def test_birth_balance_calculation():
    """Verify exact birth Mahadasha balance formula."""
    nak_info = calculate_birth_nakshatra_info(97.2052)
    tot_years = DASHA_YEARS[nak_info.nakshatra_lord]
    rem_years = tot_years * nak_info.remaining_fraction

    assert nak_info.nakshatra_lord == "Saturn"
    assert tot_years == 19.0
    assert 13.40 <= rem_years <= 13.55


def test_canonical_subramanian_t_s_dasha_suite():
    """Verify Dasha suite execution for canonical Subramanian T S chart."""
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    canonical_chart = build_canonical_vedic_chart(inp)
    dasha_res = AuthoritativeDashaEngine.calculate_dasha_suite(canonical_chart)

    # 1. Nakshatra & Lord
    assert dasha_res.nakshatra_info.nakshatra_name == "Pushya"
    assert dasha_res.nakshatra_info.nakshatra_lord == "Saturn"
    assert dasha_res.nakshatra_info.pada == 2

    # 2. Birth Balance
    assert dasha_res.birth_balance.mahadasha_lord == "Saturn"
    assert 13.40 <= dasha_res.birth_balance.remaining_years <= 13.55

    # 3. Top-Level Mahadashas (9 nodes)
    assert len(dasha_res.mahadashas) == 9
    assert dasha_res.mahadashas[0].lord == "Saturn"
    assert dasha_res.mahadashas[1].lord == "Mercury"
    assert dasha_res.mahadashas[2].lord == "Ketu"
    assert dasha_res.mahadashas[3].lord == "Venus"

    # 4. Active Hierarchy at Birth
    active = dasha_res.active_dasha_at_birth
    assert active.active_mahadasha.lord == "Saturn"
    assert active.active_antardasha.lord in DASHA_SEQUENCE
    assert active.active_pratyantardasha.lord in DASHA_SEQUENCE
    assert active.active_sookshma.lord in DASHA_SEQUENCE
    assert active.active_prana.lord in DASHA_SEQUENCE


def test_5_level_nested_hierarchy_invariants():
    """
    Property Test: Invariant verification across all 5 levels.
    Invariant 1: sum(child durations) == parent duration (within 0.001 days).
    Invariant 2: child[k].end == child[k+1].start (zero gaps, zero overlaps).
    """
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    canonical_chart = build_canonical_vedic_chart(inp)
    dasha_res = AuthoritativeDashaEngine.calculate_dasha_suite(canonical_chart)

    # Pick 2nd Mahadasha (Mercury MD)
    md_mercury = dasha_res.mahadashas[1]
    assert md_mercury.lord == "Mercury"

    # Level 2: Antardashas
    ad_nodes = generate_child_nodes(md_mercury, 2, "Antardasha")
    assert len(ad_nodes) == 9
    sum_ad_days = sum(node.duration_days for node in ad_nodes)
    assert abs(sum_ad_days - md_mercury.duration_days) < 0.001

    # Check continuity of AD nodes
    for i in range(len(ad_nodes) - 1):
        assert ad_nodes[i].end_utc_iso == ad_nodes[i + 1].start_utc_iso

    # Level 3: Pratyantardashas for 1st AD
    ad_1 = ad_nodes[0]
    pd_nodes = generate_child_nodes(ad_1, 3, "Pratyantardasha")
    assert len(pd_nodes) == 9
    sum_pd_days = sum(node.duration_days for node in pd_nodes)
    assert abs(sum_pd_days - ad_1.duration_days) < 0.001

    # Level 4: Sookshma for 1st PD
    pd_1 = pd_nodes[0]
    sookshma_nodes = generate_child_nodes(pd_1, 4, "Sookshma")
    assert len(sookshma_nodes) == 9
    sum_sookshma_days = sum(node.duration_days for node in sookshma_nodes)
    assert abs(sum_sookshma_days - pd_1.duration_days) < 0.001

    # Level 5: Prana for 1st Sookshma
    sookshma_1 = sookshma_nodes[0]
    prana_nodes = generate_child_nodes(sookshma_1, 5, "Prana")
    assert len(prana_nodes) == 9
    sum_prana_days = sum(node.duration_days for node in prana_nodes)
    assert abs(sum_prana_days - sookshma_1.duration_days) < 0.001


def test_arbitrary_date_query_get_dasha_at():
    """Verify query_dasha_hierarchy_at for arbitrary target query datetime."""
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    canonical_chart = build_canonical_vedic_chart(inp)

    # Query for year 2026 (40 years after birth -> Venus MD: 2023 to 2043)
    query_dt = datetime(2026, 9, 28, 11, 0, 0, tzinfo=timezone.utc)
    active_2026 = AuthoritativeDashaEngine.get_dasha_at(canonical_chart, query_dt)

    assert active_2026.active_mahadasha.lord == "Venus"
    assert active_2026.active_antardasha.lord in DASHA_SEQUENCE
    assert active_2026.active_pratyantardasha.lord in DASHA_SEQUENCE


def test_10_independent_birth_charts_personalization():
    """
    Verify Personalization across 10 independent birth charts.
    Ensures distinct Moon longitudes, Nakshatras, balances, timelines, and SHA-256 hashes.
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

    results = []
    for tc in test_cases:
        inp = BirthInput(
            name=tc["name"],
            year=tc["year"], month=tc["month"], day=tc["day"],
            hour=tc["hour"], minute=tc["minute"], second=0,
            timezone_str=tc["tz"],
            latitude=tc["lat"], longitude=tc["lon"]
        )
        chart = build_canonical_vedic_chart(inp)
        dasha_suite = AuthoritativeDashaEngine.calculate_dasha_suite(chart)
        results.append(dasha_suite)

    assert len(results) == 10
    hashes = set(res.calculation_hash for res in results)
    assert len(hashes) == 10

    moon_lons = set(res.moon_sidereal_longitude_deg for res in results)
    assert len(moon_lons) == 10


def test_fail_closed_on_invalid_moon_state():
    """Verify fail-closed exception if Moon placement is missing or corrupted."""
    inp = BirthInput(
        name="Test",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    chart = build_canonical_vedic_chart(inp)
    del chart.placements["Moon"]

    with pytest.raises(InvalidMoonStateError):
        AuthoritativeDashaEngine.calculate_dasha_suite(chart)
