"""
Independent Rule Validation Oracle for Astrovision Yoga & Dosha Engine (Phase 2D-R3).
Expected values are independently defined and checked against the engine's output.
Uses synthetic chart data to bypass Skyfield and test exact mathematical boundaries.
"""
import pytest
from apps.api.tests.fixtures.phase_2d_r3.synthetic import get_base_chart, set_planet, set_ascendant
from apps.api.engines.yogas import YogaEvaluator
from apps.api.engines.doshas import DoshaEvaluator

def get_rule(suite, rule_id):
    if hasattr(suite, 'all_evaluated_yogas'):
        return next((r for r in suite.all_evaluated_yogas if r.rule_id == rule_id), None)
    else:
        return next((r for r in suite.all_evaluated_doshas if r.rule_id == rule_id), None)

# --- 1. Budha Aditya Yoga Validation ---
def test_budha_aditya_positive():
    chart = get_base_chart()
    set_planet(chart, "Sun", 150.0) # Virgo 0
    set_planet(chart, "Mercury", 161.9) # Virgo 11.9
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_BUDHA_ADITYA").status == "DETECTED"

def test_budha_aditya_negative_orb():
    chart = get_base_chart()
    set_planet(chart, "Sun", 150.0)
    set_planet(chart, "Mercury", 162.1) # Orb 12.1 > 12.0
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_BUDHA_ADITYA").status == "NOT_DETECTED"

def test_budha_aditya_negative_different_signs():
    chart = get_base_chart()
    set_planet(chart, "Sun", 149.0) # Leo 29
    set_planet(chart, "Mercury", 151.0) # Virgo 1 (Orb 2.0, but different signs)
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_BUDHA_ADITYA").status == "NOT_DETECTED"

def test_budha_aditya_boundary_orb():
    chart = get_base_chart()
    set_planet(chart, "Sun", 150.0)
    set_planet(chart, "Mercury", 162.000000) # Exactly 12.0
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_BUDHA_ADITYA").status == "DETECTED"

def test_budha_aditya_missing_planet():
    chart = get_base_chart()
    del chart.placements["Mercury"]
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_BUDHA_ADITYA").status == "INDETERMINATE"

# --- 2. Gaja Kesari Yoga Validation ---
def test_gaja_kesari_positive():
    chart = get_base_chart()
    set_ascendant(chart, 0.0) # Aries Asc
    set_planet(chart, "Moon", 30.0) # Taurus (2nd house)
    # Kendra from Moon: 1, 4, 7, 10 from Taurus -> Taurus, Leo, Scorpio, Aquarius
    set_planet(chart, "Jupiter", 210.0) # Scorpio (7th from Moon)
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_GAJA_KESARI").status == "DETECTED"

def test_gaja_kesari_negative():
    chart = get_base_chart()
    set_ascendant(chart, 0.0)
    set_planet(chart, "Moon", 30.0) # Taurus
    set_planet(chart, "Jupiter", 240.0) # Sagittarius (8th from Moon)
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_GAJA_KESARI").status == "NOT_DETECTED"

def test_gaja_kesari_cancellation_debilitated():
    chart = get_base_chart()
    set_planet(chart, "Moon", 180.0) # Libra
    # Kendra from Libra -> Libra, Capricorn, Aries, Cancer
    set_planet(chart, "Jupiter", 270.0) # Capricorn (4th from Moon, BUT debilitated)
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_GAJA_KESARI").status == "NOT_DETECTED"

# --- 3. Pancha Mahapurusha Validation (Ruchaka) ---
def test_ruchaka_positive():
    chart = get_base_chart()
    set_ascendant(chart, 90.0) # Cancer Asc (1)
    # Kendra from Cancer -> Cancer (1), Libra (4), Capricorn (7), Aries (10)
    set_planet(chart, "Mars", 0.0) # Aries (10th house, Own sign)
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_RUCHAKA").status == "DETECTED"

def test_ruchaka_negative_not_kendra():
    chart = get_base_chart()
    set_ascendant(chart, 60.0) # Gemini Asc
    set_planet(chart, "Mars", 0.0) # Aries (11th house, Own sign)
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_RUCHAKA").status == "NOT_DETECTED"

def test_ruchaka_negative_not_own_exalt():
    chart = get_base_chart()
    set_ascendant(chart, 0.0) # Aries Asc
    set_planet(chart, "Mars", 90.0) # Cancer (4th house Kendra, BUT debilitated)
    res = YogaEvaluator.evaluate_all_yogas(chart)
    assert get_rule(res, "YOGA_RUCHAKA").status == "NOT_DETECTED"

# --- 4. Manglik Dosha Validation ---
def test_manglik_positive():
    chart = get_base_chart()
    set_ascendant(chart, 0.0) # Aries
    set_planet(chart, "Mars", 210.0) # Scorpio (8th house) -> Manglik
    set_planet(chart, "Moon", 60.0) # Gemini
    res = DoshaEvaluator.evaluate_all_doshas(chart)
    # Wait, Mars in Scorpio is OWN SIGN -> CANCELLED!
    assert get_rule(res, "DOSHA_MANGLIK").status == "CANCELLED"

def test_manglik_positive_uncancelled():
    chart = get_base_chart()
    set_ascendant(chart, 0.0) # Aries
    set_planet(chart, "Mars", 90.0) # Cancer (4th house) -> Cancer debilitation CANCELS it!
    res = DoshaEvaluator.evaluate_all_doshas(chart)
    assert get_rule(res, "DOSHA_MANGLIK").status == "CANCELLED"

def test_manglik_true_positive():
    chart = get_base_chart()
    set_ascendant(chart, 30.0) # Taurus (1)
    set_planet(chart, "Mars", 120.0) # Leo (4th house) -> Not own/exalt/debilitated.
    set_planet(chart, "Jupiter", 330.0) # Pisces (11th house) -> Aspects 3, 5, 7 from 11th (not 4th)
    res = DoshaEvaluator.evaluate_all_doshas(chart)
    assert get_rule(res, "DOSHA_MANGLIK").status == "DETECTED"

def test_manglik_negative():
    chart = get_base_chart()
    set_ascendant(chart, 0.0) # Aries
    set_planet(chart, "Mars", 240.0) # Sagittarius (9th house) -> Not Manglik
    res = DoshaEvaluator.evaluate_all_doshas(chart)
    assert get_rule(res, "DOSHA_MANGLIK").status == "NOT_DETECTED"

# --- 5. Kemadruma Dosha Validation ---
def test_kemadruma_positive():
    chart = get_base_chart()
    set_ascendant(chart, 0.0)
    set_planet(chart, "Moon", 60.0) # Gemini (3rd house)
    # Move all other planets to houses that are not 2nd/12th from Moon (Taurus, Cancer)
    for p in ["Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        set_planet(chart, p, 180.0) # Libra (5th house)

    # 2nd from Moon (Cancer) and 12th from Moon (Taurus) are empty.
    # Kendras from Asc (1, 4, 7, 10) -> Aries, Cancer, Libra, Capricorn
    # Kendras from Moon (1, 4, 7, 10 from Gemini) -> Gemini, Virgo, Sagittarius, Pisces
    # Planets are in Libra -> 7th from Ascendant -> Cancellation!

    # Let's move them to a non-Kendra from both.
    # Non-Kendras from Asc: 2, 3, 5, 6, 8, 9, 11, 12
    # Non-Kendras from Moon (Gemini): 2, 3, 5, 6, 8, 9, 11, 12 from Gemini
    # Let's put them in Leo (Asc 5th, Moon 3rd).
    for p in ["Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        set_planet(chart, p, 120.0)

    res = DoshaEvaluator.evaluate_all_doshas(chart)
    assert get_rule(res, "DOSHA_KEMADRUMA").status == "DETECTED"

def test_kemadruma_cancellation():
    chart = get_base_chart()
    set_ascendant(chart, 0.0)
    set_planet(chart, "Moon", 60.0) # Gemini
    for p in ["Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        set_planet(chart, p, 120.0) # Leo

    # Put Jupiter in Kendra from Moon (Virgo) -> Cancer, Virgo is 4th from Gemini
    set_planet(chart, "Jupiter", 150.0) # Virgo

    res = DoshaEvaluator.evaluate_all_doshas(chart)
    assert get_rule(res, "DOSHA_KEMADRUMA").status == "CANCELLED"
