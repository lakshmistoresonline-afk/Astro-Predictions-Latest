"""
Independent Chart State for Oracle Ashtakavarga Rule Validation.
Strictly decoupled from production CanonicalVedicChart.
"""
from typing import Dict, Optional

class IndependentPlanet:
    def __init__(self, name: str, longitude: float):
        self.name = name
        self.longitude = longitude % 360.0
        self.sign_index = int(self.longitude / 30.0) % 12 + 1

class IndependentChart:
    def __init__(self, ascendant_longitude: float):
        self.ascendant_longitude = ascendant_longitude % 360.0
        self.ascendant_sign_index = int(self.ascendant_longitude / 30.0) % 12 + 1
        self.planets: Dict[str, IndependentPlanet] = {}

    def add_planet(self, name: str, longitude: float):
        self.planets[name] = IndependentPlanet(name, longitude)

    def get_planet_sign_index(self, planet_name: str) -> Optional[int]:
        if planet_name == "Ascendant":
            return self.ascendant_sign_index
        if planet_name not in self.planets:
            return None
        return self.planets[planet_name].sign_index
