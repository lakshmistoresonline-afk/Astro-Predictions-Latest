"""
Canonical Parashari Planetary Aspect & Conjunction Engine for Astrovision.
Strictly separates Conjunction (same Whole Sign house) from Cast Aspect (4th, 7th, 8th, etc. across houses).
Unified API supporting both integer Whole Sign house numbers (1..12) and CanonicalVedicChart planet-to-planet lookups.
"""
from typing import Dict, List, Optional, Set, Tuple, Union, Any

def get_house_distance(source_house: int, target_house: int) -> int:
    """Returns 0-based Whole Sign house distance from source_house to target_house in [0, 11]."""
    dist = (target_house - source_house) % 12
    return dist if dist >= 0 else dist + 12

def is_conjunct(house_A: Union[int, Any], house_B: Union[int, Any]) -> bool:
    """Returns True if house_A and house_B represent the identical Whole Sign house."""
    if isinstance(house_A, int) and isinstance(house_B, int):
        return house_A == house_B
    return False

def get_planet_house(canonical_chart: Any, planet_name: str) -> Optional[int]:
    """
    Returns the 1-based Whole Sign house number (1..12) from Lagna for a given planet_name in canonical_chart.
    Returns None if planet placement or Lagna is missing.
    """
    if not hasattr(canonical_chart, "placements") or not hasattr(canonical_chart, "ascendant"):
        return None
    placement = canonical_chart.placements.get(planet_name)
    if not placement:
        return None
    asc_sign_idx = canonical_chart.ascendant.sign_index
    p_sign_idx = placement.rashi.sign_index
    return ((p_sign_idx - asc_sign_idx) % 12) + 1

def casts_aspect(
    planet_name: str,
    source_house: Union[int, str],
    target_house: Union[int, Any]
) -> bool:
    """
    Evaluates whether planet_name in source_house casts a Parashari aspect onto target_house.
    Conjunction (source_house == target_house) is NOT an aspect and returns False.
    Supports either integer 1-based house numbers or (planet_name, target_planet_name, canonical_chart).
    """
    # Overload handling for planet_name, target_planet, canonical_chart
    if isinstance(source_house, str) and hasattr(target_house, "placements"):
        canonical_chart = target_house
        target_planet = source_house
        h_source = get_planet_house(canonical_chart, planet_name)
        h_target = get_planet_house(canonical_chart, target_planet)
        if h_source is None or h_target is None:
            return False
        source_house = h_source
        target_house = h_target

    if not isinstance(source_house, int) or not isinstance(target_house, int):
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

    # Rahu/Ketu special aspects: 5th, 7th, 9th
    if planet_name in ["Rahu", "Ketu"] and house_offset in [5, 7, 9]:
        return True

    return False

def planet_has_relationship(
    planet_name: str,
    source_house: Union[int, str],
    target_house: Union[int, Any]
) -> bool:
    """
    Returns True if source_house and target_house are conjunct OR planet casts an aspect.
    Supports either integer 1-based house numbers or (planet_name, target_planet_name, canonical_chart).
    """
    # Overload handling for planet_name, target_planet, canonical_chart
    if isinstance(source_house, str) and hasattr(target_house, "placements"):
        canonical_chart = target_house
        target_planet = source_house
        h_source = get_planet_house(canonical_chart, planet_name)
        h_target = get_planet_house(canonical_chart, target_planet)
        if h_source is None or h_target is None:
            return False
        source_house = h_source
        target_house = h_target

    if not isinstance(source_house, int) or not isinstance(target_house, int):
        return False

    return is_conjunct(source_house, target_house) or casts_aspect(planet_name, source_house, target_house)

def get_aspecting_planets_for_house(
    target_house: int,
    planet_house_map: Dict[str, int]
) -> List[str]:
    """Returns list of planet names that cast an aspect onto target_house (excluding conjunct planets)."""
    aspecting = []
    for p_name, p_house in planet_house_map.items():
        if casts_aspect(p_name, p_house, target_house):
            aspecting.append(p_name)
    return aspecting
