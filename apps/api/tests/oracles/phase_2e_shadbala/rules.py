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
DEBILITATION_DEGREES = {
    "Sun": 190.0,
    "Moon": 213.0,
    "Mars": 118.0,
    "Mercury": 345.0,
    "Jupiter": 275.0,
    "Venus": 177.0,
    "Saturn": 20.0
}

def independent_uccha_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets:
        return 0.0
    lon = chart.planets[planet].longitude
    deb_point_lon = DEBILITATION_DEGREES[planet]

    angular_dist = abs(lon - deb_point_lon) % 360.0
    dist_from_deb = min(angular_dist, 360.0 - angular_dist)

    return (dist_from_deb / 180.0) * 60.0

def independent_dig_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets:
        return 0.0
        
    asc_lon = chart.ascendant_longitude
    mc_lon = chart.mc_longitude
    ic_lon = (mc_lon + 180) % 360.0
    desc_lon = (asc_lon + 180) % 360.0
    
    if planet in ["Sun", "Mars"]: power_lon = mc_lon
    elif planet in ["Jupiter", "Mercury"]: power_lon = asc_lon
    elif planet == "Saturn": power_lon = desc_lon
    else: power_lon = ic_lon
    
    powerless_lon = (power_lon + 180) % 360.0
    p_lon = chart.planets[planet].longitude
    
    dist = abs(p_lon - powerless_lon) % 360.0
    dist = min(dist, 360.0 - dist)
    return (dist / 180.0) * 60.0

def independent_kala_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets or "Sun" not in chart.planets or "Moon" not in chart.planets:
        return 0.0
        
    sun_lon = chart.planets["Sun"].longitude
    moon_lon = chart.planets["Moon"].longitude
    ic_lon = (chart.mc_longitude + 180) % 360.0
    p_lon = chart.planets[planet].longitude
    
    # Nathonnatha
    dist_mid = min(abs(sun_lon - ic_lon) % 360.0, 360.0 - abs(sun_lon - ic_lon) % 360.0)
    diurnal = (dist_mid / 180.0) * 60.0
    nocturnal = 60.0 - diurnal
    
    if planet in ["Sun", "Jupiter", "Venus"]: nathonnatha = diurnal
    elif planet in ["Moon", "Mars", "Saturn"]: nathonnatha = nocturnal
    else: nathonnatha = 60.0
    
    # Paksha
    paksha_ang = min((moon_lon - sun_lon) % 360.0, 360.0 - (moon_lon - sun_lon) % 360.0)
    paksha_val = (paksha_ang / 180.0) * 60.0
    paksha = paksha_val if planet in ["Moon", "Mercury", "Jupiter", "Venus"] else (60.0 - paksha_val)
    
    # Ayana
    trop_lon = (p_lon + chart.ayanamsha) % 360.0
    import math
    kranti = 23.44 * math.sin(math.radians(trop_lon))
    if planet in ["Sun", "Mars", "Jupiter", "Venus", "Mercury"]: ayana = (24 + kranti) * 1.25
    else: ayana = (24 - kranti) * 1.25
    ayana = max(0.0, min(60.0, ayana))
    
    return nathonnatha + paksha + ayana

def independent_cheshta_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets or "Sun" not in chart.planets or "Moon" not in chart.planets:
        return 0.0
    if planet == "Sun":
        p_lon = chart.planets[planet].longitude
        trop_lon = (p_lon + chart.ayanamsha) % 360.0
        import math
        kranti = 23.44 * math.sin(math.radians(trop_lon))
        ayana = (24 + kranti) * 1.25
        return max(0.0, min(60.0, ayana))
    elif planet == "Moon":
        sun_lon = chart.planets["Sun"].longitude
        moon_lon = chart.planets["Moon"].longitude
        paksha_ang = (moon_lon - sun_lon) % 360.0
        if paksha_ang > 180: paksha_ang = 360.0 - paksha_ang
        return (paksha_ang / 180.0) * 60.0
    else:
        return 60.0 if chart.planets[planet].retrograde else 30.0

def independent_naisargika_bala(chart: IndependentChart, planet: str) -> float:
    return NAISARGIKA_BALA.get(planet, 0.0)

def independent_drik_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets: return 0.0
    val = 0.0
    p_lon = chart.planets[planet].longitude
    for asp_name, asp_p in chart.planets.items():
        if asp_name == planet: continue
        ang = abs(p_lon - asp_p.longitude) % 360.0
        if ang > 180: ang = 360.0 - ang
        if 150 <= ang <= 180:
            s = (ang - 150) * 2.0
            if asp_name in ["Jupiter", "Venus", "Moon", "Mercury"]: val += s / 4.0
            else: val -= s / 4.0
    return val

SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
]

NATURAL_FRIENDSHIP = {
    "Sun": {"Moon": 1, "Mars": 1, "Jupiter": 1, "Mercury": 0, "Venus": -1, "Saturn": -1},
    "Moon": {"Sun": 1, "Mercury": 1, "Mars": 0, "Jupiter": 0, "Venus": 0, "Saturn": 0},
    "Mars": {"Sun": 1, "Moon": 1, "Jupiter": 1, "Venus": 0, "Saturn": 0, "Mercury": -1},
    "Mercury": {"Sun": 1, "Venus": 1, "Mars": 0, "Jupiter": 0, "Saturn": 0, "Moon": -1},
    "Jupiter": {"Sun": 1, "Moon": 1, "Mars": 1, "Saturn": 0, "Mercury": -1, "Venus": -1},
    "Venus": {"Mercury": 1, "Saturn": 1, "Mars": 0, "Jupiter": 0, "Sun": -1, "Moon": -1},
    "Saturn": {"Mercury": 1, "Venus": 1, "Jupiter": 0, "Sun": -1, "Moon": -1, "Mars": -1}
}

def independent_sapta_vargaja(chart: IndependentChart, planet: str, varga_suite) -> float:
    vargas_to_check = ["D1_Rashi", "D2_Hora", "D3_Drekkana", "D7_Saptamamsa", "D9_Navamsa", "D12_Dwadasamsa", "D30_Trimshamsha"]
    score = 0.0
    p_lon = chart.planets[planet].longitude
    
    for div in vargas_to_check:
        if div not in varga_suite.vargas: continue
        v_chart = varga_suite.vargas[div]
        if planet not in v_chart.placements: continue
            
        v_sign_idx = v_chart.placements[planet].varga_sign_index - 1
        lord = SIGN_LORDS[v_sign_idx]
        
        if lord == planet:
            score += 30.0
        else:
            lord_lon = chart.planets[lord].longitude
            nat = NATURAL_FRIENDSHIP[planet].get(lord, 0)
            p_sign = int(p_lon / 30)
            l_sign = int(lord_lon / 30)
            dist = (l_sign - p_sign) % 12
            tat = 1 if dist in [1, 2, 3, 9, 10, 11] else -1
            maitri = nat + tat
            
            if maitri == 2: score += 22.5
            elif maitri == 1: score += 15.0
            elif maitri == 0: score += 7.5
            elif maitri == -1: score += 3.75
            elif maitri == -2: score += 1.875
    return score

def independent_ojha_yugma(chart: IndependentChart, planet: str, varga_suite) -> float:
    score = 0.0
    d1_sign = chart.planets[planet].sign_index
    if planet in ["Venus", "Moon"]:
        if d1_sign % 2 == 0: score += 15.0
    else:
        if d1_sign % 2 != 0: score += 15.0
        
    if "D9_Navamsa" in varga_suite.vargas and planet in varga_suite.vargas["D9_Navamsa"].placements:
        d9_sign = varga_suite.vargas["D9_Navamsa"].placements[planet].varga_sign_index
        if planet in ["Venus", "Moon"]:
            if d9_sign % 2 == 0: score += 15.0
        else:
            if d9_sign % 2 != 0: score += 15.0
    return score

def independent_kendradi(chart: IndependentChart, planet: str) -> float:
    house = chart.get_house(planet)
    if house in [1, 4, 7, 10]: return 60.0
    if house in [2, 5, 8, 11]: return 30.0
    return 15.0

def independent_drekkana(chart: IndependentChart, planet: str) -> float:
    deg = chart.planets[planet].longitude % 30
    drekkana = int(deg / 10) + 1
    if planet in ["Sun", "Mars", "Jupiter"] and drekkana == 1: return 15.0
    if planet in ["Mercury", "Saturn"] and drekkana == 2: return 15.0
    if planet in ["Moon", "Venus"] and drekkana == 3: return 15.0
    return 0.0

def independent_total_shadbala(chart: IndependentChart, planet: str, varga_suite=None) -> float:
    uccha = independent_uccha_bala(chart, planet)
    if varga_suite:
        sapta = independent_sapta_vargaja(chart, planet, varga_suite)
        ojha = independent_ojha_yugma(chart, planet, varga_suite)
    else:
        sapta = 0.0
        ojha = 0.0
    kendradi = independent_kendradi(chart, planet)
    drekkana = independent_drekkana(chart, planet)
    
    sthana = uccha + sapta + ojha + kendradi + drekkana
    dig = independent_dig_bala(chart, planet)
    kala = independent_kala_bala(chart, planet)
    cheshta = independent_cheshta_bala(chart, planet)
    naisargika = independent_naisargika_bala(chart, planet)
    drik = independent_drik_bala(chart, planet)
    
    return sthana + dig + kala + cheshta + naisargika + drik
