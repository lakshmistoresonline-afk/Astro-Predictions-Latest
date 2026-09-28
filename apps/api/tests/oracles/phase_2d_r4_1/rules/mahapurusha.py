"""
Independent Oracle Rule Definition: Pancha Mahapurusha Yogas.
"""
from apps.api.tests.oracles.phase_2d_r4_1.chart_state import IndependentChart
from apps.api.tests.oracles.phase_2d_r4_1.dignity import is_kendra, is_own_sign, is_exalted

MAHAPURUSHA_MAP = {
    "YOGA_RUCHAKA": "Mars",
    "YOGA_BHADRA": "Mercury",
    "YOGA_HAMSA": "Jupiter",
    "YOGA_MALAVYA": "Venus",
    "YOGA_SHASHA": "Saturn"
}

def evaluate_mahapurusha_oracle(chart: IndependentChart, rule_id: str) -> str:
    """
    Convention: PARASHARI_CANONICAL
    - Planet in Kendra from Ascendant.
    - Planet in Own or Exaltation Sign.
    """
    planet = MAHAPURUSHA_MAP[rule_id]

    if planet not in chart.planets:
        return "INDETERMINATE"

    house = chart.get_house(planet)
    sign_idx = chart.planets[planet].sign_index

    if is_kendra(house) and (is_own_sign(planet, sign_idx) or is_exalted(planet, sign_idx)):
        return "DETECTED"

    return "NOT_DETECTED"
