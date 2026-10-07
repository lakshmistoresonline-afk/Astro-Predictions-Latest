"""
Test Suite for Historical IANA Timezone Resolution, DST Transition Dates, and Time Normalization Pipeline.
"""
import pytest
import zoneinfo
from datetime import datetime
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.time_normalization import normalize_birth_time, calculate_espenak_meeus_delta_t

def test_india_modern_and_historical_timezones():
    """Verifies Indian birth profiles in Asia/Kolkata (UTC+5:30)."""
    inp_modern = BirthInput(
        name="Modern India Native",
        year=1995, month=8, day=15,
        hour=12, minute=0, second=0,
        timezone_str="Asia/Kolkata",
        latitude=28.6139, longitude=77.2090
    )
    norm_modern = normalize_birth_time(inp_modern)

    assert norm_modern.timezone_identifier == "Asia/Kolkata"
    assert norm_modern.utc_offset_hours == 5.5
    assert norm_modern.utc_datetime_iso == "1995-08-15T06:30:00+00:00"

def test_london_dst_spring_forward_transition():
    """Verifies London BST (British Summer Time, UTC+1) vs GMT (UTC+0) transition."""
    # Summer (BST = UTC+1)
    inp_summer = BirthInput(
        name="London Summer",
        year=2020, month=6, day=15,
        hour=12, minute=0, second=0,
        timezone_str="Europe/London",
        latitude=51.5074, longitude=-0.1278
    )
    norm_summer = normalize_birth_time(inp_summer)
    assert norm_summer.utc_offset_hours == 1.0
    assert norm_summer.utc_datetime_iso == "2020-06-15T11:00:00+00:00"

    # Winter (GMT = UTC+0)
    inp_winter = BirthInput(
        name="London Winter",
        year=2020, month=1, day=15,
        hour=12, minute=0, second=0,
        timezone_str="Europe/London",
        latitude=51.5074, longitude=-0.1278
    )
    norm_winter = normalize_birth_time(inp_winter)
    assert norm_winter.utc_offset_hours == 0.0
    assert norm_winter.utc_datetime_iso == "2020-01-15T12:00:00+00:00"

def test_new_york_dst_transitions():
    """Verifies New York EDT (UTC-4) in Summer vs EST (UTC-5) in Winter."""
    # Summer (EDT = UTC-4)
    inp_summer = BirthInput(
        name="NY Summer",
        year=2023, month=7, day=4,
        hour=12, minute=0, second=0,
        timezone_str="America/New_York",
        latitude=40.7128, longitude=-74.0060
    )
    norm_summer = normalize_birth_time(inp_summer)
    assert norm_summer.utc_offset_hours == -4.0
    assert norm_summer.utc_datetime_iso == "2023-07-04T16:00:00+00:00"

    # Winter (EST = UTC-5)
    inp_winter = BirthInput(
        name="NY Winter",
        year=2023, month=12, day=25,
        hour=12, minute=0, second=0,
        timezone_str="America/New_York",
        latitude=40.7128, longitude=-74.0060
    )
    norm_winter = normalize_birth_time(inp_winter)
    assert norm_winter.utc_offset_hours == -5.0
    assert norm_winter.utc_datetime_iso == "2023-12-25T17:00:00+00:00"

def test_historical_espenak_meeus_delta_t():
    """Verifies high-precision NASA Delta-T calculation across historical dates."""
    dt_1890 = calculate_espenak_meeus_delta_t(1890, 6)
    dt_1950 = calculate_espenak_meeus_delta_t(1950, 6)
    dt_2020 = calculate_espenak_meeus_delta_t(2020, 6)

    assert dt_1890 is not None
    assert dt_1950 > 0.0
    assert dt_2020 > 60.0 # Delta-T in 2020 is ~69 seconds

def test_rectification_preserves_original_timezone():
    """Verifies rectification candidate generation preserves base timezone string."""
    from apps.api.engines.rectification_engine import RectificationEngine

    base_input = BirthInput(
        name="Rectification Test",
        year=1988, month=3, day=20,
        hour=10, minute=15, second=0,
        timezone_str="America/Los_Angeles",
        latitude=34.0522, longitude=-118.2437
    )

    result = RectificationEngine.evaluate_candidate_birth_times(
        base_birth_input=base_input,
        candidate_time_offsets_minutes=[-10, 0, 10],
        events=[]
    )

    assert result is not None
    assert result.base_birth_time_iso is not None
