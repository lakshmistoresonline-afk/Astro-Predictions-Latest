"""
Authoritative Gemstone Safety & Dignity Matrix Engine for Astrovision.
Evaluates Lagna Lord, Trikona Lords (5th & 9th), Dusthana Lords (6th, 8th, 12th),
Maraka Lords (2nd & 7th), and Badhaka Lords according to classical Parashari Jyotisha rules.

Categorizes Gemstones into:
- RECOMMENDED (Anukuul / Benefic) — Strengthens Lagna & Trikona lords for life success.
- NEUTRAL (Conditionally Permitted) — Permitted during specific Dasha activation under guidance.
- STRICTLY FORBIDDEN (Pratikool / Harmful) — Functional malefics, Marakas, or Badhakas that must NEVER be worn.
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

GEMSTONE_MAP = {
    "Sun": {"gemstone": "Ruby (Manikyam)", "substitute": "Red Garnet", "metal": "Gold / Copper", "finger": "Ring Finger"},
    "Moon": {"gemstone": "Natural Pearl (Moti)", "substitute": "Moonstone", "metal": "Silver", "finger": "Little Finger"},
    "Mars": {"gemstone": "Red Coral (Moonga)", "substitute": "Red Carnelian", "metal": "Copper / Gold", "finger": "Ring Finger"},
    "Mercury": {"gemstone": "Emerald (Panna)", "substitute": "Green Peridot", "metal": "Gold / Silver", "finger": "Little Finger"},
    "Jupiter": {"gemstone": "Yellow Sapphire (Pukhraj)", "substitute": "Yellow Topaz", "metal": "Gold", "finger": "Index Finger"},
    "Venus": {"gemstone": "Diamond (Hira)", "substitute": "White Sapphire", "metal": "Platinum / Silver", "finger": "Middle / Little Finger"},
    "Saturn": {"gemstone": "Blue Sapphire (Neelam)", "substitute": "Amethyst", "metal": "Iron / Silver", "finger": "Middle Finger"},
    "Rahu": {"gemstone": "Hessonite (Gomedh)", "substitute": "Honey Zircon", "metal": "Silver", "finger": "Middle Finger"},
    "Ketu": {"gemstone": "Cat's Eye (Vaidurya)", "substitute": "Chrysoberyl", "metal": "Silver", "finger": "Middle Finger"}
}

# Sign ownership (0-indexed: 0=Aries, 1=Taurus, ..., 11=Pisces)
SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
]

class GemstoneDignityItem(BaseModel):
    planet: str
    gemstone_name: str
    substitute: str
    suitable_metal: str
    wearing_finger: str
    lordship_role: str
    suitability_class: str = Field(description="RECOMMENDED, NEUTRAL, or STRICTLY_FORBIDDEN")
    rationale: str

class GemstoneDignityMatrix(BaseModel):
    lagna_sign: str
    lagna_lord: str
    recommendations: List[GemstoneDignityItem]

class GemstoneEngine:
    """
    Computes an authoritative Gemstone Dignity & Safety Matrix for any natal Lagna.
    """

    @classmethod
    def calculate_gemstone_matrix(cls, lagna_sign_index: int, lagna_sign_name: str) -> GemstoneDignityMatrix:
        # lagna_sign_index is 1-indexed (1=Aries .. 12=Pisces)
        l_idx = (lagna_sign_index - 1) % 12
        lagna_lord = SIGN_LORDS[l_idx]

        # Determine house lords for Lagna (1 to 12)
        house_lords = {}
        for h in range(1, 13):
            sign_idx = (l_idx + h - 1) % 12
            house_lords[h] = SIGN_LORDS[sign_idx]

        # Trikona lords (1, 5, 9)
        lord_1 = house_lords[1]
        lord_5 = house_lords[5]
        lord_9 = house_lords[9]

        # Dusthana lords (6, 8, 12)
        lord_6 = house_lords[6]
        lord_8 = house_lords[8]
        lord_12 = house_lords[12]

        # Maraka lords (2, 7)
        lord_2 = house_lords[2]
        lord_7 = house_lords[7]

        # Badhaka lord based on Lagna quadra
        # Movable (1, 4, 7, 10): 11th house
        # Fixed (2, 5, 8, 11): 9th house
        # Dual (3, 6, 9, 12): 7th house
        if lagna_sign_index in [1, 4, 7, 10]:
            badhaka_lord = house_lords[11]
        elif lagna_sign_index in [2, 5, 8, 11]:
            badhaka_lord = house_lords[9]
        else:
            badhaka_lord = house_lords[7]

        trikona_set = {lord_1, lord_5, lord_9}

        items = []
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            info = GEMSTONE_MAP[planet]

            if planet in [lord_1, lord_5, lord_9]:
                s_class = "RECOMMENDED"
                role = "Trikona / Lagna Lord (Benefic)"
                rationale = f"{planet} is a primary functional benefic for {lagna_sign_name} Lagna, ruling auspicious houses. Gemstone enhances overall life vitality and success."
            elif planet in [lord_6, lord_8, lord_12] and planet not in trikona_set:
                s_class = "STRICTLY_FORBIDDEN"
                role = "Dusthana Lord (6th/8th/12th)"
                rationale = f"{planet} rules a Dusthana house (6/8/12) for {lagna_sign_name} Lagna. Wearing its gemstone risks amplifying disease, obstacles, or losses."
            elif planet in [lord_2, lord_7] and planet not in trikona_set:
                s_class = "STRICTLY_FORBIDDEN"
                role = "Maraka Lord (2nd/7th)"
                rationale = f"{planet} acts as a Maraka lord for {lagna_sign_name} Lagna. Wearing its gemstone without specific remedial context is unsafe."
            elif planet == badhaka_lord and planet not in trikona_set:
                s_class = "STRICTLY_FORBIDDEN"
                role = "Badhaka Lord (Obstacle Planet)"
                rationale = f"{planet} acts as the Badhakadhipati (primary obstacle lord) for {lagna_sign_name} Lagna. Gemstone is forbidden."
            elif planet in ["Rahu", "Ketu"]:
                s_class = "NEUTRAL"
                role = "Shadow Node"
                rationale = f"{planet} is a shadow node. Gemstone requires explicit Dasha activation and individual chart verification."
            else:
                s_class = "NEUTRAL"
                role = "Kendradhipati / Neutral Lord"
                rationale = f"{planet} holds neutral or conditional lordship for {lagna_sign_name} Lagna. Gemstone is conditionally permitted."

            items.append(GemstoneDignityItem(
                planet=planet,
                gemstone_name=info["gemstone"],
                substitute=info["substitute"],
                suitable_metal=info["metal"],
                wearing_finger=info["finger"],
                lordship_role=role,
                suitability_class=s_class,
                rationale=rationale
            ))

        return GemstoneDignityMatrix(
            lagna_sign=lagna_sign_name,
            lagna_lord=lagna_lord,
            recommendations=items
        )
