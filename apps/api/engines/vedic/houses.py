"""
Whole Sign House System Metadata Module for Astrovision.
Maps the 12 houses to zodiac signs based on the canonical Ascendant sign.
"""
from typing import List
from apps.api.engines.vedic.models import WholeSignHouse, RashiPosition
from apps.api.engines.vedic.rashi import ZODIAC_SIGNS

def generate_whole_sign_houses(ascendant_rashi: RashiPosition) -> List[WholeSignHouse]:
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
