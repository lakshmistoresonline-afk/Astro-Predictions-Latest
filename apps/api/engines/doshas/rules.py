"""
Authoritative Rule Evaluations for Vedic Doshas.
Operates on Phase 2A Canonical Vedic Chart State.
"""
import math
from typing import Dict, List, Tuple, Any

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.doshas.models import DoshaResult, DoshaConditionEvidence
from apps.api.engines.yogas.aspects import planet_aspects_house
from apps.api.engines.yogas.rules import DEBILITATION_SIGNS, EXALTATION_SIGNS, OWN_SIGNS

# 1. Manglik / Kuja Dosha
def evaluate_manglik_dosha(canonical_chart: CanonicalVedicChart) -> DoshaResult:
    asc_sign_idx = canonical_chart.ascendant.sign_index
    moon_sign_idx = canonical_chart.placements["Moon"].rashi.sign_index if "Moon" in canonical_chart.placements else asc_sign_idx

    mars_p = canonical_chart.placements.get("Mars")
    if not mars_p:
        return DoshaResult(rule_id="DOSHA_MANGLIK", name="Manglik / Kuja Dosha", status="INDETERMINATE", conditions=[], participating_planets=[], participating_houses=[])

    mars_sign_idx = mars_p.rashi.sign_index
    mars_house_asc = (mars_sign_idx - asc_sign_idx) % 12 + 1
    mars_house_moon = (mars_sign_idx - moon_sign_idx) % 12 + 1

    manglik_houses = [1, 2, 4, 7, 8, 12]
    is_manglik_asc = mars_house_asc in manglik_houses
    is_manglik_moon = mars_house_moon in manglik_houses
    is_base_manglik = is_manglik_asc or is_manglik_moon

    conds = [
        DoshaConditionEvidence(
            condition_id="mars_in_manglik_house",
            condition_description="Mars placed in 1st, 2nd, 4th, 7th, 8th, or 12th house from Ascendant or Moon",
            status=is_base_manglik,
            evidence_details={
                "mars_house_from_ascendant": mars_house_asc,
                "mars_house_from_moon": mars_house_moon,
                "qualifying_houses": manglik_houses
            }
        )
    ]

    # Cancellation exceptions
    excep_own_exalt = mars_sign_idx in OWN_SIGNS["Mars"] or mars_sign_idx == EXALTATION_SIGNS["Mars"]
    excep_cancer = (mars_sign_idx == 4) # Cancer debilitation

    jup_p = canonical_chart.placements.get("Jupiter")
    jup_sign_idx = jup_p.rashi.sign_index if jup_p else 0
    jup_house_asc = (jup_sign_idx - asc_sign_idx) % 12 + 1 if jup_p else 0
    excep_jupiter_aspect = planet_aspects_house("Jupiter", jup_house_asc, mars_house_asc) if jup_p else False

    is_cancelled = is_base_manglik and (excep_own_exalt or excep_cancer or excep_jupiter_aspect)

    canc_conds = [
        DoshaConditionEvidence(
            condition_id="cancellation_dignity_or_aspect",
            condition_description="Mars in Own/Exaltation/Debilitation sign or aspected by Jupiter",
            status=is_cancelled,
            evidence_details={
                "in_own_or_exalt": excep_own_exalt,
                "in_cancer": excep_cancer,
                "aspected_by_jupiter": excep_jupiter_aspect
            }
        )
    ]

    if is_cancelled:
        final_status = "CANCELLED"
    elif is_base_manglik:
        final_status = "DETECTED"
    else:
        final_status = "NOT_DETECTED"

    return DoshaResult(
        rule_id="DOSHA_MANGLIK",
        name="Manglik / Kuja Dosha",
        sanskrit_name="Kuja Dosha",
        status=final_status,
        conditions=conds,
        cancellation_exceptions=canc_conds,
        participating_planets=["Mars"] + (["Jupiter"] if excep_jupiter_aspect else []),
        participating_houses=[mars_house_asc, mars_house_moon]
    )

# 2. Kemadruma Dosha
def evaluate_kemadruma_dosha(canonical_chart: CanonicalVedicChart) -> DoshaResult:
    asc_sign_idx = canonical_chart.ascendant.sign_index
    moon_p = canonical_chart.placements.get("Moon")
    if not moon_p:
        return DoshaResult(rule_id="DOSHA_KEMADRUMA", name="Kemadruma Dosha", status="INDETERMINATE", conditions=[], participating_planets=[], participating_houses=[])

    moon_sign_idx = moon_p.rashi.sign_index
    moon_house_asc = (moon_sign_idx - asc_sign_idx) % 12 + 1

    h2_from_moon = (moon_house_asc % 12) + 1
    h12_from_moon = ((moon_house_asc - 2) % 12) + 1

    # Check 2nd and 12th from Moon for planets (excl. Sun, Rahu, Ketu)
    planets_in_2_12 = []
    kendra_planets = []

    for name, p in canonical_chart.placements.items():
        if name in ["Moon", "Sun", "Rahu", "Ketu"]:
            continue
        p_house_asc = (p.rashi.sign_index - asc_sign_idx) % 12 + 1
        p_house_from_moon = (p.rashi.sign_index - moon_sign_idx) % 12 + 1

        if p_house_asc in [h2_from_moon, h12_from_moon]:
            planets_in_2_12.append(name)

        if p_house_asc in [1, 4, 7, 10] or p_house_from_moon in [1, 4, 7, 10]:
            kendra_planets.append(name)

    is_isolated = len(planets_in_2_12) == 0
    is_cancelled = is_isolated and len(kendra_planets) > 0

    conds = [
        DoshaConditionEvidence(
            condition_id="moon_isolated_2_12",
            condition_description="No planets (excl. Sun/Rahu/Ketu) in 2nd or 12th house from Moon",
            status=is_isolated,
            evidence_details={"planets_in_2nd_or_12th": planets_in_2_12}
        )
    ]

    canc_conds = [
        DoshaConditionEvidence(
            condition_id="kendra_planets_cancellation",
            condition_description="Planets present in Kendra from Moon or Ascendant",
            status=is_cancelled,
            evidence_details={"kendra_planets": kendra_planets}
        )
    ]

    if is_cancelled:
        final_status = "CANCELLED"
    elif is_isolated:
        final_status = "DETECTED"
    else:
        final_status = "NOT_DETECTED"

    return DoshaResult(
        rule_id="DOSHA_KEMADRUMA",
        name="Kemadruma Dosha",
        sanskrit_name="Kemadruma Dosha",
        status=final_status,
        conditions=conds,
        cancellation_exceptions=canc_conds,
        participating_planets=["Moon"] + planets_in_2_12 + kendra_planets,
        participating_houses=[moon_house_asc, h2_from_moon, h12_from_moon]
    )

# 3. Kala Sarpa-Type Condition
def evaluate_kala_sarpa_dosha(canonical_chart: CanonicalVedicChart) -> DoshaResult:
    rahu_p = canonical_chart.placements.get("Rahu")
    ketu_p = canonical_chart.placements.get("Ketu")

    if not rahu_p or not ketu_p:
        return DoshaResult(rule_id="DOSHA_KALA_SARPA", name="Kala Sarpa Condition", status="INDETERMINATE", conditions=[], participating_planets=[], participating_houses=[])

    rahu_lon = rahu_p.sidereal_longitude
    ketu_lon = ketu_p.sidereal_longitude

    classical_7 = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
    planets_hemisphere = []

    # Bounding arc from Rahu to Ketu counter-clockwise
    for p_name in classical_7:
        p = canonical_chart.placements.get(p_name)
        if not p:
            continue
        p_lon = p.sidereal_longitude
        rel_lon = (p_lon - rahu_lon) % 360.0
        planets_hemisphere.append(rel_lon < 180.0)

    all_one_side = all(planets_hemisphere) or all(not b for b in planets_hemisphere)

    conds = [
        DoshaConditionEvidence(
            condition_id="all_planets_hemisphere_containment",
            condition_description="All 7 classical planets contained within one 180° hemisphere bounded by Rahu-Ketu axis",
            status=all_one_side,
            evidence_details={"rahu_lon": rahu_lon, "ketu_lon": ketu_lon, "all_one_side": all_one_side}
        )
    ]

    return DoshaResult(
        rule_id="DOSHA_KALA_SARPA",
        name="Kala Sarpa Condition",
        sanskrit_name="Kala Sarpa Yoga / Dosha",
        status="DETECTED" if all_one_side else "NOT_DETECTED",
        conditions=conds,
        participating_planets=["Rahu", "Ketu"] + classical_7,
        participating_houses=[rahu_p.rashi.sign_index, ketu_p.rashi.sign_index]
    )
