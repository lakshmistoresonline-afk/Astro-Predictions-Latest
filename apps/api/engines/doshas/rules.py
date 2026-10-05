"""
Authoritative Rule Evaluations for Vedic Doshas.
Operates on Phase 2A Canonical Vedic Chart State.
Fail-closed: Returns INDETERMINATE when required planetary evidence is absent.
Sections 2, 5 & 6 Compliance: Imports centralized RASHI_LORDS, EXALTATION_SIGNS, DEBILITATION_SIGNS, OWN_SIGNS from rashi.py!
"""
import math
from typing import Dict, List, Tuple, Any

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.doshas.models import DoshaResult, DoshaConditionEvidence
from apps.api.engines.yogas.aspects import casts_aspect, planet_has_relationship
from apps.api.engines.vedic.rashi import RASHI_LORDS, DEBILITATION_SIGNS, EXALTATION_SIGNS, OWN_SIGNS

# 1. Manglik / Kuja Dosha
def evaluate_manglik_dosha(canonical_chart: CanonicalVedicChart) -> DoshaResult:
    mars_p = canonical_chart.placements.get("Mars")
    moon_p = canonical_chart.placements.get("Moon")

    # Fail closed if either required planet (Mars or Moon) is missing
    if not mars_p or not moon_p:
        missing_p = "Mars" if not mars_p else "Moon"
        return DoshaResult(
            rule_id="DOSHA_MANGLIK",
            name="Manglik / Kuja Dosha",
            sanskrit_name="Kuja Dosha",
            status="INDETERMINATE",
            conditions=[DoshaConditionEvidence(
                condition_id="planet_presence",
                condition_description=f"Required planet ({missing_p}) present in chart",
                status=False,
                evidence_details={"missing_planet": missing_p}
            )],
            participating_planets=[],
            participating_houses=[]
        )

    asc_sign_idx = canonical_chart.ascendant.sign_index
    moon_sign_idx = moon_p.rashi.sign_index

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
    cancellations = []

    # Exception 1: Mars in own sign or exaltation sign
    if mars_sign_idx in OWN_SIGNS["Mars"] or mars_sign_idx == EXALTATION_SIGNS["Mars"]:
        cancellations.append("Mars in Own Sign or Exaltation Sign")

    # Exception 2: Jupiter aspect or conjunction on Mars
    jup_p = canonical_chart.placements.get("Jupiter")
    if jup_p and planet_has_relationship("Jupiter", "Mars", canonical_chart):
        cancellations.append("Jupiter aspecting or conjunct Mars")

    is_cancelled = len(cancellations) > 0
    final_status = "NOT_DETECTED" if (not is_base_manglik or is_cancelled) else "DETECTED"

    p_houses = list(set([mars_house_asc, mars_house_moon]))

    return DoshaResult(
        rule_id="DOSHA_MANGLIK",
        name="Manglik / Kuja Dosha",
        sanskrit_name="Kuja Dosha",
        status=final_status,
        conditions=conds,
        cancellation_reasons=cancellations,
        participating_planets=["Mars", "Moon"] + (["Jupiter"] if jup_p and is_cancelled else []),
        participating_houses=p_houses
    )

# 2. Kaal Sarp Dosha
def evaluate_kaal_sarp_dosha(canonical_chart: CanonicalVedicChart) -> DoshaResult:
    rahu_p = canonical_chart.placements.get("Rahu")
    ketu_p = canonical_chart.placements.get("Ketu")

    if not rahu_p or not ketu_p:
        return DoshaResult(
            rule_id="DOSHA_KAAL_SARP",
            name="Kaal Sarp Dosha",
            sanskrit_name="Kaal Sarp Dosha",
            status="INDETERMINATE",
            conditions=[DoshaConditionEvidence(
                condition_id="nodes_presence",
                condition_description="Rahu and Ketu present in chart",
                status=False,
                evidence_details={"has_rahu": rahu_p is not None, "has_ketu": ketu_p is not None}
            )],
            participating_planets=[],
            participating_houses=[]
        )

    rahu_lon = rahu_p.sidereal_longitude
    ketu_lon = ketu_p.sidereal_longitude

    # Check if all other 7 planets fall within one hemisphere defined by Rahu-Ketu axis
    seven_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    hemisphere_1 = True
    hemisphere_2 = True

    p_houses = [rahu_p.rashi.sign_index, ketu_p.rashi.sign_index]

    for p_name in seven_planets:
        p_info = canonical_chart.placements.get(p_name)
        if not p_info:
            return DoshaResult(
                rule_id="DOSHA_KAAL_SARP",
                name="Kaal Sarp Dosha",
                sanskrit_name="Kaal Sarp Dosha",
                status="INDETERMINATE",
                conditions=[DoshaConditionEvidence(
                    condition_id="planet_presence",
                    condition_description=f"Required planet ({p_name}) present in chart",
                    status=False,
                    evidence_details={"missing_planet": p_name}
                )],
                participating_planets=[],
                participating_houses=[]
            )

        p_lon = p_info.sidereal_longitude
        p_houses.append(p_info.rashi.sign_index)

        # Angular distance from Rahu clockwise to Ketu
        dist_rahu_ketu = (ketu_lon - rahu_lon) % 360.0
        dist_rahu_planet = (p_lon - rahu_lon) % 360.0

        if dist_rahu_planet > dist_rahu_ketu:
            hemisphere_1 = False
        else:
            hemisphere_2 = False

    is_kaal_sarp = hemisphere_1 or hemisphere_2
    final_status = "DETECTED" if is_kaal_sarp else "NOT_DETECTED"

    return DoshaResult(
        rule_id="DOSHA_KAAL_SARP",
        name="Kaal Sarp Dosha",
        sanskrit_name="Kaal Sarp Dosha",
        status=final_status,
        conditions=[DoshaConditionEvidence(
            condition_id="planets_hemisphere_hemmed",
            condition_description="All 7 core planets hemmed between Rahu and Ketu axis",
            status=is_kaal_sarp,
            evidence_details={"hemisphere_1_hemmed": hemisphere_1, "hemisphere_2_hemmed": hemisphere_2}
        )],
        cancellation_reasons=[],
        participating_planets=["Rahu", "Ketu"] + (seven_planets if is_kaal_sarp else []),
        participating_houses=list(set(p_houses)) if is_kaal_sarp else []
    )

# 3. Pitru Dosha
def evaluate_pitru_dosha(canonical_chart: CanonicalVedicChart) -> DoshaResult:
    sun_p = canonical_chart.placements.get("Sun")
    rahu_p = canonical_chart.placements.get("Rahu")
    ketu_p = canonical_chart.placements.get("Ketu")
    saturn_p = canonical_chart.placements.get("Saturn")

    if not sun_p:
        return DoshaResult(
            rule_id="DOSHA_PITRU",
            name="Pitru Dosha",
            sanskrit_name="Pitru Dosha",
            status="INDETERMINATE",
            conditions=[DoshaConditionEvidence(
                condition_id="sun_presence",
                condition_description="Sun present in chart",
                status=False,
                evidence_details={"has_sun": False}
            )],
            participating_planets=[],
            participating_houses=[]
        )

    # Condition 1: Sun afflicted by Rahu, Ketu, or Saturn (conjunction or aspect)
    sun_afflicted_rahu = rahu_p and (sun_p.rashi.sign_index == rahu_p.rashi.sign_index or casts_aspect("Rahu", "Sun", canonical_chart))
    sun_afflicted_ketu = ketu_p and (sun_p.rashi.sign_index == ketu_p.rashi.sign_index or casts_aspect("Ketu", "Sun", canonical_chart))
    sun_afflicted_saturn = saturn_p and (sun_p.rashi.sign_index == saturn_p.rashi.sign_index or casts_aspect("Saturn", "Sun", canonical_chart))

    # Condition 2: 9th House / 9th Lord afflicted (Section 2: Centralized RASHI_LORDS usage!)
    asc_sign_idx = canonical_chart.ascendant.sign_index
    h9_sign_idx = ((asc_sign_idx + 7) % 12) + 1
    h9_lord = RASHI_LORDS[h9_sign_idx]

    h9_lord_p = canonical_chart.placements.get(h9_lord)
    h9_lord_afflicted = h9_lord_p and rahu_p and (h9_lord_p.rashi.sign_index == rahu_p.rashi.sign_index or casts_aspect("Rahu", h9_lord, canonical_chart))

    is_pitru = sun_afflicted_rahu or sun_afflicted_ketu or sun_afflicted_saturn or h9_lord_afflicted
    final_status = "DETECTED" if is_pitru else "NOT_DETECTED"

    p_planets = ["Sun"]
    if sun_afflicted_rahu or h9_lord_afflicted:
        p_planets.append("Rahu")
    if sun_afflicted_ketu:
        p_planets.append("Ketu")
    if sun_afflicted_saturn:
        p_planets.append("Saturn")

    return DoshaResult(
        rule_id="DOSHA_PITRU",
        name="Pitru Dosha",
        sanskrit_name="Pitru Dosha",
        status=final_status,
        conditions=[DoshaConditionEvidence(
            condition_id="sun_or_9th_lord_afflicted",
            condition_description="Sun or 9th Lord afflicted by Rahu, Ketu, or Saturn",
            status=is_pitru,
            evidence_details={
                "sun_afflicted_rahu": bool(sun_afflicted_rahu),
                "sun_afflicted_ketu": bool(sun_afflicted_ketu),
                "sun_afflicted_saturn": bool(sun_afflicted_saturn),
                "h9_lord_afflicted": bool(h9_lord_afflicted)
            }
        )],
        cancellation_reasons=[],
        participating_planets=list(set(p_planets)) if is_pitru else [],
        participating_houses=[sun_p.rashi.sign_index, h9_sign_idx] if is_pitru else []
    )
