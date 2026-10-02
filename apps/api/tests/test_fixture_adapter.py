"""
Unit Tests for Canonical Fixture Adapter (reference_fixture_to_birth_input).
Verifies correct transformation for REF_001, REF_002, REF_015, REF_016, REF_020 and malformed fixture rejection.
"""
import json
import pytest
from pathlib import Path
from apps.api.tests.fixtures.fixture_adapter import reference_fixture_to_birth_input
from apps.api.engines.vedic.models import BirthInput

REF_DIR = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected")

@pytest.mark.parametrize("fid", ["REF_001", "REF_002", "REF_015", "REF_016", "REF_020"])
def test_reference_fixture_adapter_valid_fixtures(fid):
    fpath = REF_DIR / f"{fid}.json"
    assert fpath.exists(), f"Reference fixture file missing: {fpath}"
    with open(fpath, "r", encoding="utf-8") as f:
        doc = json.load(f)

    b_inp = reference_fixture_to_birth_input(doc)
    assert isinstance(b_inp, BirthInput)
    assert b_inp.year == doc["local_year"]
    assert b_inp.month == doc["local_month"]
    assert b_inp.day == doc["local_day"]
    assert b_inp.hour == doc["local_hour"]
    assert b_inp.minute == doc["local_minute"]
    assert b_inp.latitude == doc["latitude"]
    assert b_inp.longitude == doc["longitude"]
    assert b_inp.timezone_str == doc.get("timezone_str", "Asia/Kolkata")

def test_reference_fixture_adapter_malformed_rejection():
    with pytest.raises(ValueError, match="Malformed reference fixture"):
        reference_fixture_to_birth_input("NOT_A_DICT")

    with pytest.raises(ValueError, match="missing required birth input fields"):
        reference_fixture_to_birth_input({"fixture_id": "BAD_001", "name": "Bad"})

    with pytest.raises(ValueError, match="Latitude 100.0 out of physical range"):
        reference_fixture_to_birth_input({
            "local_year": 1986, "local_month": 9, "local_day": 28,
            "local_hour": 16, "local_minute": 30,
            "latitude": 100.0, "longitude": 76.6,
            "timezone_str": "Asia/Kolkata"
        })
