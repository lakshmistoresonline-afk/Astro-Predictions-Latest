"""
Independent Shadbala Calculation Engine for R4 Oracle.
Computes Sthana, Dig, Kala, Cheshta, Naisargika, Drik Balas from IndependentChart without production calls.
"""
import math
from typing import Dict, Any

from apps.api.tests.oracles.phase_2e_r4.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4.independent_geometry import independent_declination, independent_drishti_pinda
from apps.api.tests.oracles.phase_2e_r4.independent_calendar import (
    get_independent_vara_lord, get_independent_hora_lord,
    get_independent_masa_lord, get_independent_varsha_lord
)
from apps.api.tests.oracles.phase_2e_r4.independent_varga import get_all_7_varga_signs
from apps.api.tests.oracles.phase_2e_r4.independent_constants import (
    DEBILITATION_DEGREES, NAISARGIKA_BALA_SHASHTIAMSAS, AVG_DAILY_VELOCITY,
    NATURAL_FRIENDSHIP, SIGN_LORDS
)

def r4_calc_uccha_bala(chart: IndependentChart, planet: str) -> float:
    p_lon = chart.planets[planet].longitude
    deb_lon = DEBILITATION_DEGREES[planet]
    angular_dist = abs(p_lon - deb_lon) % 360.0
    dist_from_deb = min(angular_dist, 360.0 - angular_dist)
    return (dist_from_deb / 180.0) * 60.0

def r4_calc_sapta_vargaja(chart: IndependentChart, planet: str) -> float:
    score = 0.0
    p_lon = chart.planets[planet].longitude
    vargas = get_all_7_varga_signs(p_lon)

    for div, v_sign in vargas.items():
        lord = SIGN_LORDS[v_sign - 1]
        if lord == planet:
            score += 30.0
        else:
            lord_lon = chart.planets[lord].longitude if lord in chart.planets else 0.0
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

def r4_calc_ojha_yugma(chart: IndependentChart, planet: str) -> float:
    score = 0.0
    d1_sign = chart.planets[planet].sign_index
    if planet in ["Venus", "Moon"]:
        if d1_sign % 2 == 0: score += 15.0
    else:
        if d1_sign % 2 != 0: score += 15.0

    vargas = get_all_7_varga_signs(chart.planets[planet].longitude)
    d9_sign = vargas["D9_Navamsa"]
    if planet in ["Venus", "Moon"]:
        if d9_sign % 2 == 0: score += 15.0
    else:
        if d9_sign % 2 != 0: score += 15.0

    return score

def r4_calc_kendradi(chart: IndependentChart, planet: str) -> float:
    house = chart.get_house(planet)
    if house in [1, 4, 7, 10]: return 60.0
    if house in [2, 5, 8, 11]: return 30.0
    return 15.0

def r4_calc_drekkana(chart: IndependentChart, planet: str) -> float:
    deg = chart.planets[planet].degree_in_sign
    drekkana = int(deg / 10.0) + 1
    if planet in ["Sun", "Mars", "Jupiter"] and drekkana == 1: return 15.0
    if planet in ["Mercury", "Saturn"] and drekkana == 2: return 15.0
    if planet in ["Moon", "Venus"] and drekkana == 3: return 15.0
    return 0.0

def r4_calc_dig_bala(chart: IndependentChart, planet: str) -> float:
    p_lon = chart.planets[planet].longitude
    asc_lon = chart.ascendant_longitude
    mc_lon = chart.mc_longitude
    ic_lon = chart.ic_longitude
    desc_lon = chart.descendant_longitude

    if planet in ["Sun", "Mars"]: power_lon = mc_lon
    elif planet in ["Jupiter", "Mercury"]: power_lon = asc_lon
    elif planet == "Saturn": power_lon = desc_lon
    else: power_lon = ic_lon

    powerless_lon = (power_lon + 180.0) % 360.0
    dist = abs(p_lon - powerless_lon) % 360.0
    dist = min(dist, 360.0 - dist)
    return (dist / 180.0) * 60.0

def r4_calc_tribhaga(chart: IndependentChart, planet: str) -> float:
    if planet == "Jupiter": return 60.0
    sun_house = chart.get_house("Sun")
    is_day = sun_house in [7, 8, 9, 10, 11, 12]
    if is_day:
        if sun_house in [11, 12] and planet == "Mercury": return 60.0
        if sun_house in [9, 10] and planet == "Sun": return 60.0
        if sun_house in [7, 8] and planet == "Saturn": return 60.0
    else:
        if sun_house in [5, 6] and planet == "Moon": return 60.0
        if sun_house in [3, 4] and planet == "Mars": return 60.0
        if sun_house in [1, 2] and planet == "Venus": return 60.0
    return 0.0

def r4_calc_kala_bala(chart: IndependentChart, planet: str) -> Dict[str, float]:
    sun_lon = chart.planets["Sun"].longitude
    moon_lon = chart.planets["Moon"].longitude
    p_lon = chart.planets[planet].longitude
    ic_lon = chart.ic_longitude

    # Nathonnatha
    dist_mid = abs(sun_lon - ic_lon) % 360.0
    dist_mid = min(dist_mid, 360.0 - dist_mid)
    diurnal = (dist_mid / 180.0) * 60.0
    nocturnal = 60.0 - diurnal

    if planet in ["Sun", "Jupiter", "Venus"]: nathonnatha = diurnal
    elif planet in ["Moon", "Mars", "Saturn"]: nathonnatha = nocturnal
    else: nathonnatha = 60.0

    # Paksha
    paksha_ang = (moon_lon - sun_lon) % 360.0
    if paksha_ang > 180.0: paksha_ang = 360.0 - paksha_ang
    paksha_val = (paksha_ang / 180.0) * 60.0
    paksha = paksha_val if planet in ["Moon", "Mercury", "Jupiter", "Venus"] else (60.0 - paksha_val)

    # Ayana
    kranti = independent_declination(p_lon, chart.ayanamsha)
    if planet in ["Sun", "Mars", "Jupiter", "Venus", "Mercury"]: ayana = (24.0 + kranti) * 1.25
    else: ayana = (24.0 - kranti) * 1.25
    ayana = max(0.0, min(60.0, ayana))

    # Tribhaga
    tribhaga = r4_calc_tribhaga(chart, planet)

    # Vara, Hora, Masa, Varsha
    vara_lord = get_independent_vara_lord(chart.julian_day)
    hora_lord = get_independent_hora_lord(chart.julian_day, chart.hour)
    masa_lord = get_independent_masa_lord(chart.julian_day, chart.month)
    varsha_lord = get_independent_varsha_lord(chart.julian_day, chart.year)

    vara = 45.0 if planet == vara_lord else 0.0
    hora = 60.0 if planet == hora_lord else 0.0
    masa = 30.0 if planet == masa_lord else 0.0
    varsha = 15.0 if planet == varsha_lord else 0.0

    total_kala = nathonnatha + paksha + ayana + tribhaga + vara + hora + masa + varsha

    return {
        "Nathonnatha Bala": round(nathonnatha, 2),
        "Paksha Bala": round(paksha, 2),
        "Ayana Bala": round(ayana, 2),
        "Tribhaga Bala": round(tribhaga, 2),
        "Vara Bala": round(vara, 2),
        "Hora Bala": round(hora, 2),
        "Masa Bala": round(masa, 2),
        "Varsha Bala": round(varsha, 2),
        "total_shashtiamsas": round(total_kala, 2)
    }

def r4_calc_cheshta_bala(chart: IndependentChart, planet: str) -> float:
    if planet == "Sun":
        kranti = independent_declination(chart.planets["Sun"].longitude, chart.ayanamsha)
        return max(0.0, min(60.0, (24.0 + kranti) * 1.25))
    elif planet == "Moon":
        sun_lon = chart.planets["Sun"].longitude
        moon_lon = chart.planets["Moon"].longitude
        paksha_ang = (moon_lon - sun_lon) % 360.0
        if paksha_ang > 180.0: paksha_ang = 360.0 - paksha_ang
        return (paksha_ang / 180.0) * 60.0
    else:
        vel = chart.planets[planet].velocity
        avg_v = AVG_DAILY_VELOCITY[planet]
        if vel < 0: return 60.0
        elif abs(vel) < 0.005: return 15.0
        elif vel > 1.15 * avg_v: return 45.0
        elif 0.85 * avg_v <= vel <= 1.15 * avg_v: return 30.0
        else: return 15.0

def r4_calc_drik_bala(chart: IndependentChart, planet: str) -> float:
    p_lon = chart.planets[planet].longitude
    drik_total = 0.0
    for asp_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if asp_name == planet or asp_name not in chart.planets: continue
        asp_lon = chart.planets[asp_name].longitude
        drishti = independent_drishti_pinda(asp_name, asp_lon, p_lon)
        is_benefic = asp_name in ["Jupiter", "Venus", "Moon", "Mercury"]
        if is_benefic: drik_total += drishti / 4.0
        else: drik_total -= drishti / 4.0
    return drik_total

def r4_calculate_shadbala_for_planet(chart: IndependentChart, planet: str) -> Dict[str, Any]:
    uccha = r4_calc_uccha_bala(chart, planet)
    sapta = r4_calc_sapta_vargaja(chart, planet)
    ojha = r4_calc_ojha_yugma(chart, planet)
    kendradi = r4_calc_kendradi(chart, planet)
    drekkana = r4_calc_drekkana(chart, planet)
    sthana_total = uccha + sapta + ojha + kendradi + drekkana

    dig = r4_calc_dig_bala(chart, planet)
    kala_dict = r4_calc_kala_bala(chart, planet)
    kala_total = kala_dict["total_shashtiamsas"]

    cheshta = r4_calc_cheshta_bala(chart, planet)
    naisargika = NAISARGIKA_BALA_SHASHTIAMSAS.get(planet, 0.0)
    drik = r4_calc_drik_bala(chart, planet)

    total_shasht = sthana_total + dig + kala_total + cheshta + naisargika + drik
    total_rupas = total_shasht / 60.0

    min_rupas = {"Sun": 5.0, "Moon": 6.0, "Mars": 5.0, "Mercury": 7.0, "Jupiter": 6.5, "Venus": 5.5, "Saturn": 5.0}
    percent = (total_rupas / min_rupas[planet]) * 100.0

    return {
        "sthana": round(sthana_total, 2),
        "uccha": round(uccha, 2),
        "sapta_vargaja": round(sapta, 2),
        "ojha_yugma": round(ojha, 2),
        "kendradi": round(kendradi, 2),
        "drekkana": round(drekkana, 2),
        "dig": round(dig, 2),
        "kala": round(kala_total, 2),
        "kala_sub": kala_dict,
        "cheshta": round(cheshta, 2),
        "naisargika": round(naisargika, 2),
        "drik": round(drik, 2),
        "total_shashtiamsas": round(total_shasht, 2),
        "total_rupas": round(total_rupas, 2),
        "strength_percentage": round(percent, 2)
    }
