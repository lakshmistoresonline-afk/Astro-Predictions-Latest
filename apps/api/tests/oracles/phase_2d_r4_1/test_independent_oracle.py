"""
Phase 2D-R4.1 Genuinely Independent Oracle Integration Tests.
Executes the production engine and compares actual results against
independently constructed rule definitions and chart states.
"""
import pytest
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.yogas.evaluator import YogaEvaluator
from apps.api.engines.doshas.evaluator import DoshaEvaluator

from apps.api.tests.fixtures.phase_2d_r3.synthetic import get_base_chart, set_planet, set_ascendant
from apps.api.tests.oracles.phase_2d_r4_1.chart_state import IndependentChart
from apps.api.tests.oracles.phase_2d_r4_1.rules.budha_aditya import evaluate_budha_aditya_oracle
from apps.api.tests.oracles.phase_2d_r4_1.rules.gaja_kesari import evaluate_gaja_kesari_oracle
from apps.api.tests.oracles.phase_2d_r4_1.rules.mahapurusha import evaluate_mahapurusha_oracle
from apps.api.tests.oracles.phase_2d_r4_1.rules.manglik import evaluate_manglik_oracle

def sync_charts(asc_lon, planets):
    """Creates matched pair of IndependentChart and CanonicalVedicChart."""
    ind_chart = IndependentChart(asc_lon)
    prod_chart = get_base_chart()
    set_ascendant(prod_chart, asc_lon)

    for name, lon in planets.items():
        ind_chart.add_planet(name, lon)
        set_planet(prod_chart, name, lon)

    return ind_chart, prod_chart

def get_prod_status(suite, rule_id):
    if hasattr(suite, 'all_evaluated_yogas'):
        res = next((r for r in suite.all_evaluated_yogas if r.rule_id == rule_id), None)
    else:
        res = next((r for r in suite.all_evaluated_doshas if r.rule_id == rule_id), None)
    return res.status if res else "UNKNOWN"

# --- BUDHA ADITYA YOGA ORACLE VALIDATION ---
def test_budha_aditya_oracle_positive():
    ind, prod = sync_charts(0.0, {"Sun": 150.0, "Mercury": 161.9})
    assert evaluate_budha_aditya_oracle(ind) == "DETECTED"
    assert get_prod_status(YogaEvaluator.evaluate_all_yogas(prod), "YOGA_BUDHA_ADITYA") == "DETECTED"

def test_budha_aditya_oracle_negative_orb():
    ind, prod = sync_charts(0.0, {"Sun": 150.0, "Mercury": 162.1})
    assert evaluate_budha_aditya_oracle(ind) == "NOT_DETECTED"
    assert get_prod_status(YogaEvaluator.evaluate_all_yogas(prod), "YOGA_BUDHA_ADITYA") == "NOT_DETECTED"

def test_budha_aditya_oracle_indeterminate():
    ind, prod = sync_charts(0.0, {"Sun": 150.0}) # Missing Mercury
    del prod.placements["Mercury"]
    assert evaluate_budha_aditya_oracle(ind) == "INDETERMINATE"
    assert get_prod_status(YogaEvaluator.evaluate_all_yogas(prod), "YOGA_BUDHA_ADITYA") == "INDETERMINATE"

# --- GAJA KESARI YOGA ORACLE VALIDATION ---
def test_gaja_kesari_oracle_positive():
    ind, prod = sync_charts(0.0, {"Moon": 30.0, "Jupiter": 210.0}) # Taurus and Scorpio (Kendra)
    assert evaluate_gaja_kesari_oracle(ind) == "DETECTED"
    assert get_prod_status(YogaEvaluator.evaluate_all_yogas(prod), "YOGA_GAJA_KESARI") == "DETECTED"

def test_gaja_kesari_oracle_debilitation():
    ind, prod = sync_charts(0.0, {"Moon": 180.0, "Jupiter": 270.0}) # Libra and Capricorn (Kendra but Debilitated)
    assert evaluate_gaja_kesari_oracle(ind) == "NOT_DETECTED"
    assert get_prod_status(YogaEvaluator.evaluate_all_yogas(prod), "YOGA_GAJA_KESARI") == "NOT_DETECTED"

# --- MAHAPURUSHA ORACLE VALIDATION ---
def test_ruchaka_oracle_positive():
    ind, prod = sync_charts(90.0, {"Mars": 0.0}) # Cancer Asc, Mars in Aries (10th Kendra, Own sign)
    assert evaluate_mahapurusha_oracle(ind, "YOGA_RUCHAKA") == "DETECTED"
    assert get_prod_status(YogaEvaluator.evaluate_all_yogas(prod), "YOGA_RUCHAKA") == "DETECTED"

def test_ruchaka_oracle_negative_house():
    ind, prod = sync_charts(60.0, {"Mars": 0.0}) # Gemini Asc, Mars in Aries (11th, Own sign)
    assert evaluate_mahapurusha_oracle(ind, "YOGA_RUCHAKA") == "NOT_DETECTED"
    assert get_prod_status(YogaEvaluator.evaluate_all_yogas(prod), "YOGA_RUCHAKA") == "NOT_DETECTED"

# --- MANGLIK DOSHA ORACLE VALIDATION ---
def test_manglik_oracle_positive():
    ind, prod = sync_charts(30.0, {"Mars": 120.0, "Jupiter": 330.0}) # Taurus Asc, Mars Leo (4th), Jup Pisces (no aspect to Leo)
    assert evaluate_manglik_oracle(ind) == "DETECTED"
    assert get_prod_status(DoshaEvaluator.evaluate_all_doshas(prod), "DOSHA_MANGLIK") == "DETECTED"

def test_manglik_oracle_cancellation_exalt():
    ind, prod = sync_charts(0.0, {"Mars": 270.0}) # Aries Asc, Mars Cap (10th... wait, Manglik houses are 1,2,4,7,8,12)
    # Let's use 8th house for Mars to trigger Manglik
    ind, prod = sync_charts(0.0, {"Mars": 210.0}) # Aries Asc, Mars Scorpio (8th) -> Own sign
    assert evaluate_manglik_oracle(ind) == "CANCELLED"
    assert get_prod_status(DoshaEvaluator.evaluate_all_doshas(prod), "DOSHA_MANGLIK") == "CANCELLED"

def test_manglik_oracle_cancellation_aspect():
    ind, prod = sync_charts(0.0, {"Mars": 90.0, "Jupiter": 330.0}) # Aries Asc, Mars Cancer (4th, Debilitated). Wait, Cancer also cancels by deb.
    # Let's use 7th house (Libra) and Jupiter aspect from 11th (Aquarius - 9th aspect to Libra)
    ind, prod = sync_charts(0.0, {"Mars": 180.0, "Jupiter": 300.0}) # Mars Libra (7th), Jup Aquarius (11th). Jup aspects 5,7,9 -> 11+9-1 = 19%12 = 7th house (Libra).
    assert evaluate_manglik_oracle(ind) == "CANCELLED"
    assert get_prod_status(DoshaEvaluator.evaluate_all_doshas(prod), "DOSHA_MANGLIK") == "CANCELLED"
