"""
Independent Planetary Dignity Logic for Oracle.
"""
from typing import Dict, List

INDEPENDENT_OWN_SIGNS = {
    "Sun": [5],
    "Moon": [4],
    "Mars": [1, 8],
    "Mercury": [3, 6],
    "Jupiter": [9, 12],
    "Venus": [2, 7],
    "Saturn": [10, 11]
}

INDEPENDENT_EXALTATION = {
    "Sun": 1, "Moon": 2, "Mars": 10, "Mercury": 6,
    "Jupiter": 4, "Venus": 12, "Saturn": 7, "Rahu": 2, "Ketu": 8
}

INDEPENDENT_DEBILITATION = {
    "Sun": 7, "Moon": 8, "Mars": 4, "Mercury": 12,
    "Jupiter": 10, "Venus": 6, "Saturn": 1, "Rahu": 8, "Ketu": 2
}

def is_own_sign(planet: str, sign_index: int) -> bool:
    return sign_index in INDEPENDENT_OWN_SIGNS.get(planet, [])

def is_exalted(planet: str, sign_index: int) -> bool:
    return sign_index == INDEPENDENT_EXALTATION.get(planet, -1)

def is_debilitated(planet: str, sign_index: int) -> bool:
    return sign_index == INDEPENDENT_DEBILITATION.get(planet, -1)

def is_kendra(house: int) -> bool:
    return house in [1, 4, 7, 10]

def is_dusthana(house: int) -> bool:
    return house in [6, 8, 12]
