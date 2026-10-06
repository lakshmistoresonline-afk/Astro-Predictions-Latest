"""
Authoritative Rule Evaluations for Vedic Doshas.
Operates on Phase 2A Canonical Vedic Chart State.
Fail-closed: Returns INDETERMINATE when required planetary evidence is absent.
Sections 2, 5 & 6 Compliance:
- Explicit 1..12 Whole Sign house number derivation from Lagna for all aspect & conjunction calls.
- Participating_houses strictly populated with 1..12 Whole Sign house numbers (never sign indices!).
- Centralized RASHI_LORDS, EXALTATION_SIGNS, DEBILITATION_SIGNS, OWN_SIGNS imported from rashi.py.
"""
import math
from typing import Dict, List, Tuple, Any, Optional

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.doshas.models import DoshaResult, DoshaConditionEvidence
from apps.api.engines.yogas.aspects import casts_aspect, planet_has_relationship
from apps.api.engines.vedic.rashi import RASHI_LORDS, DEBILITATION_SIGNS, EXALTATION_SIGNS, OWN_SIGNS
from apps.api.engines.vedic.houses import get_house_from_lagna

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

    # 1-based Whole Sign houses from Lagna
    mars_house_asc = get_house_from_lagna(mars_sign_idx, asc_sign_idx)
    moon_house_asc = get_house_from_lagna(moon_sign_idx, asc_sign_idx)

    # Houses from Moon
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
    cancellation_evs: List[DoshaConditionEvidence] = []

    # Exception 1: Mars in own sign or exaltation sign
    is_own_or_exalt = (mars_sign_idx in OWN_SIGNS["Mars"]) or (mars_sign_idx == EXALTATION_SIGNS["Mars"])
    if is_own_or_exalt:
        cancellation_evs.append(DoshaConditionEvidence(
            condition_id="mars_dignity_cancellation",
            condition_description="Mars in Own Sign or Exaltation Sign",
            status=True,
            evidence_details={"mars_sign_index": mars_sign_idx}
        ))

    # Exception 2: Jupiter aspect or conjunction on Mars (Explicit 1..12 Whole Sign house numbers from Lagna)
    jup_p = canonical_chart.placements.get("Jupiter")
    jup_cancels = False
    if jup_p:
        jup_house_asc = get_house_from_lagna(jup_p.rashi.sign_index, asc_sign_idx)
        if planet_has_relationship("Jupiter", jup_house_asc, mars_house_asc):
            jup_cancels = True
            cancellation_evs.append(DoshaConditionEvidence(
                condition_id="jupiter_aspect_cancellation",
                condition_description="Jupiter aspecting or conjunct Mars",
                status=True,
                evidence_details={"jupiter_house": jup_house_asc, "mars_house": mars_house_asc}
            ))

    is_cancelled = is_base_manglik and (len(cancellation_evs) > 0)
    if is_cancelled:
        final_status = "CANCELLED"
    elif is_base_manglik:
        final_status = "DETECTED"
    else:
        final_status = "NOT_DETECTED"

    participating_h = [mars_house_asc, moon_house_asc]
    if jup_p and jup_cancels:
        participating_h.append(get_house_from_lagna(jup_p.rashi.sign_index, asc_sign_idx))

    return DoshaResult(
        rule_id="DOSHA_MANGLIK",
        name="Manglik / Kuja Dosha",
        sanskrit_name="Kuja Dosha",
        status=final_status,
        conditions=conds,
        cancellation_exceptions=cancellation_evs,
        participating_planets=["Mars", "Moon"] + (["Jupiter"] if jup_cancels else []),
        participating_houses=list(set(participating_h)) if final_status in ["DETECTED", "CANCELLED"] else []
    )

# 2. Kemadruma Dosha
def evaluate_kemadruma_dosha(canonical_chart: CanonicalVedicChart) -> DoshaResult:
    moon_p = canonical_chart.placements.get("Moon")

    if not moon_p:
        return DoshaResult(
            rule_id="DOSHA_KEMADRUMA",
            name="Kemadruma Dosha",
            sanskrit_name="Kemadruma Dosha",
            status="INDETERMINATE",
            conditions=[DoshaConditionEvidence(
                condition_id="moon_presence",
                condition_description="Moon present in chart",
                status=False,
                evidence_details={"has_moon": False}
            )],
            participating_planets=[],
            participating_houses=[]
        )

    asc_sign_idx = canonical_chart.ascendant.sign_index
    moon_sign_idx = moon_p.rashi.sign_index
    moon_house_asc = get_house_from_lagna(moon_sign_idx, asc_sign_idx)

    h2_from_moon = (moon_house_asc % 12) + 1
    h12_from_moon = ((moon_house_asc - 2) % 12) + 1

    # Map planets to Whole Sign houses from Lagna (1..12)
    house_map: Dict[str, int] = {}
    for p_name, p in canonical_chart.placements.items():
        house_map[p_name] = get_house_from_lagna(p.rashi.sign_index, asc_sign_idx)

    # Planets excluding Sun, Rahu, Ketu
    planets_in_2nd = [
        p for p, h in house_map.items()
        if h == h2_from_moon and p not in ["Sun", "Moon", "Rahu", "Ketu"]
    ]
    planets_in_12th = [
        p for p, h in house_map.items()
        if h == h12_from_moon and p not in ["Sun", "Moon", "Rahu", "Ketu"]
    ]

    is_base_kemadruma = (len(planets_in_2nd) == 0 and len(planets_in_12th) == 0)

    conds = [
        DoshaConditionEvidence(
            condition_id="no_planets_adjacent_to_moon",
            condition_description="No planets (except Sun/Rahu/Ketu) in 2nd or 12th house from Moon",
            status=is_base_kemadruma,
            evidence_details={
                "moon_house": moon_house_asc,
                "planets_in_2nd": planets_in_2nd,
                "planets_in_12th": planets_in_12th
            }
        )
    ]

    # Cancellation Checks (Kemadruma Bhanga)
    cancellation_evs: List[DoshaConditionEvidence] = []

    # Cancellation 1: Any planet (except Sun/Rahu/Ketu) in Kendra (1, 4, 7, 10) from Lagna
    planets_in_kendra_lagna = [
        p for p, h in house_map.items()
        if h in [1, 4, 7, 10] and p not in ["Sun", "Moon", "Rahu", "Ketu"]
    ]
    if planets_in_kendra_lagna:
        cancellation_evs.append(DoshaConditionEvidence(
            condition_id="planets_in_kendra_lagna",
            condition_description="Planet(s) placed in Kendra (1st, 4th, 7th, 10th house) from Lagna",
            status=True,
            evidence_details={"planets": planets_in_kendra_lagna}
        ))

    # Cancellation 2: Any planet (except Sun/Rahu/Ketu) in Kendra (1, 4, 7, 10) from Moon
    planets_in_kendra_moon = []
    for p, h in house_map.items():
        if p not in ["Sun", "Moon", "Rahu", "Ketu"]:
            h_from_moon = (h - moon_house_asc) % 12 + 1
            if h_from_moon in [1, 4, 7, 10]:
                planets_in_kendra_moon.append(p)

    if planets_in_kendra_moon:
        cancellation_evs.append(DoshaConditionEvidence(
            condition_id="planets_in_kendra_moon",
            condition_description="Planet(s) placed in Kendra (1st, 4th, 7th, 10th house) from Moon",
            status=True,
            evidence_details={"planets": planets_in_kendra_moon}
        ))

    is_cancelled = is_base_kemadruma and (len(cancellation_evs) > 0)

    if is_cancelled:
        final_status = "CANCELLED"
    elif is_base_kemadruma:
        final_status = "DETECTED"
    else:
        final_status = "NOT_DETECTED"

    return DoshaResult(
        rule_id="DOSHA_KEMADRUMA",
        name="Kemadruma Dosha",
        sanskrit_name="Kemadruma Dosha",
        status=final_status,
        conditions=conds,
        cancellation_exceptions=cancellation_evs,
        participating_planets=["Moon"],
        participating_houses=[moon_house_asc]
    )

# 3. Kala Sarpa / Kaal Sarp Dosha
def evaluate_kala_sarpa_dosha(canonical_chart: CanonicalVedicChart) -> DoshaResult:
    rahu_p = canonical_chart.placements.get("Rahu")
    ketu_p = canonical_chart.placements.get("Ketu")

    if not rahu_p or not ketu_p:
        return DoshaResult(
            rule_id="DOSHA_KALA_SARPA",
            name="Kala Sarpa Dosha",
            sanskrit_name="Kala Sarpa Dosha",
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

    asc_sign_idx = canonical_chart.ascendant.sign_index
    rahu_house = get_house_from_lagna(rahu_p.rashi.sign_index, asc_sign_idx)
    ketu_house = get_house_from_lagna(ketu_p.rashi.sign_index, asc_sign_idx)

    rahu_lon = rahu_p.sidereal_longitude
    ketu_lon = ketu_p.sidereal_longitude

    seven_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    hemisphere_1 = True
    hemisphere_2 = True

    p_houses = [rahu_house, ketu_house]

    for p_name in seven_planets:
        p_info = canonical_chart.placements.get(p_name)
        if not p_info:
            return DoshaResult(
                rule_id="DOSHA_KALA_SARPA",
                name="Kala Sarpa Dosha",
                sanskrit_name="Kala Sarpa Dosha",
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
        p_house = get_house_from_lagna(p_info.rashi.sign_index, asc_sign_idx)
        p_houses.append(p_house)

        dist_rahu_ketu = (ketu_lon - rahu_lon) % 360.0
        dist_rahu_planet = (p_lon - rahu_lon) % 360.0

        if dist_rahu_planet > dist_rahu_ketu:
            hemisphere_1 = False
        else:
            hemisphere_2 = False

    is_kaal_sarp = hemisphere_1 or hemisphere_2
    final_status = "DETECTED" if is_kaal_sarp else "NOT_DETECTED"

    return DoshaResult(
        rule_id="DOSHA_KALA_SARPA",
        name="Kala Sarpa Dosha",
        sanskrit_name="Kala Sarpa Dosha",
        status=final_status,
        conditions=[DoshaConditionEvidence(
            condition_id="planets_hemisphere_hemmed",
            condition_description="All 7 core planets hemmed between Rahu and Ketu axis",
            status=is_kaal_sarp,
            evidence_details={"hemisphere_1_hemmed": hemisphere_1, "hemisphere_2_hemmed": hemisphere_2}
        )],
        cancellation_exceptions=[],
        participating_planets=["Rahu", "Ketu"] + (seven_planets if is_kaal_sarp else []),
        participating_houses=list(set(p_houses)) if is_kaal_sarp else []
    )

evaluate_kaal_sarp_dosha = evaluate_kala_sarpa_dosha

# 4. Pitru Dosha
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

    asc_sign_idx = canonical_chart.ascendant.sign_index

    # Derive exact 1..12 Whole Sign houses from Lagna
    sun_house = get_house_from_lagna(sun_p.rashi.sign_index, asc_sign_idx)
    rahu_house = get_house_from_lagna(rahu_p.rashi.sign_index, asc_sign_idx) if rahu_p else None
    ketu_house = get_house_from_lagna(ketu_p.rashi.sign_index, asc_sign_idx) if ketu_p else None
    saturn_house = get_house_from_lagna(saturn_p.rashi.sign_index, asc_sign_idx) if saturn_p else None

    # Condition 1: Sun afflicted by Rahu, Ketu, or Saturn (conjunction or aspect using 1..12 Whole Sign houses)
    sun_afflicted_rahu = rahu_p and (sun_house == rahu_house or casts_aspect("Rahu", rahu_house, sun_house))
    sun_afflicted_ketu = ketu_p and (sun_house == ketu_house or casts_aspect("Ketu", ketu_house, sun_house))
    sun_afflicted_saturn = saturn_p and (sun_house == saturn_house or casts_aspect("Saturn", saturn_house, sun_house))

    # Condition 2: 9th House / 9th Lord afflicted (Section 2: Centralized RASHI_LORDS usage!)
    h9_sign_idx = ((asc_sign_idx + 7) % 12) + 1 # 9th house sign index (1..12)
    h9_lord = RASHI_LORDS[h9_sign_idx]

    h9_lord_p = canonical_chart.placements.get(h9_lord)
    h9_lord_house = get_house_from_lagna(h9_lord_p.rashi.sign_index, asc_sign_idx) if h9_lord_p else None
    h9_lord_afflicted = h9_lord_p and rahu_p and (h9_lord_house == rahu_house or casts_aspect("Rahu", rahu_house, h9_lord_house))

    is_pitru = sun_afflicted_rahu or sun_afflicted_ketu or sun_afflicted_saturn or h9_lord_afflicted
    final_status = "DETECTED" if is_pitru else "NOT_DETECTED"

    p_planets = ["Sun"]
    if sun_afflicted_rahu or h9_lord_afflicted:
        p_planets.append("Rahu")
    if sun_afflicted_ketu:
        p_planets.append("Ketu")
    if sun_afflicted_saturn:
        p_planets.append("Saturn")

    p_houses = [sun_house, 9]
    if h9_lord_house:
        p_houses.append(h9_lord_house)

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
        cancellation_exceptions=[],
        participating_planets=list(set(p_planets)) if is_pitru else [],
        participating_houses=list(set(p_houses)) if is_pitru else []
    )
