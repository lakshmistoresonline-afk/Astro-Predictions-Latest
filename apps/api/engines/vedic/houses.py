"""
Whole Sign House System Metadata Module for Astrovision.
Maps the 12 houses to zodiac signs based on the canonical Ascendant sign.
Section 5 & 7 Compliance: Centralized get_house_from_lagna and get_relative_house_distance helpers!
"""
from typing import List, Optional, Any
from apps.api.engines.vedic.models import WholeSignHouse, RashiPosition
from apps.api.engines.vedic.rashi import ZODIAC_SIGNS

def get_house_from_lagna(planet_rashi_index: int, lagna_rashi_index: int) -> int:
    """
    Returns 1-based Whole Sign house number relative to Lagna Rashi index.
    planet_rashi_index and lagna_rashi_index must be 1-based (1 = Aries, 12 = Pisces).
    """
    if not (1 <= planet_rashi_index <= 12) or not (1 <= lagna_rashi_index <= 12):
        raise ValueError("rashi indexes must be between 1 and 12")
    return ((planet_rashi_index - lagna_rashi_index) % 12) + 1

def get_relative_house_distance(source_house: int, target_house: int) -> int:
    """
    Returns 1-based Whole Sign relative house distance from source_house to target_house (1..12).
    Same house = 1, 7th house = 7, 4th house = 4, 8th house = 8, 5th house = 5, 9th house = 9, 3rd = 3, 10th = 10.
    """
    if not (1 <= source_house <= 12) or not (1 <= target_house <= 12):
        raise ValueError("source_house and target_house must be between 1 and 12")
    return ((target_house - source_house) % 12) + 1

def generate_whole_sign_houses(
    ascendant_rashi: RashiPosition,
    placements: Optional[Any] = None
) -> List[WholeSignHouse]:
    """
    Generates Whole Sign house metadata starting from the Ascendant's sign.
    House 1 is the complete sign of the Ascendant.
    """
    asc_sign_idx = ascendant_rashi.sign_index - 1 # 0-indexed (0 = Aries)
    houses: List[WholeSignHouse] = []

    for house_num in range(1, 13):
        current_sign_idx = (asc_sign_idx + house_num - 1) % 12
        sign_name = ZODIAC_SIGNS[current_sign_idx]
        start_lon = current_sign_idx * 30.0
        end_lon = (current_sign_idx + 1) * 30.0

        houses.append(WholeSignHouse(
            house_number=house_num,
            sign=sign_name,
            sign_index=current_sign_idx + 1,
            start_longitude=round(start_lon, 6),
            end_longitude=round(end_lon, 6)
        ))

    return houses
