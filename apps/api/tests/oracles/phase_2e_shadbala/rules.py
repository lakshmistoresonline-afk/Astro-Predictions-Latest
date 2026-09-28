"""
Independent Shadbala Rules for Oracle.
"""
from apps.api.tests.oracles.phase_2e_shadbala.chart_state import IndependentChart

# Naisargika
NAISARGIKA_BALA = {
    "Sun": 60.0,
    "Moon": 51.43,
    "Venus": 42.85,
    "Jupiter": 34.28,
    "Mercury": 25.70,
    "Mars": 17.14,
    "Saturn": 8.57
}

# Dig Bala Power Houses (0-indexed house offsets from Ascendant)
DIG_BALA_HOUSES = {
    "Sun": 9,      # 10th House
    "Mars": 9,     # 10th House
    "Jupiter": 0,  # 1st House
    "Mercury": 0,  # 1st House
    "Saturn": 6,   # 7th House
    "Moon": 3,     # 4th House
    "Venus": 3     # 4th House
}

EXALTATION_SIGNS = {
    "Sun": 1, "Moon": 2, "Mars": 10, "Mercury": 6,
    "Jupiter": 4, "Venus": 12, "Saturn": 7
}
DEBILITATION_SIGNS = {
    "Sun": 7, "Moon": 8, "Mars": 4, "Mercury": 12,
    "Jupiter": 10, "Venus": 6, "Saturn": 1
}

def independent_uccha_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets:
        return 0.0
    lon = chart.planets[planet].longitude
    deb_sign = DEBILITATION_SIGNS[planet]
    deb_point_lon = (deb_sign - 1) * 30.0 + 15.0

    angular_dist = abs(lon - deb_point_lon) % 360.0
    dist_from_deb = min(angular_dist, 360.0 - angular_dist)

    return (dist_from_deb / 180.0) * 60.0

def independent_dig_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets:
        return 0.0

    power_house_idx = DIG_BALA_HOUSES[planet]
    p_house_idx = chart.get_house(planet) - 1 # 0-indexed

    house_dist = abs(p_house_idx - power_house_idx)
    if house_dist > 6:
        house_dist = 12 - house_dist

    return ((6 - house_dist) / 6.0) * 60.0

def independent_kala_bala(chart: IndependentChart, planet: str) -> float:
    return 30.0

def independent_cheshta_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets:
        return 0.0
    if planet in ["Sun", "Moon"]:
        return 60.0
    return 60.0 if chart.planets[planet].retrograde else 30.0

def independent_naisargika_bala(chart: IndependentChart, planet: str) -> float:
    return NAISARGIKA_BALA.get(planet, 0.0)

def independent_drik_bala(chart: IndependentChart, planet: str) -> float:
    return 15.0

def independent_total_shadbala(chart: IndependentChart, planet: str) -> float:
    sthana = independent_uccha_bala(chart, planet) + 30.0 + 15.0 + 30.0 + 15.0
    dig = independent_dig_bala(chart, planet)
    kala = independent_kala_bala(chart, planet)
    cheshta = independent_cheshta_bala(chart, planet)
    naisargika = independent_naisargika_bala(chart, planet)
    drik = independent_drik_bala(chart, planet)

    return sthana + dig + kala + cheshta + naisargika + drik
