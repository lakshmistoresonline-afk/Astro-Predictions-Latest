"""
Authoritative Rule Evaluations for Vedic Yogas.
Operates on Phase 2A Canonical Vedic Chart State.
Fail-closed: Returns INDETERMINATE when required planetary evidence is absent.
Sections 4 & 5 Compliance: Imports centralized RASHI_LORDS, EXALTATION_SIGNS, DEBILITATION_SIGNS, OWN_SIGNS and get_house_from_lagna helper!
"""
import math
from typing import Dict, List, Tuple, Any, Optional

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

CLASSICAL_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

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

def _is_planet_conjunct(p1_name: str, p2_name: str, house_map: Dict[str, int]) -> bool:
    """Returns True if p1_name and p2_name occupy the exact same Whole Sign house."""
    h1 = house_map.get(p1_name)
    h2 = house_map.get(p2_name)
    if h1 is None or h2 is None:
        return False
    return h1 == h2

def _planet_aspects_planet(p1_name: str, p2_name: str, house_map: Dict[str, int]) -> bool:
    """Returns True if p1_name in its house casts a Parashari aspect onto p2_name's house."""
    h1 = house_map.get(p1_name)
    h2 = house_map.get(p2_name)
    if h1 is None or h2 is None:
        return False
    return casts_aspect(p1_name, h1, h2)

def _planets_have_relationship(p1_name: str, p2_name: str, house_map: Dict[str, int]) -> bool:
    """Returns True if p1 and p2 are conjunct OR either p1 aspects p2 OR p2 aspects p1."""
    return (
        _is_planet_conjunct(p1_name, p2_name, house_map)
        or _planet_aspects_planet(p1_name, p2_name, house_map)
        or _planet_aspects_planet(p2_name, p1_name, house_map)
    )

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
def evaluate_gaja_kesari(canonical_chart: CanonicalVedicChart) -> YogaResult:
    jup_p = canonical_chart.placements.get("Jupiter")
    moon_p = canonical_chart.placements.get("Moon")

    if not jup_p or not moon_p:
        missing_p = "Jupiter" if not jup_p else "Moon"
        return YogaResult(
            rule_id="YOGA_GAJA_KESARI",
            name="Gaja Kesari Yoga",
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

    jup_house_from_moon = (jup_sign_idx - moon_sign_idx) % 12 + 1
    is_kendra_from_moon = jup_house_from_moon in [1, 4, 7, 10]

    jup_house_asc = get_house_from_lagna(jup_sign_idx, asc_sign_idx)
    moon_house_asc = get_house_from_lagna(moon_sign_idx, asc_sign_idx)

    return YogaResult(
        rule_id="YOGA_GAJA_KESARI",
        name="Gaja Kesari Yoga",
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

evaluate_gajakesari = evaluate_gaja_kesari

# 3. Budha Aditya Yoga
def evaluate_budha_aditya(canonical_chart: CanonicalVedicChart) -> YogaResult:
    sun_p = canonical_chart.placements.get("Sun")
    merc_p = canonical_chart.placements.get("Mercury")

    if not sun_p or not merc_p:
        missing_p = "Sun" if not sun_p else "Mercury"
        return YogaResult(
            rule_id="YOGA_BUDHA_ADITYA",
            name="Budha Aditya Yoga",
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
    same_sign = (sun_p.rashi.sign_index == merc_p.rashi.sign_index)
    orb_deg = abs((sun_p.sidereal_longitude - merc_p.sidereal_longitude + 180.0) % 360.0 - 180.0)
    is_active = same_sign and (orb_deg <= 12.0)

    sun_house = get_house_from_lagna(sun_p.rashi.sign_index, asc_sign_idx)

    return YogaResult(
        rule_id="YOGA_BUDHA_ADITYA",
        name="Budha Aditya Yoga",
        sanskrit_name="Budhaditya Yoga",
        category="Auspicious",
        status="DETECTED" if is_active else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="sun_mercury_conjunction",
            condition_description="Sun and Mercury conjunct in same sign within 12 degrees orb",
            status=is_active,
            evidence_details={"same_sign": same_sign, "orb_deg": round(orb_deg, 2), "sun_house": sun_house}
        )],
        participating_planets=["Sun", "Mercury"] if is_active else [],
        participating_houses=[sun_house] if is_active else []
    )

evaluate_budhaditya = evaluate_budha_aditya

# 4. Dharma-Karma Adhipati Yoga
def evaluate_dharma_karma(canonical_chart: CanonicalVedicChart) -> YogaResult:
    house_lords = _get_house_lords(canonical_chart)
    house_map = _get_planet_house_map(canonical_chart)

    lord_9 = house_lords.get(9)
    lord_10 = house_lords.get(10)

    if not lord_9 or not lord_10:
        return YogaResult(
            rule_id="YOGA_DHARMA_KARMA_ADHIPATI",
            name="Dharma-Karma Adhipati Yoga",
            sanskrit_name="Dharma-Karma Adhipati Yoga",
            category="Raja",
            status="INDETERMINATE",
            conditions=[RuleConditionEvidence(
                condition_id="house_lord_presence",
                condition_description="Lords of 9th and 10th houses present",
                status=False,
                evidence_details={"lord_9": lord_9, "lord_10": lord_10}
            )],
            participating_planets=[],
            participating_houses=[]
        )

    if lord_9 == lord_10:
        # Single planet ruling both 9th and 10th (Yogakaraka)
        is_active = True
        rel_type = "Yogakaraka (Single ruler of 9th and 10th)"
    else:
        p9 = canonical_chart.placements.get(lord_9)
        p10 = canonical_chart.placements.get(lord_10)
        if not p9 or not p10:
            return YogaResult(
                rule_id="YOGA_DHARMA_KARMA_ADHIPATI",
                name="Dharma-Karma Adhipati Yoga",
                sanskrit_name="Dharma-Karma Adhipati Yoga",
                category="Raja",
                status="INDETERMINATE",
                conditions=[RuleConditionEvidence(
                    condition_id="planet_presence",
                    condition_description="Placements for 9th and 10th lords present",
                    status=False,
                    evidence_details={"lord_9": lord_9, "lord_10": lord_10}
                )],
                participating_planets=[],
                participating_houses=[]
            )

        is_active = _planets_have_relationship(lord_9, lord_10, house_map)
        rel_type = "Conjunction/Aspect" if is_active else "None"

    h9 = house_map.get(lord_9, 9)
    h10 = house_map.get(lord_10, 10)

    return YogaResult(
        rule_id="YOGA_DHARMA_KARMA_ADHIPATI",
        name="Dharma-Karma Adhipati Yoga",
        sanskrit_name="Dharma-Karma Adhipati Yoga",
        category="Raja",
        status="DETECTED" if is_active else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="dharma_karma_lord_relationship",
            condition_description=f"Relationship between 9th lord ({lord_9}) and 10th lord ({lord_10})",
            status=is_active,
            evidence_details={"lord_9": lord_9, "lord_10": lord_10, "relationship": rel_type}
        )],
        participating_planets=list(set([lord_9, lord_10])) if is_active else [],
        participating_houses=list(set([h9, h10])) if is_active else []
    )

# 5. Parivartana Yogas
def evaluate_parivartana_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    house_lords = _get_house_lords(canonical_chart)
    house_map = _get_planet_house_map(canonical_chart)

    benefic_houses = [1, 2, 4, 5, 7, 9, 10, 11]
    dusthana_houses = [6, 8, 12]

    # Check all pairs of houses (1..12)
    for h1 in range(1, 13):
        for h2 in range(h1 + 1, 13):
            l1 = house_lords[h1]
            l2 = house_lords[h2]
            if l1 == l2:
                continue

            p1 = canonical_chart.placements.get(l1)
            p2 = canonical_chart.placements.get(l2)
            if not p1 or not p2:
                continue

            # Sign exchange: p1 in l2's own sign, p2 in l1's own sign
            p1_in_l2_sign = p1.rashi.sign_index in OWN_SIGNS[l2]
            p2_in_l1_sign = p2.rashi.sign_index in OWN_SIGNS[l1]
            is_exchange = p1_in_l2_sign and p2_in_l1_sign

            if is_exchange:
                if h1 in dusthana_houses or h2 in dusthana_houses:
                    cat_name = "Dainya Parivartana"
                    rule_id = f"YOGA_PARIVARTANA_DAINYA_{h1}_{h2}"
                elif h1 == 3 or h2 == 3:
                    cat_name = "Kahala Parivartana"
                    rule_id = f"YOGA_PARIVARTANA_KAHALA_{h1}_{h2}"
                else:
                    cat_name = "Maha Parivartana"
                    rule_id = f"YOGA_PARIVARTANA_MAHA_{h1}_{h2}"

                results.append(YogaResult(
                    rule_id=rule_id,
                    name=f"{cat_name} (H{h1} & H{h2})",
                    sanskrit_name=f"{cat_name}",
                    category="Parivartana",
                    status="DETECTED",
                    conditions=[RuleConditionEvidence(
                        condition_id="sign_exchange",
                        condition_description=f"Mutual sign exchange between Lord of House {h1} ({l1}) and Lord of House {h2} ({l2})",
                        status=True,
                        evidence_details={"house1": h1, "lord1": l1, "house2": h2, "lord2": l2}
                    )],
                    participating_planets=[l1, l2],
                    participating_houses=[h1, h2]
                ))

    if not results:
        results.append(YogaResult(
            rule_id="YOGA_PARIVARTANA_GENERAL",
            name="Parivartana Yoga",
            sanskrit_name="Parivartana Yoga",
            category="Parivartana",
            status="NOT_DETECTED",
            conditions=[RuleConditionEvidence(
                condition_id="sign_exchange",
                condition_description="Mutual sign exchange between house lords",
                status=False,
                evidence_details={}
            )],
            participating_planets=[],
            participating_houses=[]
        ))

    return results

# 6. Viparita Raja Yogas
VIPARITA_SPECS = [
    ("Harsha", 6, "YOGA_HARSHA", "6th Lord placed in 6th, 8th, or 12th House"),
    ("Sarala", 8, "YOGA_SARALA", "8th Lord placed in 6th, 8th, or 12th House"),
    ("Vimala", 12, "YOGA_VIMALA", "12th Lord placed in 6th, 8th, or 12th House"),
]

def evaluate_viparita_raja_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    house_lords = _get_house_lords(canonical_chart)
    house_map = _get_planet_house_map(canonical_chart)

    for name, target_h, rule_id, desc in VIPARITA_SPECS:
        lord = house_lords.get(target_h)
        if not lord:
            results.append(YogaResult(
                rule_id=rule_id,
                name=f"{name} Yoga",
                sanskrit_name=f"{name} Viparita Raja Yoga",
                category="Viparita",
                status="INDETERMINATE",
                conditions=[RuleConditionEvidence(
                    condition_id="lord_presence",
                    condition_description=f"Lord of House {target_h} present in chart",
                    status=False,
                    evidence_details={"house": target_h}
                )],
                participating_planets=[],
                participating_houses=[]
            ))
            continue

        p_placement = canonical_chart.placements.get(lord)
        if not p_placement:
            results.append(YogaResult(
                rule_id=rule_id,
                name=f"{name} Yoga",
                sanskrit_name=f"{name} Viparita Raja Yoga",
                category="Viparita",
                status="INDETERMINATE",
                conditions=[RuleConditionEvidence(
                    condition_id="planet_presence",
                    condition_description=f"Placement for {lord} present in chart",
                    status=False,
                    evidence_details={"lord": lord}
                )],
                participating_planets=[],
                participating_houses=[]
            ))
            continue

        p_house = house_map[lord]
        is_in_dusthana = p_house in [6, 8, 12]

        results.append(YogaResult(
            rule_id=rule_id,
            name=f"{name} Yoga",
            sanskrit_name=f"{name} Viparita Raja Yoga",
            category="Viparita",
            status="DETECTED" if is_in_dusthana else "NOT_DETECTED",
            conditions=[RuleConditionEvidence(
                condition_id="dusthana_placement",
                condition_description=f"{target_h}th Lord ({lord}) placed in 6th, 8th, or 12th house",
                status=is_in_dusthana,
                evidence_details={"lord": lord, "house": p_house}
            )],
            participating_planets=[lord] if is_in_dusthana else [],
            participating_houses=[p_house] if is_in_dusthana else []
        ))

    return results

# 7. Neecha Bhanga Raja Yogas
def evaluate_neecha_bhanga(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    house_map = _get_planet_house_map(canonical_chart)
    moon_p = canonical_chart.placements.get("Moon")
    moon_house = house_map.get("Moon") if moon_p else None

    for planet in CLASSICAL_PLANETS:
        p_placement = canonical_chart.placements.get(planet)
        if not p_placement:
            results.append(YogaResult(
                rule_id=f"YOGA_NEECHA_BHANGA_{planet.upper()}",
                name=f"Neecha Bhanga ({planet})",
                sanskrit_name="Neecha Bhanga Raja Yoga",
                category="NeechaBhanga",
                status="INDETERMINATE",
                conditions=[RuleConditionEvidence(
                    condition_id="planet_presence",
                    condition_description=f"Placement for {planet} present in chart",
                    status=False,
                    evidence_details={"planet": planet}
                )],
                participating_planets=[],
                participating_houses=[]
            ))
            continue

        p_sign_idx = p_placement.rashi.sign_index
        is_debilitated = (p_sign_idx == DEBILITATION_SIGNS[planet])

        if not is_debilitated:
            results.append(YogaResult(
                rule_id=f"YOGA_NEECHA_BHANGA_{planet.upper()}",
                name=f"Neecha Bhanga ({planet})",
                sanskrit_name="Neecha Bhanga Raja Yoga",
                category="NeechaBhanga",
                status="NOT_DETECTED",
                conditions=[RuleConditionEvidence(
                    condition_id="debilitation_check",
                    condition_description=f"{planet} is placed in its debilitation sign",
                    status=False,
                    evidence_details={"planet": planet, "sign_index": p_sign_idx}
                )],
                participating_planets=[],
                participating_houses=[]
            ))
            continue

        # Cancellation Checks (Neecha Bhanga)
        # 1. Sign lord of debilitated planet is in Kendra from Lagna or Moon
        sign_lord = SIGN_RULERS[p_sign_idx]
        sign_lord_h = house_map.get(sign_lord)
        sign_lord_kendra_lagna = (sign_lord_h in [1, 4, 7, 10]) if sign_lord_h else False
        sign_lord_kendra_moon = ((sign_lord_h - moon_house) % 12 + 1 in [1, 4, 7, 10]) if (sign_lord_h and moon_house) else False

        # 2. Exaltation lord of the sign where planet is debilitated is in Kendra from Lagna or Moon
        # Find which planet gets exalted in p_sign_idx
        exalt_planet = next((pl for pl, ex_sign in EXALTATION_SIGNS.items() if ex_sign == p_sign_idx), None)
        exalt_planet_h = house_map.get(exalt_planet) if exalt_planet else None
        exalt_kendra_lagna = (exalt_planet_h in [1, 4, 7, 10]) if exalt_planet_h else False
        exalt_kendra_moon = ((exalt_planet_h - moon_house) % 12 + 1 in [1, 4, 7, 10]) if (exalt_planet_h and moon_house) else False

        has_neecha_bhanga = (
            sign_lord_kendra_lagna or sign_lord_kendra_moon or exalt_kendra_lagna or exalt_kendra_moon
        )

        p_house = house_map[planet]
        part_planets = [planet]
        if sign_lord:
            part_planets.append(sign_lord)
        if exalt_planet:
            part_planets.append(exalt_planet)

        results.append(YogaResult(
            rule_id=f"YOGA_NEECHA_BHANGA_{planet.upper()}",
            name=f"Neecha Bhanga ({planet})",
            sanskrit_name="Neecha Bhanga Raja Yoga",
            category="NeechaBhanga",
            status="DETECTED" if has_neecha_bhanga else "NOT_DETECTED",
            conditions=[
                RuleConditionEvidence(
                    condition_id="debilitation_check",
                    condition_description=f"{planet} is placed in its debilitation sign",
                    status=True,
                    evidence_details={"planet": planet, "sign_index": p_sign_idx}
                ),
                RuleConditionEvidence(
                    condition_id="neecha_bhanga_kendra_lord",
                    condition_description="Sign or Exaltation lord of debilitation sign in Kendra from Lagna or Moon",
                    status=has_neecha_bhanga,
                    evidence_details={
                        "sign_lord": sign_lord,
                        "sign_lord_kendra_lagna": sign_lord_kendra_lagna,
                        "sign_lord_kendra_moon": sign_lord_kendra_moon,
                        "exalt_planet": exalt_planet,
                        "exalt_kendra_lagna": exalt_kendra_lagna,
                        "exalt_kendra_moon": exalt_kendra_moon
                    }
                )
            ],
            participating_planets=list(set(part_planets)) if has_neecha_bhanga else [],
            participating_houses=[p_house] if has_neecha_bhanga else []
        ))

    return results

# 8. Chandra Yogas
def evaluate_chandra_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    moon_p = canonical_chart.placements.get("Moon")
    house_map = _get_planet_house_map(canonical_chart)

    if not moon_p:
        return [
            YogaResult(
                rule_id=f"YOGA_{name.upper()}",
                name=f"{name} Yoga",
                sanskrit_name=f"{name} Yoga",
                category="Chandra",
                status="INDETERMINATE",
                conditions=[RuleConditionEvidence(
                    condition_id="moon_presence",
                    condition_description="Moon present in chart",
                    status=False,
                    evidence_details={"missing_planet": "Moon"}
                )],
                participating_planets=[],
                participating_houses=[]
            ) for name in ["Sunapha", "Anapha", "Durudhara", "Kemadruma"]
        ]

    moon_house = house_map["Moon"]
    h2_from_moon = (moon_house % 12) + 1
    h12_from_moon = ((moon_house - 2) % 12) + 1

    # Planets excluding Sun, Rahu, Ketu
    planets_in_2nd = [
        p for p, h in house_map.items()
        if h == h2_from_moon and p not in ["Sun", "Moon", "Rahu", "Ketu"]
    ]
    planets_in_12th = [
        p for p, h in house_map.items()
        if h == h12_from_moon and p not in ["Sun", "Moon", "Rahu", "Ketu"]
    ]

    has_sunapha = len(planets_in_2nd) > 0 and len(planets_in_12th) == 0
    has_anapha = len(planets_in_12th) > 0 and len(planets_in_2nd) == 0
    has_durudhara = len(planets_in_2nd) > 0 and len(planets_in_12th) > 0
    has_kemadruma = len(planets_in_2nd) == 0 and len(planets_in_12th) == 0

    results = []

    # Sunapha
    results.append(YogaResult(
        rule_id="YOGA_SUNAPHA",
        name="Sunapha Yoga",
        sanskrit_name="Sunapha Yoga",
        category="Chandra",
        status="DETECTED" if has_sunapha else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="planets_in_2nd_from_moon",
            condition_description="Planets (except Sun/Rahu/Ketu) in 2nd house from Moon, none in 12th",
            status=has_sunapha,
            evidence_details={"planets_in_2nd": planets_in_2nd, "planets_in_12th": planets_in_12th}
        )],
        participating_planets=["Moon"] + planets_in_2nd if has_sunapha else [],
        participating_houses=[moon_house, h2_from_moon] if has_sunapha else []
    ))

    # Anapha
    results.append(YogaResult(
        rule_id="YOGA_ANAPHA",
        name="Anapha Yoga",
        sanskrit_name="Anapha Yoga",
        category="Chandra",
        status="DETECTED" if has_anapha else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="planets_in_12th_from_moon",
            condition_description="Planets (except Sun/Rahu/Ketu) in 12th house from Moon, none in 2nd",
            status=has_anapha,
            evidence_details={"planets_in_12th": planets_in_12th, "planets_in_2nd": planets_in_2nd}
        )],
        participating_planets=["Moon"] + planets_in_12th if has_anapha else [],
        participating_houses=[moon_house, h12_from_moon] if has_anapha else []
    ))

    # Durudhara
    results.append(YogaResult(
        rule_id="YOGA_DURUDHARA",
        name="Durudhara Yoga",
        sanskrit_name="Durudhara Yoga",
        category="Chandra",
        status="DETECTED" if has_durudhara else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="planets_in_both_2nd_and_12th",
            condition_description="Planets (except Sun/Rahu/Ketu) in both 2nd and 12th houses from Moon",
            status=has_durudhara,
            evidence_details={"planets_in_2nd": planets_in_2nd, "planets_in_12th": planets_in_12th}
        )],
        participating_planets=["Moon"] + planets_in_2nd + planets_in_12th if has_durudhara else [],
        participating_houses=[moon_house, h2_from_moon, h12_from_moon] if has_durudhara else []
    ))

    # Kemadruma
    results.append(YogaResult(
        rule_id="YOGA_KEMADRUMA",
        name="Kemadruma Yoga",
        sanskrit_name="Kemadruma Yoga",
        category="Chandra",
        status="DETECTED" if has_kemadruma else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="no_planets_adjacent_to_moon",
            condition_description="No planets (except Sun/Rahu/Ketu) in 2nd or 12th house from Moon",
            status=has_kemadruma,
            evidence_details={"planets_in_2nd": planets_in_2nd, "planets_in_12th": planets_in_12th}
        )],
        participating_planets=["Moon"] if has_kemadruma else [],
        participating_houses=[moon_house] if has_kemadruma else []
    ))

    return results

# 9. Surya Yogas
def evaluate_surya_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    sun_p = canonical_chart.placements.get("Sun")
    house_map = _get_planet_house_map(canonical_chart)

    if not sun_p:
        return [
            YogaResult(
                rule_id=f"YOGA_{name.upper()}",
                name=f"{name} Yoga",
                sanskrit_name=f"{name} Yoga",
                category="Surya",
                status="INDETERMINATE",
                conditions=[RuleConditionEvidence(
                    condition_id="sun_presence",
                    condition_description="Sun present in chart",
                    status=False,
                    evidence_details={"missing_planet": "Sun"}
                )],
                participating_planets=[],
                participating_houses=[]
            ) for name in ["Vesi", "Vasi", "Ubhayachari"]
        ]

    sun_house = house_map["Sun"]
    h2_from_sun = (sun_house % 12) + 1
    h12_from_sun = ((sun_house - 2) % 12) + 1

    # Planets excluding Moon, Rahu, Ketu
    planets_in_2nd = [
        p for p, h in house_map.items()
        if h == h2_from_sun and p not in ["Sun", "Moon", "Rahu", "Ketu"]
    ]
    planets_in_12th = [
        p for p, h in house_map.items()
        if h == h12_from_sun and p not in ["Sun", "Moon", "Rahu", "Ketu"]
    ]

    has_vesi = len(planets_in_2nd) > 0 and len(planets_in_12th) == 0
    has_vasi = len(planets_in_12th) > 0 and len(planets_in_2nd) == 0
    has_ubhayachari = len(planets_in_2nd) > 0 and len(planets_in_12th) > 0

    results = []

    # Vesi
    results.append(YogaResult(
        rule_id="YOGA_VESI",
        name="Vesi Yoga",
        sanskrit_name="Vesi Yoga",
        category="Surya",
        status="DETECTED" if has_vesi else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="planets_in_2nd_from_sun",
            condition_description="Planets (except Moon/Rahu/Ketu) in 2nd house from Sun, none in 12th",
            status=has_vesi,
            evidence_details={"planets_in_2nd": planets_in_2nd, "planets_in_12th": planets_in_12th}
        )],
        participating_planets=["Sun"] + planets_in_2nd if has_vesi else [],
        participating_houses=[sun_house, h2_from_sun] if has_vesi else []
    ))

    # Vasi
    results.append(YogaResult(
        rule_id="YOGA_VASI",
        name="Vasi Yoga",
        sanskrit_name="Vasi Yoga",
        category="Surya",
        status="DETECTED" if has_vasi else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="planets_in_12th_from_sun",
            condition_description="Planets (except Moon/Rahu/Ketu) in 12th house from Sun, none in 2nd",
            status=has_vasi,
            evidence_details={"planets_in_12th": planets_in_12th, "planets_in_2nd": planets_in_2nd}
        )],
        participating_planets=["Sun"] + planets_in_12th if has_vasi else [],
        participating_houses=[sun_house, h12_from_sun] if has_vasi else []
    ))

    # Ubhayachari
    results.append(YogaResult(
        rule_id="YOGA_UBHAYACHARI",
        name="Ubhayachari Yoga",
        sanskrit_name="Ubhayachari Yoga",
        category="Surya",
        status="DETECTED" if has_ubhayachari else "NOT_DETECTED",
        conditions=[RuleConditionEvidence(
            condition_id="planets_in_both_2nd_and_12th_from_sun",
            condition_description="Planets (except Moon/Rahu/Ketu) in both 2nd and 12th houses from Sun",
            status=has_ubhayachari,
            evidence_details={"planets_in_2nd": planets_in_2nd, "planets_in_12th": planets_in_12th}
        )],
        participating_planets=["Sun"] + planets_in_2nd + planets_in_12th if has_ubhayachari else [],
        participating_houses=[sun_house, h2_from_sun, h12_from_sun] if has_ubhayachari else []
    ))

    return results

# 10. Raja Yogas (General Kendra & Trikona Lord Relationships)
def evaluate_raja_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    house_lords = _get_house_lords(canonical_chart)
    house_map = _get_planet_house_map(canonical_chart)

    kendra_houses = [1, 4, 7, 10]
    trikona_houses = [1, 5, 9]

    kendra_lords = set(house_lords[h] for h in kendra_houses)
    trikona_lords = set(house_lords[h] for h in trikona_houses)

    for kl in kendra_lords:
        for tl in trikona_lords:
            if kl == tl:
                continue

            p1 = canonical_chart.placements.get(kl)
            p2 = canonical_chart.placements.get(tl)
            if not p1 or not p2:
                continue

            rel = _planets_have_relationship(kl, tl, house_map)
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

# Master Parashari Yoga Evaluator
def evaluate_all_parashari_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    all_yogas = []
    all_yogas.extend(evaluate_pancha_mahapurusha(canonical_chart))
    all_yogas.append(evaluate_gaja_kesari(canonical_chart))
    all_yogas.append(evaluate_budha_aditya(canonical_chart))
    all_yogas.append(evaluate_dharma_karma(canonical_chart))
    all_yogas.extend(evaluate_parivartana_yogas(canonical_chart))
    all_yogas.extend(evaluate_viparita_raja_yogas(canonical_chart))
    all_yogas.extend(evaluate_neecha_bhanga(canonical_chart))
    all_yogas.extend(evaluate_chandra_yogas(canonical_chart))
    all_yogas.extend(evaluate_surya_yogas(canonical_chart))
    all_yogas.extend(evaluate_raja_yogas(canonical_chart))
    return all_yogas
