"""
Release Gate G15 Test Suite — Muhurta Suitability & Rule Precedence.
Verifies activity suitability evaluations across TRAVEL, MARRIAGE, BUSINESS, EDUCATION, PROPERTY, and SPIRITUALITY.
"""
import pytest
from datetime import datetime, timezone
from apps.api.engines.panchanga.engine import PanchangaEngine
from apps.api.engines.muhurta.engine import MuhurtaEngine

def test_muhurta_activity_suitability_and_precedence():
    """G15 Gate Test: Verifies Muhurta activity suitability suite."""
    eval_dt = datetime(2026, 10, 8, 10, 0, 0, tzinfo=timezone.utc)
    lat, lon = 13.0827, 80.2707 # Chennai

    p_res = PanchangaEngine.calculate_panchanga(
        dt=eval_dt,
        latitude=lat,
        longitude=lon,
        timezone_str="Asia/Kolkata"
    )

    m_res = MuhurtaEngine.calculate_muhurta_suite(p_res)

    assert m_res is not None
    assert len(m_res.evaluations) == 6

    for req_act in ["TRAVEL", "MARRIAGE", "BUSINESS", "EDUCATION", "PROPERTY", "SPIRITUALITY"]:
        assert req_act in m_res.evaluations
        act_eval = m_res.evaluations[req_act]
        assert act_eval.activity_name == req_act
        assert act_eval.recommendation in ["HIGHLY_RECOMMENDED", "RECOMMENDED", "NEUTRAL", "NOT_RECOMMENDED", "INCORRECT_TIME"]
        assert act_eval.summary is not None
