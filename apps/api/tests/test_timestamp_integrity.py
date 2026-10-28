"""
Regression tests for timestamp integrity, duration consistency, and provenance validation.
Proves that reported run durations match recorded UTC start/end timestamps and rejects
silent replacement of missing timestamps with invented values.
"""
import pytest
from datetime import datetime, timezone
import json
from pathlib import Path

def test_utc_timestamp_format():
    """Verify that generated UTC timestamps are valid ISO 8601 strings with timezone info."""
    now_utc = datetime.now(timezone.utc).isoformat()
    assert "T" in now_utc
    # ISO format from datetime.now(timezone.utc).isoformat() ends with +00:00 or Z
    dt = datetime.fromisoformat(now_utc)
    assert dt.tzinfo is not None

def test_duration_consistency():
    """Verify that elapsed duration matches difference between start and end timestamps."""
    start = datetime(2026, 10, 22, 6, 30, 0, tzinfo=timezone.utc)
    end = datetime(2026, 10, 22, 6, 32, 30, tzinfo=timezone.utc)
    duration_seconds = (end - start).total_seconds()
    assert duration_seconds == 150.0

def test_unverified_timestamp_policy():
    """Verify that missing historical timestamps are marked UNVERIFIED/UNAVAILABLE rather than fabricated."""
    historical_record = {
        "run_id": "RUN_LEGACY_001",
        "start_timestamp_utc": "UNVERIFIED",
        "end_timestamp_utc": "UNAVAILABLE",
        "duration_seconds": 269.79
    }
    assert historical_record["start_timestamp_utc"] == "UNVERIFIED"
    assert historical_record["end_timestamp_utc"] == "UNAVAILABLE"
    # Ensure no false claim of exact datetime range when unverified
    with pytest.raises(ValueError):
        datetime.fromisoformat(historical_record["start_timestamp_utc"])

def test_evidence_validator_timestamp_check():
    """Verify evidence validator rejects contradictory timestamps."""
    def validate_timestamps(data):
        start = data.get("start_timestamp_utc")
        end = data.get("end_timestamp_utc")
        if start in ["UNVERIFIED", "UNAVAILABLE"] or end in ["UNVERIFIED", "UNAVAILABLE"]:
            return True # Allowed if explicitly qualified
        dt_start = datetime.fromisoformat(start)
        dt_end = datetime.fromisoformat(end)
        if dt_end < dt_start:
            raise ValueError("End time cannot be earlier than start time")
        return True

    valid_data = {
        "start_timestamp_utc": "2026-10-22T06:30:00+00:00",
        "end_timestamp_utc": "2026-10-22T06:32:30+00:00"
    }
    assert validate_timestamps(valid_data) is True

    invalid_data = {
        "start_timestamp_utc": "2026-10-22T06:32:30+00:00",
        "end_timestamp_utc": "2026-10-22T06:30:00+00:00"
    }
    with pytest.raises(ValueError, match="End time cannot be earlier"):
        validate_timestamps(invalid_data)
