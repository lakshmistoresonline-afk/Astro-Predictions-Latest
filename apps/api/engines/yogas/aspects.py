"""
Canonical Parashari Planetary Aspect & Conjunction Engine for Astrovision.
Strictly separates Conjunction (same Whole Sign house) from Cast Aspect (4th, 7th, 8th, etc. across houses).

Core Design Principles:
1. Strict Type Signatures: House-level functions take integer 1-based house numbers [1..12].
2. High-Level Chart Helpers: Chart functions accept CanonicalVedicChart and planet names.
3. Explicit Node Aspect Convention: Rahu/Ketu trine aspects (5th, 7th, 9th) governed by explicit parameter/configuration.
"""
from typing import Dict, List, Optional, Set, Tuple, Any

# Explicit Rahu/Ketu Parashari Trine Aspect Convention Flag (5th, 7th, 9th)
DEFAULT_INCLUDE_NODE_ASPECTS: bool = True

def get_house_distance(source_house: int, target_house: int) -> int:
    """Returns 0-based Whole Sign house distance from source_house to target_house in [0, 11]."""
    if not isinstance(source_house, int) or not isinstance(target_house, int):
        return 0
    if not (1 <= source_house <= 12) or not (1 <= target_house <= 12):
        return 0
    dist = (target_house - source_house) % 12
    return dist if dist >= 0 else dist + 12

def is_conjunct(source_house: int, target_house: int) -> bool:
    """Returns True if source_house and target_house represent the identical Whole Sign house [1..12]."""
    if not isinstance(source_house, int) or not isinstance(target_house, int):
        return False
    if not (1 <= source_house <= 12) or not (1 <= target_house <= 12):
        return False
    return source_house == target_house

def casts_aspect(
    planet_name: str,
    source_house: int,
    target_house: int,
    include_node_aspects: bool = DEFAULT_INCLUDE_NODE_ASPECTS
) -> bool:
    """
    Evaluates whether planet_name in source_house (1..12) casts a Parashari aspect onto target_house (1..12).
    Conjunction (source_house == target_house) is NOT an aspect and returns False.
    """
    if not isinstance(source_house, int) or not isinstance(target_house, int):
        return False

    if not (1 <= source_house <= 12) or not (1 <= target_house <= 12):
        return False

    if source_house == target_house:
        return False # Conjunction is distinct from aspect

    dist_0_based = get_house_distance(source_house, target_house)
    house_offset = dist_0_based + 1 # 1-based house offset (1st..12th)

    # All classical planets cast 7th house aspect
    if house_offset == 7:
        return True

    # Mars special aspects: 4th, 7th, 8th
    if planet_name == "Mars" and house_offset in [4, 7, 8]:
        return True

    # Jupiter special aspects: 5th, 7th, 9th
    if planet_name == "Jupiter" and house_offset in [5, 7, 9]:
        return True

    # Saturn special aspects: 3rd, 7th, 10th
    if planet_name == "Saturn" and house_offset in [3, 7, 10]:
        return True

    # Rahu/Ketu special aspects: 5th, 7th, 9th (Explicitly configurable)
    if include_node_aspects and planet_name in ["Rahu", "Ketu"] and house_offset in [5, 7, 9]:
        return True

    return False

def planet_has_relationship(
    planet_name: str,
    source_house: int,
    target_house: int,
    include_node_aspects: bool = DEFAULT_INCLUDE_NODE_ASPECTS
) -> bool:
    """
    Returns True if source_house and target_house are conjunct OR planet_name casts an aspect onto target_house.
    """
    if not isinstance(source_house, int) or not isinstance(target_house, int):
        return False

    if not (1 <= source_house <= 12) or not (1 <= target_house <= 12):
        return False

    return is_conjunct(source_house, target_house) or casts_aspect(
        planet_name, source_house, target_house, include_node_aspects=include_node_aspects
    )

# --- Canonical Chart Level Helper Functions ---

def get_planet_house(canonical_chart: Any, planet_name: str) -> Optional[int]:
    """
    Returns the 1-based Whole Sign house number (1..12) from Lagna for a given planet_name in canonical_chart.
    Returns None if planet placement or Lagna is missing or invalid.
    """
    if not hasattr(canonical_chart, "placements") or not hasattr(canonical_chart, "ascendant"):
        return None
    placement = canonical_chart.placements.get(planet_name)
    if not placement or not hasattr(placement, "rashi") or not hasattr(canonical_chart.ascendant, "sign_index"):
        return None
    asc_sign_idx = canonical_chart.ascendant.sign_index
    p_sign_idx = placement.rashi.sign_index
    if not (1 <= asc_sign_idx <= 12) or not (1 <= p_sign_idx <= 12):
        return None
    return ((p_sign_idx - asc_sign_idx) % 12) + 1

def planets_conjunct(
    canonical_chart: Any,
    p1_name: str,
    p2_name: str
) -> bool:
    """Returns True if p1_name and p2_name occupy the exact same Whole Sign house in canonical_chart."""
    h1 = get_planet_house(canonical_chart, p1_name)
    h2 = get_planet_house(canonical_chart, p2_name)
    if h1 is None or h2 is None:
        return False
    return is_conjunct(h1, h2)

def planet_aspects_planet(
    canonical_chart: Any,
    source_planet: str,
    target_planet: str,
    include_node_aspects: bool = DEFAULT_INCLUDE_NODE_ASPECTS
) -> bool:
    """
    Returns True if source_planet casts a Parashari aspect onto target_planet's Whole Sign house in canonical_chart.
    Conjunction (same house) returns False.
    """
    h_source = get_planet_house(canonical_chart, source_planet)
    h_target = get_planet_house(canonical_chart, target_planet)
    if h_source is None or h_target is None:
        return False
    return casts_aspect(source_planet, h_source, h_target, include_node_aspects=include_node_aspects)

def planets_have_relationship(
    canonical_chart: Any,
    p1_name: str,
    p2_name: str,
    include_node_aspects: bool = DEFAULT_INCLUDE_NODE_ASPECTS
) -> bool:
    """
    Returns True if p1_name and p2_name are conjunct OR if either planet casts an aspect onto the other.
    """
    h1 = get_planet_house(canonical_chart, p1_name)
    h2 = get_planet_house(canonical_chart, p2_name)
    if h1 is None or h2 is None:
        return False
    return (
        is_conjunct(h1, h2)
        or casts_aspect(p1_name, h1, h2, include_node_aspects=include_node_aspects)
        or casts_aspect(p2_name, h2, h1, include_node_aspects=include_node_aspects)
    )

def get_aspecting_planets_for_house(
    canonical_chart_or_map: Any,
    target_house: int,
    include_node_aspects: bool = DEFAULT_INCLUDE_NODE_ASPECTS
) -> List[str]:
    """
    Returns list of planet names that cast an aspect onto target_house (1..12).
    Accepts either CanonicalVedicChart or planet_house_map Dict[str, int].
    Excludes conjunct planets in the same house.
    """
    if not isinstance(target_house, int) or not (1 <= target_house <= 12):
        return []

    aspecting = []
    if isinstance(canonical_chart_or_map, dict):
        house_map = canonical_chart_or_map
        for p_name, p_house in house_map.items():
            if isinstance(p_house, int) and (1 <= p_house <= 12):
                if casts_aspect(p_name, p_house, target_house, include_node_aspects=include_node_aspects):
                    aspecting.append(p_name)
    elif hasattr(canonical_chart_or_map, "placements"):
        for p_name in canonical_chart_or_map.placements.keys():
            pHouse = get_planet_house(canonical_chart_or_map, p_name)
            if pHouse is not None:
                if casts_aspect(p_name, pHouse, target_house, include_node_aspects=include_node_aspects):
                    aspecting.append(p_name)

    return aspecting
