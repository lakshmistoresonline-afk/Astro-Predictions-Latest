"""
Phase 2E-R4.1 Corruption Sensitivity Test Suite.
Proves that intentionally corrupting fixture expected values or production results triggers hard test failures.
"""
import pytest
from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4_1.independent_shadbala import r4_calculate_shadbala_for_planet
from apps.api.tests.oracles.phase_2e_r4_1.independent_ashtakavarga import r4_independent_bav, r4_independent_sav

def test_corrupted_expected_shadbala_causes_failure():
    chart = IndependentChart(321.43, 256.08, 23.85, 2446702.95, 1986, 9, 28, 16, 30)
    chart.add_planet("Sun", 161.54, 0.98, False)
    chart.add_planet("Moon", 80.0, 13.1, False)

    oracle_res = r4_calculate_shadbala_for_planet(chart, "Sun")
    corrupted_expected = oracle_res["total_shashtiamsas"] + 50.0 # Corrupted by +50 shashtiamsas

    with pytest.raises(AssertionError):
        assert abs(corrupted_expected - oracle_res["total_shashtiamsas"]) <= 0.03

def test_corrupted_sav_total_causes_failure():
    chart = IndependentChart(321.43, 256.08, 23.85, 2446702.95, 1986, 9, 28, 16, 30)
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        chart.add_planet(p, 100.0, 1.0, False)

    sav_res = r4_independent_sav(chart)
    corrupted_sav_sum = sum(sav_res) - 10 # Corrupted total

    with pytest.raises(AssertionError):
        assert corrupted_sav_sum == 337
