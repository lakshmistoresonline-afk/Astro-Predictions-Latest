"""
Independent Chart State for Oracle Rule Validation.
Strictly decoupled from production CanonicalVedicChart.
"""

from typing import Dict, Optional

class IndependentPlanet:
    def __init__(self, name: str, longitude: float):
        self.name = name
        self.longitude = longitude % 360.0
        self.sign_index = int(self.longitude / 30.0) % 12 + 1
        self.sign_name = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                          "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"][self.sign_index - 1]

class IndependentChart:
    def __init__(self, ascendant_longitude: float):
        self.ascendant_longitude = ascendant_longitude % 360.0
        self.ascendant_sign_index = int(self.ascendant_longitude / 30.0) % 12 + 1
        self.planets: Dict[str, IndependentPlanet] = {}

    def add_planet(self, name: str, longitude: float):
        self.planets[name] = IndependentPlanet(name, longitude)

    def get_house(self, planet_name: str) -> Optional[int]:
        if planet_name not in self.planets:
            return None
        p_sign = self.planets[planet_name].sign_index
        return (p_sign - self.ascendant_sign_index) % 12 + 1

    def get_house_from_moon(self, planet_name: str) -> Optional[int]:
        if "Moon" not in self.planets or planet_name not in self.planets:
            return None
        moon_sign = self.planets["Moon"].sign_index
        p_sign = self.planets[planet_name].sign_index
        return (p_sign - moon_sign) % 12 + 1
