"""
Authoritative Ashtakavarga Kakshya Micro-Transit Engine for Astrovision.
Divides every 30° zodiac sign into 8 Kakshyas of 3°45' (3.75°) each:
1. Saturn  (0°00' - 3°45')
2. Jupiter (3°45' - 7°30')
3. Mars    (7°30' - 11°15')
4. Sun     (11°15' - 15°00')
5. Venus   (15°00' - 18°45')
6. Mercury (18°45' - 22°30')
7. Moon    (22°30' - 26°15')
8. Lagna   (26°15' - 30°00')

Determines Kakshya lord for any longitude and evaluates whether transiting planets
pass through a BAV bindu-contributing Kakshya in real-time.
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

KAKSHYA_LORDS = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Lagna"]
KAKSHYA_SPAN_DEG = 3.75  # 3°45'

class KakshyaPosition(BaseModel):
    sign_index: int  # 1-indexed (1=Aries .. 12=Pisces)
    sign_name: str
    degree_in_sign: float
    kakshya_number: int  # 1 to 8
    kakshya_lord: str
    kakshya_start_deg: float
    kakshya_end_deg: float

class KakshyaTransitTrigger(BaseModel):
    transiting_planet: str
    sign_name: str
    transit_longitude: float
    kakshya_lord: str
    has_bav_bindu: bool
    trigger_status: str = Field(description="ACTIVE_MICRO_TRIGGER or PASSIVE_TRANSIT")
    description: str

class KakshyaEngine:

    @classmethod
    def get_kakshya_position(cls, sidereal_longitude: float) -> KakshyaPosition:
        norm_lon = sidereal_longitude % 360.0
        sign_idx = int(norm_lon // 30.0) + 1
        deg_in_sign = norm_lon % 30.0

        kak_num = int(deg_in_sign // KAKSHYA_SPAN_DEG) + 1
        if kak_num > 8:
            kak_num = 8

        kak_lord = KAKSHYA_LORDS[kak_num - 1]
        start_d = (kak_num - 1) * KAKSHYA_SPAN_DEG
        end_d = kak_num * KAKSHYA_SPAN_DEG

        sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        s_name = sign_names[sign_idx - 1]

        return KakshyaPosition(
            sign_index=sign_idx,
            sign_name=s_name,
            degree_in_sign=deg_in_sign,
            kakshya_number=kak_num,
            kakshya_lord=kak_lord,
            kakshya_start_deg=start_d,
            kakshya_end_deg=end_d
        )

    @classmethod
    def evaluate_transit_trigger(cls, planet_name: str, transit_longitude: float, bav_bindus_for_lord: bool) -> KakshyaTransitTrigger:
        pos = cls.get_kakshya_position(transit_longitude)
        if bav_bindus_for_lord:
            status = "ACTIVE_MICRO_TRIGGER"
            desc = f"Transiting {planet_name} crosses {pos.sign_name} Kakshya {pos.kakshya_number} ({pos.kakshya_lord}'s zone). Bindu present: High-probability 3-5 day micro-event window."
        else:
            status = "PASSIVE_TRANSIT"
            desc = f"Transiting {planet_name} crosses {pos.sign_name} Kakshya {pos.kakshya_number} ({pos.kakshya_lord}'s zone). No bindu contributed by Kakshya lord."

        return KakshyaTransitTrigger(
            transiting_planet=planet_name,
            sign_name=pos.sign_name,
            transit_longitude=transit_longitude,
            kakshya_lord=pos.kakshya_lord,
            has_bav_bindu=bav_bindus_for_lord,
            trigger_status=status,
            description=desc
        )
