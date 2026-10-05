"""
Authoritative Rule Evaluations for Vedic Yogas.
Operates on Phase 2A Canonical Vedic Chart State.
Fail-closed: Returns INDETERMINATE when required planetary evidence is absent.
Section 4 & 5 Compliance: Imports centralized RASHI_LORDS, EXALTATION_SIGNS, DEBILITATION_SIGNS, OWN_SIGNS and get_house_from_lagna helper!
"""
import math
from typing import Dict, List, Tuple, Any

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.vedic.rashi import (
    RASHI_LORDS as SIGN_RULERS,
    EXALTATION_SIGNS,
    DEBILITATION_SIGNS,
    OWN_SIGNS
)
from apps.api.engines.vedic.houses import get_house_from_lagna
from apps.api.engines.yogas.models import YogaResult, RuleConditionEvidence
from apps.api.engines.yogas.aspects import (
    is_conjunct,
    casts_aspect,
    planet_has_relationship
)

def _get_house_lords(canonical_chart: CanonicalVedicChart) -> Dict[int, str]:
    """Returns mapping of 1-based House Number (1..12) to its ruling planet name."""
    lords: Dict[int, str] = {}
    for house in canonical_chart.whole_sign_houses:
        sign_idx = house.sign_index
        ruler = SIGN_RULERS[sign_idx]
        lords[house.house_number] = ruler
    return lords

def _get_planet_house_map(canonical_chart: CanonicalVedicChart) -> Dict[str, int]:
    """Returns mapping of planet name to its 1-based Whole Sign house number via get_house_from_lagna."""
    asc_sign_idx = canonical_chart.ascendant.sign_index
    house_map: Dict[str, int] = {}
    for name, p in canonical_chart.placements.items():
        p_sign_idx = p.rashi.sign_index
        house_map[name] = get_house_from_lagna(p_sign_idx, asc_sign_idx)
    return house_map

# 1. Pancha Mahapurusha Yogas
MAHAPURUSHA_SPECS = [
    ("Ruchaka", "Mars", "YOGA_RUCHAKA", "Mars in Kendra in Own or Exaltation Sign"),
    ("Bhadra", "Mercury", "YOGA_BHADRA", "Mercury in Kendra in Own or Exaltation Sign"),
    ("Hamsa", "Jupiter", "YOGA_HAMSA", "Jupiter in Kendra in Own or Exaltation Sign"),
    ("Malavya", "Venus", "YOGA_MALAVYA", "Venus in Kendra in Own or Exaltation Sign"),
    ("Shasha", "Saturn", "YOGA_SHASHA", "Saturn in Kendra in Own or Exaltation Sign"),
]

def evaluate_pancha_mahapurusha(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    house_map = _get_planet_house_map(canonical_chart)

    for name, planet_name, rule_id, desc in MAHAPURUSHA_SPECS:
        p_placement = canonical_chart.placements.get(planet_name)
        if not p_placement:
            # Required planet missing -> INDETERMINATE
            results.append(YogaResult(
                rule_id=rule_id,
                name=f"{name} Yoga",
                sanskrit_name=f"{name} Mahapurusha Yoga",
                category="Mahapurusha",
                status="INDETERMINATE",
                conditions=[RuleConditionEvidence(
                    condition_id="planet_presence",
                    condition_description=f"Required planet {planet_name} present in chart",
                    status=False,
                    evidence_details={"missing_planet": planet_name}
                )],
                participating_planets=[],
                participating_houses=[]
            ))
            continue

        p_house = house_map[planet_name]
        p_sign_idx = p_placement.rashi.sign_index

        is_kendra = p_house in [1, 4, 7, 10]
        is_own_or_exalt = (p_sign_idx in OWN_SIGNS[planet_name]) or (p_sign_idx == EXALTATION_SIGNS[planet_name])
        is_active = is_kendra and is_own_or_exalt

        results.append(YogaResult(
            rule_id=rule_id,
            name=f"{name} Yoga",
            sanskrit_name=f"{name} Mahapurusha Yoga",
            category="Mahapurusha",
            status="DETECTED" if is_active else "NOT_DETECTED",
            conditions=[
                RuleConditionEvidence(
                    condition_id="kendra_placement",
                    condition_description=f"{planet_name} in Kendra house (1, 4, 7, 10)",
                    status=is_kendra,
                    evidence_details={"house": p_house}
                ),
                RuleConditionEvidence(
                    condition_id="dignity_placement",
                    condition_description=f"{planet_name} in Own Sign or Exaltation Sign",
                    status=is_own_or_exalt,
                    evidence_details={"sign_index": p_sign_idx}
                )
            ],
            participating_planets=[planet_name] if is_active else [],
            participating_houses=[p_house] if is_active else []
        ))

    return results

# 2. Gajakesari Yoga
def evaluate_gajakesari(canonical_chart: CanonicalVedicChart) -> YogaResult:
    jup_p = canonical_chart.placements.get("Jupiter")
    moon_p = canonical_chart.placements.get("Moon")

    if not jup_p or not moon_p:
        missing_p = "Jupiter" if not jup_p else "Moon"
        return YogaResult(
            rule_id="YOGA_GAJAKESARI",
            name="Gajakesari Yoga",
            sanskrit_name="Gajakesari Yoga",
            category="Auspicious",
            status="INDETERMINATE",
            conditions=[RuleConditionEvidence(
                condition_id="planet_presence",
                condition_description="Jupiter and Moon present in chart",
                status=False,
                evidence_details={"missing_planet": missing_p}
            )],
            participating_planets=[],
            participating_houses=[]
        )

    asc_sign_idx = canonical_chart.ascendant.sign_index
    jup_sign_idx = jup_p.rashi.sign_index
    moon_sign_idx = moon_p.rashi.sign_index

    # Jupiter in Kendra (1, 4, 7, 10) from Moon
    jup_house_from_moon = (jup_sign_idx - moon_sign_idx) % 12 + 1
    is_kendra_from_moon = jup_house_from_moon in [1, 4, 7, 10]

    jup_house_asc = get_house_from_lagna(jup_sign_idx, asc_sign_idx)
    moon_house_asc = get_house_from_lagna(moon_sign_idx, asc_sign_idx)

    return YogaResult(
        rule_id="YOGA_GAJAKESARI",
        name="Gajakesari Yoga",
        sanskrit_name="Gajakesari Yoga",
        category="Auspicious",
        status="DETECTED" if is_kendra_from_moon else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="jup_kendra_from_moon",
            condition_description="Jupiter in Kendra (1st, 4th, 7th, 10th house) from Moon",
            status=is_kendra_from_moon,
            evidence_details={"jup_house_from_moon": jup_house_from_moon}
        )],
        participating_planets=["Jupiter", "Moon"] if is_kendra_from_moon else [],
        participating_houses=[jup_house_asc, moon_house_asc] if is_kendra_from_moon else []
    )

# 3. Budhaditya Yoga
def evaluate_budhaditya(canonical_chart: CanonicalVedicChart) -> YogaResult:
    sun_p = canonical_chart.placements.get("Sun")
    merc_p = canonical_chart.placements.get("Mercury")

    if not sun_p or not merc_p:
        missing_p = "Sun" if not sun_p else "Mercury"
        return YogaResult(
            rule_id="YOGA_BUDHADITYA",
            name="Budhaditya Yoga",
            sanskrit_name="Budhaditya Yoga",
            category="Auspicious",
            status="INDETERMINATE",
            conditions=[RuleConditionEvidence(
                condition_id="planet_presence",
                condition_description="Sun and Mercury present in chart",
                status=False,
                evidence_details={"missing_planet": missing_p}
            )],
            participating_planets=[],
            participating_houses=[]
        )

    asc_sign_idx = canonical_chart.ascendant.sign_index
    is_conj = is_conjunct("Sun", "Mercury", canonical_chart)
    sun_house = get_house_from_lagna(sun_p.rashi.sign_index, asc_sign_idx)

    return YogaResult(
        rule_id="YOGA_BUDHADITYA",
        name="Budhaditya Yoga",
        sanskrit_name="Budhaditya Yoga",
        category="Auspicious",
        status="DETECTED" if is_conj else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="sun_mercury_conjunction",
            condition_description="Sun and Mercury conjunct in same sign",
            status=is_conj,
            evidence_details={"sun_house": sun_house}
        )],
        participating_planets=["Sun", "Mercury"] if is_conj else [],
        participating_houses=[sun_house] if is_conj else []
    )

# 4. Raja Yogas (Lords of Kendra and Trikona conjunct/aspecting)
def evaluate_raja_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    house_lords = _get_house_lords(canonical_chart)
    house_map = _get_planet_house_map(canonical_chart)

    kendra_houses = [1, 4, 7, 10]
    trikona_houses = [1, 5, 9]

    # Find Kendra lords and Trikona lords
    kendra_lords = set(house_lords[h] for h in kendra_houses)
    trikona_lords = set(house_lords[h] for h in trikona_houses)

    # Combinations between Kendra and Trikona lords
    for kl in kendra_lords:
        for tl in trikona_lords:
            if kl == tl:
                continue # Same planet ruling both (e.g. Yogakaraka)

            p1 = canonical_chart.placements.get(kl)
            p2 = canonical_chart.placements.get(tl)
            if not p1 or not p2:
                continue

            rel = planet_has_relationship(kl, tl, canonical_chart)
            if rel:
                rule_id = f"YOGA_RAJA_{kl.upper()}_{tl.upper()}"
                p1_h = house_map[kl]
                p2_h = house_map[tl]
                results.append(YogaResult(
                    rule_id=rule_id,
                    name=f"Raja Yoga ({kl} & {tl})",
                    sanskrit_name="Raja Yoga",
                    category="Raja",
                    status="DETECTED",
                    conditions=[RuleConditionEvidence(
                        condition_id="kendra_trikona_lord_relationship",
                        condition_description=f"Kendra lord ({kl}) and Trikona lord ({tl}) in relationship",
                        status=True,
                        evidence_details={"kendra_lord": kl, "trikona_lord": tl, "relationship": "Conjunction/Aspect"}
                    )],
                    participating_planets=[kl, tl],
                    participating_houses=list(set([p1_h, p2_h]))
                ))

    return results

# Master Yoga Evaluator Function
def evaluate_all_parashari_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    all_yogas = []

    # Pancha Mahapurusha
    all_yogas.extend(evaluate_pancha_mahapurusha(canonical_chart))

    # Gajakesari
    all_yogas.append(evaluate_gajakesari(canonical_chart))

    # Budhaditya
    all_yogas.append(evaluate_budhaditya(canonical_chart))

    # Raja Yogas
    all_yogas.extend(evaluate_raja_yogas(canonical_chart))

    return all_yogas
