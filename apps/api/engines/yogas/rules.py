"""
Authoritative Rule Evaluations for Vedic Yogas.
Operates on Phase 2A Canonical Vedic Chart State.
Fail-closed: Returns INDETERMINATE when required planetary evidence is absent.
"""
import math
from typing import Dict, List, Tuple, Any

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.yogas.models import YogaResult, RuleConditionEvidence
from apps.api.engines.yogas.aspects import (
    is_conjunct,
    casts_aspect,
    planet_has_relationship
)

# Sign Rulers Mapping (0-indexed sign index 0=Aries, 11=Pisces)
SIGN_RULERS = {
    1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
    5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
    9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
}

# Exaltation & Debilitation Signs
EXALTATION_SIGNS = {
    "Sun": 1, "Moon": 2, "Mars": 10, "Mercury": 6,
    "Jupiter": 4, "Venus": 12, "Saturn": 7, "Rahu": 2, "Ketu": 8
}

DEBILITATION_SIGNS = {
    "Sun": 7, "Moon": 8, "Mars": 4, "Mercury": 12,
    "Jupiter": 10, "Venus": 6, "Saturn": 1, "Rahu": 8, "Ketu": 2
}

OWN_SIGNS = {
    "Sun": [5],
    "Moon": [4],
    "Mars": [1, 8],
    "Mercury": [3, 6],
    "Jupiter": [9, 12],
    "Venus": [2, 7],
    "Saturn": [10, 11]
}

def _get_house_lords(canonical_chart: CanonicalVedicChart) -> Dict[int, str]:
    """Returns mapping of 1-based House Number (1..12) to its ruling planet name."""
    lords: Dict[int, str] = {}
    for house in canonical_chart.whole_sign_houses:
        sign_idx = house.sign_index
        ruler = SIGN_RULERS[sign_idx]
        lords[house.house_number] = ruler
    return lords

def _get_planet_house_map(canonical_chart: CanonicalVedicChart) -> Dict[str, int]:
    """Returns mapping of planet name to its 1-based Whole Sign house number."""
    asc_sign_idx = canonical_chart.ascendant.sign_index
    house_map: Dict[str, int] = {}
    for name, p in canonical_chart.placements.items():
        p_sign_idx = p.rashi.sign_index
        h_num = (p_sign_idx - asc_sign_idx) % 12 + 1
        house_map[name] = h_num
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
        cond1 = RuleConditionEvidence(
            condition_id="kendra_placement",
            condition_description=f"{planet_name} placed in Kendra house (1, 4, 7, 10) from Ascendant",
            status=is_kendra,
            evidence_details={"planet": planet_name, "house": p_house}
        )

        is_own_or_exalt = (p_sign_idx in OWN_SIGNS[planet_name]) or (p_sign_idx == EXALTATION_SIGNS[planet_name])
        cond2 = RuleConditionEvidence(
            condition_id="sign_dignity",
            condition_description=f"{planet_name} placed in Own or Exaltation sign",
            status=is_own_or_exalt,
            evidence_details={"planet": planet_name, "sign": p_placement.rashi.sign, "sign_index": p_sign_idx}
        )

        detected = is_kendra and is_own_or_exalt
        results.append(YogaResult(
            rule_id=rule_id,
            name=f"{name} Yoga",
            sanskrit_name=f"{name} Mahapurusha Yoga",
            category="Mahapurusha",
            status="DETECTED" if detected else "NOT_DETECTED",
            conditions=[cond1, cond2],
            participating_planets=[planet_name],
            participating_houses=[p_house]
        ))

    return results

# 2. Gaja Kesari Yoga
def evaluate_gaja_kesari(canonical_chart: CanonicalVedicChart) -> YogaResult:
    jup_p = canonical_chart.placements.get("Jupiter")
    moon_p = canonical_chart.placements.get("Moon")

    if not jup_p or not moon_p:
        return YogaResult(
            rule_id="YOGA_GAJA_KESARI",
            name="Gaja Kesari Yoga",
            sanskrit_name="Gaja Kesari Yoga",
            category="Auspicious",
            status="INDETERMINATE",
            conditions=[RuleConditionEvidence(
                condition_id="planets_presence",
                condition_description="Required planets (Jupiter and Moon) present in chart",
                status=False,
                evidence_details={"has_jupiter": jup_p is not None, "has_moon": moon_p is not None}
            )],
            participating_planets=[],
            participating_houses=[]
        )

    house_map = _get_planet_house_map(canonical_chart)
    jup_house = house_map["Jupiter"]
    moon_house = house_map["Moon"]

    dist_from_moon = (jup_house - moon_house) % 12
    if dist_from_moon < 0:
        dist_from_moon += 12
    kendra_from_moon = (dist_from_moon + 1) in [1, 4, 7, 10]

    cond1 = RuleConditionEvidence(
        condition_id="jupiter_kendra_from_moon",
        condition_description="Jupiter in Kendra house (1, 4, 7, 10) from Moon",
        status=kendra_from_moon,
        evidence_details={"jupiter_house": jup_house, "moon_house": moon_house, "kendra_offset": dist_from_moon + 1}
    )

    not_debilitated = jup_p.rashi.sign_index != DEBILITATION_SIGNS["Jupiter"]
    cond2 = RuleConditionEvidence(
        condition_id="jupiter_not_debilitated",
        condition_description="Jupiter is not in debilitation sign (Capricorn)",
        status=not_debilitated,
        evidence_details={"jupiter_sign": jup_p.rashi.sign}
    )

    detected = kendra_from_moon and not_debilitated
    return YogaResult(
        rule_id="YOGA_GAJA_KESARI",
        name="Gaja Kesari Yoga",
        sanskrit_name="Gaja Kesari Yoga",
        category="Auspicious",
        status="DETECTED" if detected else "NOT_DETECTED",
        conditions=[cond1, cond2],
        participating_planets=["Jupiter", "Moon"],
        participating_houses=[jup_house, moon_house]
    )

# 3. Budha Aditya Yoga
def evaluate_budha_aditya(canonical_chart: CanonicalVedicChart) -> YogaResult:
    sun_p = canonical_chart.placements.get("Sun")
    merc_p = canonical_chart.placements.get("Mercury")

    if not sun_p or not merc_p:
        return YogaResult(
            rule_id="YOGA_BUDHA_ADITYA",
            name="Budha Aditya Yoga",
            sanskrit_name="Budha Aditya Yoga",
            category="Auspicious",
            status="INDETERMINATE",
            conditions=[RuleConditionEvidence(
                condition_id="planets_presence",
                condition_description="Required planets (Sun and Mercury) present in chart",
                status=False,
                evidence_details={"has_sun": sun_p is not None, "has_mercury": merc_p is not None}
            )],
            participating_planets=[],
            participating_houses=[]
        )

    same_sign = (sun_p.rashi.sign_index == merc_p.rashi.sign_index)
    orb_deg = abs((sun_p.sidereal_longitude - merc_p.sidereal_longitude + 180.0) % 360.0 - 180.0)
    within_orb = same_sign and (orb_deg <= 12.0)

    cond1 = RuleConditionEvidence(
        condition_id="sun_mercury_conjunction",
        condition_description="Sun and Mercury conjunct in same sign within 12.0° orb",
        status=within_orb,
        evidence_details={
            "sun_sign": sun_p.rashi.sign,
            "mercury_sign": merc_p.rashi.sign,
            "orb_deg": round(orb_deg, 4),
            "max_orb_threshold_deg": 12.0
        }
    )

    house_map = _get_planet_house_map(canonical_chart)
    return YogaResult(
        rule_id="YOGA_BUDHA_ADITYA",
        name="Budha Aditya Yoga",
        sanskrit_name="Budha Aditya Yoga",
        category="Auspicious",
        status="DETECTED" if within_orb else "NOT_DETECTED",
        conditions=[cond1],
        exceptions_checked=[RuleConditionEvidence(
            condition_id="mercury_combustion_immunity",
            condition_description="Classical Parashari rule: Mercury is immune to combustion cancellation for Budha Aditya Yoga",
            status=True,
            evidence_details={"orb_deg": round(orb_deg, 4)}
        )],
        participating_planets=["Sun", "Mercury"],
        participating_houses=[house_map.get("Sun", 0), house_map.get("Mercury", 0)]
    )

# 4. Dharma-Karma Adhipati Yoga
def evaluate_dharma_karma(canonical_chart: CanonicalVedicChart) -> YogaResult:
    house_lords = _get_house_lords(canonical_chart)
    house_map = _get_planet_house_map(canonical_chart)

    l9 = house_lords[9]
    l10 = house_lords[10]

    p9_p = canonical_chart.placements.get(l9)
    p10_p = canonical_chart.placements.get(l10)

    if not p9_p or not p10_p:
        return YogaResult(
            rule_id="YOGA_DHARMA_KARMA",
            name="Dharma-Karma Adhipati Yoga",
            sanskrit_name="Dharma-Karma Adhipati Yoga",
            category="Raja",
            status="INDETERMINATE",
            conditions=[],
            participating_planets=[],
            participating_houses=[]
        )

    h9 = house_map[l9]
    h10 = house_map[l10]

    is_conj = is_conjunct(h9, h10)
    is_asp = casts_aspect(l9, h9, h10) and casts_aspect(l10, h10, h9)
    is_pariv = (h9 == 10) and (h10 == 9)

    connected = is_conj or is_asp or is_pariv

    conds = [
        RuleConditionEvidence(
            condition_id="dharma_karma_connection",
            condition_description="Relationship between 9th Lord and 10th Lord (Conjunction, Mutual Aspect, or Parivartana)",
            status=connected,
            evidence_details={
                "lord_9": l9, "house_9_lord": h9,
                "lord_10": l10, "house_10_lord": h10,
                "is_conjunct": is_conj, "is_mutual_aspect": is_asp, "is_parivartana": is_pariv
            }
        )
    ]

    return YogaResult(
        rule_id="YOGA_DHARMA_KARMA",
        name="Dharma-Karma Adhipati Yoga",
        sanskrit_name="Dharma-Karma Adhipati Yoga",
        category="Raja",
        status="DETECTED" if connected else "NOT_DETECTED",
        conditions=conds,
        participating_planets=[l9, l10],
        participating_houses=[h9, h10]
    )

# 5. Parivartana Yogas
def evaluate_parivartana_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    house_lords = _get_house_lords(canonical_chart)
    house_map = _get_planet_house_map(canonical_chart)

    exchanges = []
    for h1 in range(1, 13):
        for h2 in range(h1 + 1, 13):
            l1 = house_lords[h1]
            l2 = house_lords[h2]
            if l1 == l2:
                continue

            p1_p = canonical_chart.placements.get(l1)
            p2_p = canonical_chart.placements.get(l2)
            if not p1_p or not p2_p:
                continue

            if house_map[l1] == h2 and house_map[l2] == h1:
                exchanges.append((h1, l1, h2, l2))

    for h1, l1, h2, l2 in exchanges:
        category = "Parivartana"
        if h1 in [6, 8, 12] or h2 in [6, 8, 12]:
            name = "Dainya Parivartana Yoga"
        elif h1 == 3 or h2 == 3:
            name = "Kahala Parivartana Yoga"
        else:
            name = "Maha Parivartana Yoga"

        conds = [
            RuleConditionEvidence(
                condition_id="mutual_sign_exchange",
                condition_description=f"Mutual sign exchange between {h1}st/th Lord ({l1}) in House {h2} and {h2}nd/th Lord ({l2}) in House {h1}",
                status=True,
                evidence_details={"house_A": h1, "lord_A": l1, "house_B": h2, "lord_B": l2}
            )
        ]

        results.append(YogaResult(
            rule_id=f"YOGA_PARIVARTANA_{h1}_{h2}",
            name=name,
            sanskrit_name=name,
            category=category,
            status="DETECTED",
            conditions=conds,
            participating_planets=[l1, l2],
            participating_houses=[h1, h2]
        ))

    return results

# 6. Viparita Raja Yogas
def evaluate_viparita_raja_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    house_lords = _get_house_lords(canonical_chart)
    house_map = _get_planet_house_map(canonical_chart)

    dusthanas = [6, 8, 12]
    viparita_specs = [
        (6, "Harsha", "YOGA_HARSHA_VIPARITA", "6th Lord placed in 6th, 8th, or 12th house"),
        (8, "Sarala", "YOGA_SARALA_VIPARITA", "8th Lord placed in 6th, 8th, or 12th house"),
        (12, "Vimala", "YOGA_VIMALA_VIPARITA", "12th Lord placed in 6th, 8th, or 12th house"),
    ]

    for d_house, name, rule_id, desc in viparita_specs:
        lord = house_lords[d_house]
        lord_p = canonical_chart.placements.get(lord)
        if not lord_p:
            results.append(YogaResult(
                rule_id=rule_id, name=f"{name} Viparita Raja Yoga", category="Viparita", status="INDETERMINATE", conditions=[], participating_planets=[], participating_houses=[]
            ))
            continue

        p_house = house_map[lord]
        in_dusthana = p_house in dusthanas

        conds = [
            RuleConditionEvidence(
                condition_id="dusthana_lord_in_dusthana",
                condition_description=desc,
                status=in_dusthana,
                evidence_details={"house_lord": d_house, "lord_planet": lord, "placed_house": p_house}
            )
        ]

        results.append(YogaResult(
            rule_id=rule_id,
            name=f"{name} Viparita Raja Yoga",
            sanskrit_name=f"{name} Viparita Raja Yoga",
            category="Viparita",
            status="DETECTED" if in_dusthana else "NOT_DETECTED",
            conditions=conds,
            participating_planets=[lord],
            participating_houses=[p_house]
        ))

    return results

# 7. Neecha Bhanga Raja Yoga
def evaluate_neecha_bhanga(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    house_map = _get_planet_house_map(canonical_chart)
    moon_p = canonical_chart.placements.get("Moon")

    for planet_name, deb_sign in DEBILITATION_SIGNS.items():
        if planet_name in ["Rahu", "Ketu"]:
            continue

        p = canonical_chart.placements.get(planet_name)
        if not p or p.rashi.sign_index != deb_sign:
            continue

        dispositor = SIGN_RULERS[deb_sign]
        disp_p = canonical_chart.placements.get(dispositor)
        disp_house = house_map.get(dispositor, 0) if disp_p else 0

        exalt_sign = EXALTATION_SIGNS[planet_name]
        exalt_lord = SIGN_RULERS[exalt_sign]
        exalt_p = canonical_chart.placements.get(exalt_lord)
        exalt_lord_house = house_map.get(exalt_lord, 0) if exalt_p else 0

        disp_in_kendra_asc = disp_house in [1, 4, 7, 10]
        moon_h = house_map.get("Moon", 0) if moon_p else 0
        disp_in_kendra_moon = ((disp_house - moon_h) % 12 + 1) in [1, 4, 7, 10] if moon_h > 0 else False

        exalt_lord_kendra_asc = exalt_lord_house in [1, 4, 7, 10]

        cancelled = disp_in_kendra_asc or disp_in_kendra_moon or exalt_lord_kendra_asc

        conds = [
            RuleConditionEvidence(
                condition_id="debilitation_present",
                condition_description=f"{planet_name} in debilitation sign ({p.rashi.sign})",
                status=True,
                evidence_details={"planet": planet_name, "sign": p.rashi.sign}
            ),
            RuleConditionEvidence(
                condition_id="cancellation_condition",
                condition_description=f"Dispositor ({dispositor}) or Exaltation Lord ({exalt_lord}) in Kendra from Ascendant/Moon",
                status=cancelled,
                evidence_details={
                    "dispositor": dispositor, "dispositor_house": disp_house,
                    "exaltation_lord": exalt_lord, "exaltation_lord_house": exalt_lord_house
                }
            )
        ]

        results.append(YogaResult(
            rule_id=f"YOGA_NEECHA_BHANGA_{planet_name.upper()}",
            name=f"Neecha Bhanga Raja Yoga ({planet_name})",
            sanskrit_name=f"Neecha Bhanga Raja Yoga ({planet_name})",
            category="NeechaBhanga",
            status="DETECTED" if cancelled else "NOT_DETECTED",
            conditions=conds,
            participating_planets=[planet_name, dispositor, exalt_lord],
            participating_houses=[house_map.get(planet_name, 0), disp_house, exalt_lord_house]
        ))

    return results

# 8. Chandra Yogas (Sunapha, Anapha, Durudhara)
def evaluate_chandra_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    moon_p = canonical_chart.placements.get("Moon")
    if not moon_p:
        for name, rule_id in [("Sunapha", "YOGA_SUNAPHA"), ("Anapha", "YOGA_ANAPHA"), ("Durudhara", "YOGA_DURUDHARA")]:
            results.append(YogaResult(rule_id=rule_id, name=f"{name} Yoga", category="Chandra", status="INDETERMINATE", conditions=[], participating_planets=[], participating_houses=[]))
        return results

    house_map = _get_planet_house_map(canonical_chart)
    moon_h = house_map["Moon"]

    h2_from_moon = (moon_h % 12) + 1
    h12_from_moon = ((moon_h - 2) % 12) + 1

    planets_in_2nd = [p for p, h in house_map.items() if h == h2_from_moon and p not in ["Moon", "Sun", "Rahu", "Ketu"]]
    planets_in_12th = [p for p, h in house_map.items() if h == h12_from_moon and p not in ["Moon", "Sun", "Rahu", "Ketu"]]

    has_sunapha = len(planets_in_2nd) > 0 and len(planets_in_12th) == 0
    has_anapha = len(planets_in_12th) > 0 and len(planets_in_2nd) == 0
    has_durudhara = len(planets_in_2nd) > 0 and len(planets_in_12th) > 0

    specs = [
        ("Sunapha", "YOGA_SUNAPHA", has_sunapha, planets_in_2nd, "Non-luminary planet in 2nd house from Moon"),
        ("Anapha", "YOGA_ANAPHA", has_anapha, planets_in_12th, "Non-luminary planet in 12th house from Moon"),
        ("Durudhara", "YOGA_DURUDHARA", has_durudhara, planets_in_2nd + planets_in_12th, "Non-luminary planets in both 2nd and 12th houses from Moon"),
    ]

    for name, rule_id, status_bool, p_list, desc in specs:
        conds = [
            RuleConditionEvidence(
                condition_id=rule_id.lower(),
                condition_description=desc,
                status=status_bool,
                evidence_details={"occupying_planets": p_list}
            )
        ]

        results.append(YogaResult(
            rule_id=rule_id,
            name=f"{name} Yoga",
            sanskrit_name=f"{name} Yoga",
            category="Chandra",
            status="DETECTED" if status_bool else "NOT_DETECTED",
            conditions=conds,
            participating_planets=["Moon"] + p_list,
            participating_houses=[moon_h, h2_from_moon, h12_from_moon]
        ))

    return results

# 9. Surya Yogas (Veshi, Vashi, Obhayachari)
def evaluate_surya_yogas(canonical_chart: CanonicalVedicChart) -> List[YogaResult]:
    results = []
    sun_p = canonical_chart.placements.get("Sun")
    if not sun_p:
        for name, rule_id in [("Veshi", "YOGA_VESHI"), ("Vashi", "YOGA_VASHI"), ("Obhayachari", "YOGA_OBHAYACHARI")]:
            results.append(YogaResult(rule_id=rule_id, name=f"{name} Yoga", category="Surya", status="INDETERMINATE", conditions=[], participating_planets=[], participating_houses=[]))
        return results

    house_map = _get_planet_house_map(canonical_chart)
    sun_h = house_map["Sun"]

    h2_from_sun = (sun_h % 12) + 1
    h12_from_sun = ((sun_h - 2) % 12) + 1

    planets_in_2nd = [p for p, h in house_map.items() if h == h2_from_sun and p not in ["Sun", "Moon", "Rahu", "Ketu"]]
    planets_in_12th = [p for p, h in house_map.items() if h == h12_from_sun and p not in ["Sun", "Moon", "Rahu", "Ketu"]]

    has_veshi = len(planets_in_2nd) > 0 and len(planets_in_12th) == 0
    has_vashi = len(planets_in_12th) > 0 and len(planets_in_2nd) == 0
    has_obhayachari = len(planets_in_2nd) > 0 and len(planets_in_12th) > 0

    specs = [
        ("Veshi", "YOGA_VESHI", has_veshi, planets_in_2nd, "Non-luminary planet in 2nd house from Sun"),
        ("Vashi", "YOGA_VASHI", has_vashi, planets_in_12th, "Non-luminary planet in 12th house from Sun"),
        ("Obhayachari", "YOGA_OBHAYACHARI", has_obhayachari, planets_in_2nd + planets_in_12th, "Non-luminary planets in both 2nd and 12th houses from Sun"),
    ]

    for name, rule_id, status_bool, p_list, desc in specs:
        conds = [
            RuleConditionEvidence(
                condition_id=rule_id.lower(),
                condition_description=desc,
                status=status_bool,
                evidence_details={"occupying_planets": p_list}
            )
        ]

        results.append(YogaResult(
            rule_id=rule_id,
            name=f"{name} Yoga",
            sanskrit_name=f"{name} Yoga",
            category="Surya",
            status="DETECTED" if status_bool else "NOT_DETECTED",
            conditions=conds,
            participating_planets=["Sun"] + p_list,
            participating_houses=[sun_h, h2_from_sun, h12_from_sun]
        ))

    return results
