"""
Canonical Parashari Planetary Aspect & Conjunction Engine for Astrovision.
Strictly separates Conjunction (same house) from Cast Aspect (4th, 7th, 8th, etc. across houses).
"""
from typing import Dict, List, Set, Tuple

def get_house_distance(source_house: int, target_house: int) -> int:
    """Returns 0-based Whole Sign house distance from source_house to target_house in [0, 11]."""
    dist = (target_house - source_house) % 12
    return dist if dist >= 0 else dist + 12

def is_conjunct(house_A: int, house_B: int) -> bool:
    """Returns True if house_A and house_B are identical (co-location / conjunction)."""
    return house_A == house_B

def casts_aspect(planet_name: str, source_house: int, target_house: int) -> bool:
    """
    Evaluates whether planet_name in source_house casts a Parashari aspect onto target_house.
    Conjunction (source_house == target_house) is NOT an aspect and returns False.
    """
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

def planet_has_relationship(planet_name: str, source_house: int, target_house: int) -> bool:
    """Returns True if source_house and target_house are conjunct OR planet casts an aspect."""
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
