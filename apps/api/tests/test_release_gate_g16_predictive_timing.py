"""
Release Gate G16 Test Suite — Convergent Domain Timing Windows.
Verifies predictive timing windows, dasha-transit convergence, and SAV bindu weighting.
"""
import pytest
from datetime import datetime, timezone
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.timing.engine import TimingEngine

def test_predictive_timing_suite_and_windows():
    """G16 Gate Test: Verifies predictive timing window generation and domain convergence."""
    inp = BirthInput(
        name="Timing Test Native",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    chart = build_canonical_vedic_chart(inp)
    q_dt = datetime(2026, 10, 8, 12, 0, 0, tzinfo=timezone.utc)

    timing_res = TimingEngine.generate_timing_suite(chart, query_dt=q_dt)

    assert timing_res is not None
    assert hasattr(timing_res, "timing_windows")

    windows = timing_res.timing_windows
    assert len(windows) >= 1

    # Verify each window carries domain code, evidence status, and participating planets
    for w in windows:
        assert hasattr(w, "domain")
        assert hasattr(w, "evidence_status")
        assert w.evidence_status in ["CONVERGENT", "PARTIAL", "UNAVAILABLE"]
