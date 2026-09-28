"""
Independent Chart State for Oracle Shadbala Rule Validation.
Strictly decoupled from production CanonicalVedicChart.
"""
from typing import Dict, Optional

class IndependentPlanet:
    def __init__(self, name: str, longitude: float, retrograde: bool = False):
        self.name = name
        self.longitude = longitude % 360.0
        self.sign_index = int(self.longitude / 30.0) % 12 + 1
        self.retrograde = retrograde

class IndependentChart:
    def __init__(self, ascendant_longitude: float, mc_longitude: float = 0.0, ayanamsha: float = 23.85):
        self.ascendant_longitude = ascendant_longitude % 360.0
        self.ascendant_sign_index = int(self.ascendant_longitude / 30.0) % 12 + 1
        self.mc_longitude = mc_longitude % 360.0
        self.ayanamsha = ayanamsha
        self.planets: Dict[str, IndependentPlanet] = {}

    def add_planet(self, name: str, longitude: float, retrograde: bool = False):
        self.planets[name] = IndependentPlanet(name, longitude, retrograde)

    def get_house(self, planet_name: str) -> Optional[int]:
        if planet_name not in self.planets:
            return None
        p_sign = self.planets[planet_name].sign_index
        return (p_sign - self.ascendant_sign_index) % 12 + 1


