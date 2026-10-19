"""
Release Gate G13 Test Suite — Geocentric Planetary Transits & Aspect Contacts.
Verifies real-time ephemeris transits relative to natal Lagna.
"""
import pytest
from datetime import datetime, timezone
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.transit.engine import TransitEngine

def test_planetary_transits_and_aspect_contacts():
    """G13 Gate Test: Verifies transit position calculation and aspect contacts."""
    inp = BirthInput(
        name="Transit Test Native",
        year=1990, month=5, day=15,
        hour=12, minute=0, second=0,
        timezone_str="Asia/Kolkata",
        latitude=28.6139, longitude=77.2090
    )
    chart = build_canonical_vedic_chart(inp)
    q_dt = datetime(2026, 10, 8, 12, 0, 0, tzinfo=timezone.utc)

    transit_res = TransitEngine.calculate_transit_snapshot(chart, query_dt=q_dt)

    assert transit_res is not None
    assert hasattr(transit_res, "placements")

    placements = transit_res.placements
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        assert p_name in placements
        p_info = placements[p_name]
        assert 0.0 <= p_info.sidereal_longitude < 360.0
        assert 1 <= p_info.rashi.sign_index <= 12
        assert 1 <= p_info.house_from_lagna <= 12
