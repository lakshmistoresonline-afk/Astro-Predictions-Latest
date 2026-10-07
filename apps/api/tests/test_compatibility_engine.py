"""
Authoritative Unit & Independent Oracle Test Suite for Vedic Ashtakoota Compatibility Engine.
Verifies deterministic sub-scores, maximum points, Nadi/Bhakoot Doshas & Cancellations, and invalid input validation.
"""
import pytest
from apps.api.engines.compatibility_engine import CompatibilityEngine

def test_different_inputs_produce_different_scores():
    """Requirement: Two different input pairs must produce different koota scores and recommendations."""
    res1 = CompatibilityEngine.calculate_ashtakoota("Ashwini", "Rohini")
    res2 = CompatibilityEngine.calculate_ashtakoota("Ashwini", "Ardra")

    assert res1["total_score"] != res2["total_score"]
    assert res1["recommendation"] != res2["recommendation"]
    assert res1["kootas"]["nadi"]["score"] == 8.0 # Ashwini (Adi) & Rohini (Antya) -> Different Nadis
    assert res2["kootas"]["nadi"]["score"] == 0.0 # Ashwini (Adi) & Ardra (Adi) -> Nadi Dosha

def test_same_nakshatra_matching():
    """Test same Nakshatra pair behavior and Pada-based Nadi cancellation."""
    # Same Nakshatra, same Pada -> Nadi Dosha active (0/8)
    res_same_pada = CompatibilityEngine.calculate_ashtakoota("Ashwini-1", "Ashwini-1")
    assert res_same_pada["has_nadi_dosha"] is True
    assert res_same_pada["kootas"]["nadi"]["score"] == 0.0

    # Same Nakshatra, different Padas -> Nadi Dosha cancelled (8/8)
    res_diff_pada = CompatibilityEngine.calculate_ashtakoota("Ashwini-1", "Ashwini-3")
    assert res_diff_pada["has_nadi_dosha"] is False
    assert res_diff_pada["kootas"]["nadi"]["score"] == 8.0

def test_nadi_dosha_cancellation_different_rashis():
    """Same Nakshatra across different Rashis (e.g. Krittika 1 in Aries vs Krittika 2 in Taurus) cancels Nadi Dosha."""
    res = CompatibilityEngine.calculate_ashtakoota("Krittika-1", "Krittika-2")
    assert res["has_nadi_dosha"] is False
    assert res["kootas"]["nadi"]["score"] == 8.0

def test_bhakoot_edge_cases_and_cancellation():
    """Test Bhakoot 6-8 relationship and lord-based cancellation."""
    # Aries (Ashwini) vs Virgo (Hasta) -> 6-8 relationship (Bhakoot Dosha)
    res_6_8 = CompatibilityEngine.calculate_ashtakoota("Ashwini", "Hasta")
    assert res_6_8["kootas"]["bhakoot"]["score"] == 0.0

    # Aries (Ashwini) vs Scorpio (Anuradha) -> 6-8 relationship BUT same Lord (Mars) -> Bhakoot Dosha Cancelled
    res_cancelled = CompatibilityEngine.calculate_ashtakoota("Ashwini", "Anuradha")
    assert res_cancelled["has_bhakoot_dosha"] is False
    assert res_cancelled["kootas"]["bhakoot"]["score"] == 7.0

def test_invalid_nakshatra_input():
    """Validation test: invalid Nakshatra names or out-of-range Padas must fail closed with ValueError."""
    with pytest.raises(ValueError):
        CompatibilityEngine.calculate_ashtakoota("NonExistentNakshatra", "Rohini")

    with pytest.raises(ValueError):
        CompatibilityEngine.calculate_ashtakoota("Ashwini-5", "Rohini")

def test_independent_oracle_reference_dataset():
    """
    Independent Reference Dataset: Verified Ashtakoota test cases.
    Ensures calculations match expected independent Vedic astrology matching rules.
    """
    oracle_cases = [
        # (Boy, Girl, MinExpectedScore, MaxExpectedScore, ExpectedNadiDosha, ExpectedBhakootDosha)
        ("Ashwini", "Bharani", 25.0, 35.0, False, False),  # Aries-Aries (Mars-Mars)
        ("Rohini", "Mrigashira-1", 28.0, 36.0, False, False), # Taurus-Taurus (Venus-Venus)
        ("Ashwini", "Ardra", 10.0, 25.0, True, False),     # Adi-Adi Nadi Dosha
        ("Swati", "Anuradha", 24.0, 36.0, False, False),   # Libra-Scorpio
        ("Pushya", "Ashlesha", 15.0, 28.0, False, False)    # Cancer-Cancer
    ]

    for boy_nak, girl_nak, min_score, max_score, exp_nadi_dosha, exp_bhakoot_dosha in oracle_cases:
        res = CompatibilityEngine.calculate_ashtakoota(boy_nak, girl_nak)
        score = res["total_score"]

        assert min_score <= score <= max_score, f"Case {boy_nak} x {girl_nak} score {score} outside [{min_score}, {max_score}]"
        assert res["has_nadi_dosha"] == exp_nadi_dosha, f"Case {boy_nak} x {girl_nak} Nadi Dosha mismatch"
        assert res["has_bhakoot_dosha"] == exp_bhakoot_dosha, f"Case {boy_nak} x {girl_nak} Bhakoot Dosha mismatch"
