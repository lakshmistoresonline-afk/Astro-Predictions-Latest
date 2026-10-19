"""
Release Gate G14 Test Suite — Panchanga Elements & Local Solar Day Timing.
Verifies Tithi (1..30), Vara, Nakshatra, Nitya Yoga, Karana (1..60), and sunrise/sunset daylight windows.
"""
import pytest
from datetime import datetime, timezone
from apps.api.engines.panchanga.engine import PanchangaEngine

def test_panchanga_elements_and_solar_day():
    """G14 Gate Test: Verifies Panchanga calculation suite."""
    q_dt = datetime(2026, 10, 8, 6, 30, 0, tzinfo=timezone.utc)
    lat, lon = 10.7867, 76.6548

    p_res = PanchangaEngine.calculate_panchanga(
        dt=q_dt,
        latitude=lat,
        longitude=lon,
        timezone_str="Asia/Kolkata"
    )

    assert p_res is not None
    # 1. Verify Tithi (1..30)
    assert p_res.tithi.tithi_number == 28
    assert p_res.tithi.tithi_name == "Trayodashi"
    assert "Krishna" in p_res.tithi.paksha

    # 2. Verify Vara (Local solar day weekday)
    assert p_res.vara.day_name_english == "Thursday"
    assert p_res.vara.day_name_sanskrit == "Guruwara"

    # 3. Verify Nakshatra
    assert isinstance(p_res.nakshatra_name, str) and len(p_res.nakshatra_name) >= 3

    # 4. Verify Nitya Yoga (1..27)
    assert 1 <= p_res.nitya_yoga.yoga_number <= 27

    # 5. Verify Karana (1..60)
    assert 1 <= p_res.karana.karana_number <= 60

    # 6. Verify Daylight Octant Windows (Rahu Kalam, Yamaganda)
    assert p_res.rahu_kalam is not None
    assert p_res.yamaganda is not None
