"""
Independent Oracle Rule Definition: Budha Aditya Yoga.
"""
from apps.api.tests.oracles.phase_2d_r4_1.chart_state import IndependentChart

def evaluate_budha_aditya_oracle(chart: IndependentChart) -> str:
    """
    Convention: PARASHARI_CANONICAL
    - Sun and Mercury must be present
    - Must be in same sign
    - Absolute angular separation <= 12.0 degrees
    - Mercury combustion does NOT cancel.
    """
    if "Sun" not in chart.planets or "Mercury" not in chart.planets:
        return "INDETERMINATE"

    sun = chart.planets["Sun"]
    mercury = chart.planets["Mercury"]

    if sun.sign_index != mercury.sign_index:
        return "NOT_DETECTED"

    delta = abs(sun.longitude - mercury.longitude) % 360.0
    orb = min(delta, 360.0 - delta)

    if orb <= 12.0:
        return "DETECTED"
    else:
        return "NOT_DETECTED"
