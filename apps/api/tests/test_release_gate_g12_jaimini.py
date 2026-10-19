"""
Release Gate G12 Test Suite — Jaimini Sutras & Calculation Engine.
Verifies Chara Karakas (7-planet order), Arudha Lagna (AL), Upapada Lagna (UL), and Karakamsha in D9.
"""
import pytest
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.jaimini.engine import JaiminiEngine

def test_jaimini_chara_karakas_and_arudhas():
    """G12 Gate Test: Verifies Jaimini 7 Chara Karakas, Arudha Lagna, and Karakamsha derivations."""
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    chart = build_canonical_vedic_chart(inp)
    jaimini_res = JaiminiEngine.calculate_jaimini_suite(chart)

    # 1. Verify 7 Chara Karakas
    ck = jaimini_res.chara_karakas
    assert "AK" in ck
    assert "AmK" in ck
    assert "BK" in ck
    assert "MK" in ck
    assert "PK" in ck
    assert "GK" in ck
    assert "DK" in ck

    # Subramanian T S: Mercury has highest degree in sign -> Atmakaraka (AK)
    assert ck["AK"].planet == "Mercury"
    assert ck["AK"].karaka_name == "Atmakaraka"
    assert jaimini_res.atmakaraka_planet == "Mercury"

    # 2. Verify Arudha Lagna (AL) & Upapada Lagna (UL)
    assert jaimini_res.arudha_lagna_rashi_index == 4
    assert jaimini_res.arudha_lagna_rashi_name == "Cancer"

    assert jaimini_res.upapada_lagna_rashi_index == 5
    assert jaimini_res.upapada_lagna_rashi_name == "Leo"

    # 3. Verify Karakamsha
    assert jaimini_res.karakamsha_rashi_index == 6
    assert jaimini_res.karakamsha_rashi_name == "Virgo"
    assert len(jaimini_res.calculation_hash) == 64
