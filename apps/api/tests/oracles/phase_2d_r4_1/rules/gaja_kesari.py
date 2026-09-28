"""
Independent Oracle Rule Definition: Gaja Kesari Yoga.
"""
from apps.api.tests.oracles.phase_2d_r4_1.chart_state import IndependentChart
from apps.api.tests.oracles.phase_2d_r4_1.dignity import is_debilitated, is_kendra

def evaluate_gaja_kesari_oracle(chart: IndependentChart) -> str:
    """
    Convention: PARASHARI_CANONICAL
    - Jupiter and Moon present.
    - Jupiter in Kendra (1, 4, 7, 10) from Moon.
    - Jupiter is not debilitated.
    """
    if "Jupiter" not in chart.planets or "Moon" not in chart.planets:
        return "INDETERMINATE"

    jup_house_moon = chart.get_house_from_moon("Jupiter")

    if is_kendra(jup_house_moon):
        if not is_debilitated("Jupiter", chart.planets["Jupiter"].sign_index):
            return "DETECTED"

    return "NOT_DETECTED"
