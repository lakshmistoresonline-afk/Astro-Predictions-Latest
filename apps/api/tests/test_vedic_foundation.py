"""
Comprehensive Unit & Numerical Verification Suite for Canonical Vedic Engine Foundation (Phase 2A).
"""
import pytest
from pydantic import ValidationError
from apps.api.engines.vedic import (
    BirthInput,
    build_canonical_vedic_chart,
    normalize_birth_time,
    calculate_rashi,
    calculate_nakshatra_pada,
    generate_whole_sign_houses,
    InvalidBirthDataError,
    TimezoneResolutionError,
    OutOfBoundaryError
)
from apps.api.engines.astronomy.exceptions import KernelNotFoundError


def test_time_normalization_and_julian_date():
    """Verify local civil time to UTC and Julian Date normalization."""
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    time_norm = normalize_birth_time(inp)

    assert time_norm.utc_datetime_iso.startswith("1986-09-28T11:00:00")
    assert time_norm.utc_offset_hours == 5.5
    assert abs(time_norm.julian_day_tt - 2446701.958333) < 0.001


def test_invalid_timezone_fail_closed():
    """Verify fail-closed behavior on unknown or invalid timezone."""
    with pytest.raises((TimezoneResolutionError, ValidationError, ValueError)):
        inp = BirthInput(
            name="Invalid TZ",
            year=1990, month=1, day=15,
            hour=8, minute=30, second=0,
            timezone_str="Invalid/Unknown_Zone_123",
            latitude=10.0, longitude=76.0
        )
        normalize_birth_time(inp)


def test_invalid_coordinates_fail_closed():
    """Verify fail-closed validation on invalid physical coordinates."""
    with pytest.raises((ValidationError, ValueError)):
        BirthInput(
            name="Invalid Lat",
            year=1990, month=1, day=15,
            hour=8, minute=30, second=0,
            timezone_str="Asia/Kolkata",
            latitude=105.0, # invalid
            longitude=76.0
        )


def test_boundary_dates_pass_and_out_of_boundary_fail_closed():
    """Verify that dates within 1850 - 2150 pass and outside dates fail closed."""
    # Min boundary date 1850-01-01
    inp_min = BirthInput(
        name="Min Date",
        year=1850, month=1, day=1,
        hour=12, minute=0, second=0,
        timezone_str="UTC",
        latitude=51.5, longitude=0.0
    )
    time_min = normalize_birth_time(inp_min)
    assert time_min.utc_datetime_iso.startswith("1850-01-01")

    # Max boundary date 2150-01-20
    inp_max = BirthInput(
        name="Max Date",
        year=2150, month=1, day=20,
        hour=12, minute=0, second=0,
        timezone_str="UTC",
        latitude=51.5, longitude=0.0
    )
    time_max = normalize_birth_time(inp_max)
    assert time_max.utc_datetime_iso.startswith("2150-01-20")

    # Out-of-boundary date 1840-01-01
    with pytest.raises(OutOfBoundaryError):
        inp_before = BirthInput(
            name="Before Min",
            year=1840, month=1, day=1,
            hour=12, minute=0, second=0,
            timezone_str="UTC",
            latitude=51.5, longitude=0.0
        )
        normalize_birth_time(inp_before)


def test_rashi_classification_full_precision():
    """Verify full precision Rashi (Sign, Degree, Minute, Second) calculation."""
    rashi = calculate_rashi(97.2052)
    assert rashi.sign == "Cancer"
    assert rashi.sign_index == 4
    assert rashi.degree == 7
    assert rashi.minute == 12
    assert 18.0 <= rashi.second <= 19.5


def test_nakshatra_pada_classification():
    """Verify full precision Nakshatra and Pada calculation."""
    nak_pada = calculate_nakshatra_pada(97.2052)
    assert nak_pada.nakshatra == "Pushya"
    assert nak_pada.nakshatra_index == 8
    assert nak_pada.pada == 2


def test_canonical_subramanian_t_s_chart():
    """Verify canonical Subramanian T S chart calculation against reference values."""
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    chart = build_canonical_vedic_chart(inp)

    # 1. Ascendant: Aquarius
    assert chart.ascendant.sign == "Aquarius"
    assert chart.ascendant.degree in [11, 12]

    # 2. MC: Scorpio
    assert chart.mc.sign == "Scorpio"
    assert chart.mc.degree in [16, 17]

    # 3. Moon: Cancer 07° 12', Pushya Pada 2
    moon_placement = chart.placements["Moon"]
    assert moon_placement.rashi.sign == "Cancer"
    assert moon_placement.rashi.degree == 7
    assert moon_placement.nakshatra_pada.nakshatra == "Pushya"
    assert moon_placement.nakshatra_pada.pada == 2

    # 4. Sun: Virgo
    sun_placement = chart.placements["Sun"]
    assert sun_placement.rashi.sign == "Virgo"

    # 5. Whole Sign Houses
    assert len(chart.whole_sign_houses) == 12
    assert chart.whole_sign_houses[0].sign == "Aquarius"
    assert chart.whole_sign_houses[1].sign == "Pisces"
    assert chart.whole_sign_houses[11].sign == "Capricorn"

    # 6. Hash
    assert len(chart.calculation_hash) == 64


def test_differential_personalization_user_a_vs_user_b():
    """
    Verify Part 14 Personalization:
    User A: 1990-01-15 08:30 IST, Kochi
    User B: 1985-07-22 18:45 BST, London
    Must produce different JDs, planetary longitudes, Moon, Ascendants, Nakshatras, and SHA-256 hashes.
    """
    user_a_inp = BirthInput(
        name="User A Kochi",
        year=1990, month=1, day=15,
        hour=8, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=9.9312, longitude=76.2673
    )
    user_b_inp = BirthInput(
        name="User B London",
        year=1985, month=7, day=22,
        hour=18, minute=45, second=0,
        timezone_str="Europe/London",
        latitude=51.5074, longitude=-0.1278
    )

    chart_a = build_canonical_vedic_chart(user_a_inp)
    chart_b = build_canonical_vedic_chart(user_b_inp)

    assert chart_a.time_normalization.julian_day_tt != chart_b.time_normalization.julian_day_tt
    assert chart_a.ascendant.absolute_longitude != chart_b.ascendant.absolute_longitude
    assert chart_a.placements["Moon"].sidereal_longitude != chart_b.placements["Moon"].sidereal_longitude
    assert chart_a.placements["Moon"].nakshatra_pada.nakshatra != chart_b.placements["Moon"].nakshatra_pada.nakshatra
    assert chart_a.calculation_hash != chart_b.calculation_hash
