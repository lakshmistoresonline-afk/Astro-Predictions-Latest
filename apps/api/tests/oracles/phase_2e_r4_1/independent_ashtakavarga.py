"""
Independent Ashtakavarga Calculation Engine for R4 Oracle.
Computes BAV and SAV matrices from IndependentChart without production calls.
"""
from typing import Dict, List
from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4_1.independent_constants import BAV_RULES

def r4_independent_bav(chart: IndependentChart, target_planet: str) -> List[int]:
    bav = [0] * 12
    for contributor, houses in BAV_RULES[target_planet].items():
        if contributor == "Ascendant":
            sign = chart.ascendant_sign_index
        elif contributor in chart.planets:
            sign = chart.planets[contributor].sign_index
        else:
            continue

        for h in houses:
            idx = (sign + h - 2) % 12
            bav[idx] += 1

    return bav

def r4_independent_sav(chart: IndependentChart) -> List[int]:
    sav = [0] * 12
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        bav = r4_independent_bav(chart, p)
        for i in range(12):
            sav[i] += bav[i]
    return sav
