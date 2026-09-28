"""
Independent Oracle Rule Definition: Manglik Dosha.
"""
from apps.api.tests.oracles.phase_2d_r4_1.chart_state import IndependentChart
from apps.api.tests.oracles.phase_2d_r4_1.dignity import is_own_sign, is_exalted, is_debilitated
from apps.api.tests.oracles.phase_2d_r4_1.aspects import independent_casts_aspect

def evaluate_manglik_oracle(chart: IndependentChart) -> str:
    """
    Convention: JATAKA_PARIJATA_SYNTHESIS
    - Mars in 1, 2, 4, 7, 8, 12 from Ascendant or Moon.
    - Cancellation: Mars in Own/Exaltation/Debilitation or Jupiter aspect.
    """
    if "Mars" not in chart.planets:
        return "INDETERMINATE"

    mars = chart.planets["Mars"]
    mars_house_asc = chart.get_house("Mars")
    mars_house_moon = chart.get_house_from_moon("Mars") if "Moon" in chart.planets else None

    manglik_houses = [1, 2, 4, 7, 8, 12]
    is_manglik_asc = mars_house_asc in manglik_houses
    is_manglik_moon = mars_house_moon in manglik_houses if mars_house_moon else False

    if not (is_manglik_asc or is_manglik_moon):
        return "NOT_DETECTED"

    # Check cancellations
    is_own = is_own_sign("Mars", mars.sign_index)
    is_exalt = is_exalted("Mars", mars.sign_index)
    is_deb = is_debilitated("Mars", mars.sign_index) # Cancer

    jup_aspects_mars = False
    if "Jupiter" in chart.planets:
        jup_house_asc = chart.get_house("Jupiter")
        if independent_casts_aspect("Jupiter", jup_house_asc, mars_house_asc):
            jup_aspects_mars = True

    if is_own or is_exalt or is_deb or jup_aspects_mars:
        return "CANCELLED"

    return "DETECTED"
