"""
Independent Shadbala Rules for Oracle.
"""
import math
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

DEBILITATION_DEGREES = {
    "Sun": 190.0,
    "Moon": 213.0,
    "Mars": 118.0,
    "Mercury": 345.0,
    "Jupiter": 275.0,
    "Venus": 177.0,
    "Saturn": 20.0
}

AVG_DAILY_VELOCITY = {
    "Mars": 0.524,
    "Mercury": 1.20,
    "Jupiter": 0.083,
    "Venus": 1.20,
    "Saturn": 0.033
}

SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
]

VARA_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
HORA_SEQUENCE = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

NATURAL_FRIENDSHIP = {
    "Sun": {"Moon": 1, "Mars": 1, "Jupiter": 1, "Mercury": 0, "Venus": -1, "Saturn": -1},
    "Moon": {"Sun": 1, "Mercury": 1, "Mars": 0, "Jupiter": 0, "Venus": 0, "Saturn": 0},
    "Mars": {"Sun": 1, "Moon": 1, "Jupiter": 1, "Venus": 0, "Saturn": 0, "Mercury": -1},
    "Mercury": {"Sun": 1, "Venus": 1, "Mars": 0, "Jupiter": 0, "Saturn": 0, "Moon": -1},
    "Jupiter": {"Sun": 1, "Moon": 1, "Mars": 1, "Saturn": 0, "Mercury": -1, "Venus": -1},
    "Venus": {"Mercury": 1, "Saturn": 1, "Mars": 0, "Jupiter": 0, "Sun": -1, "Moon": -1},
    "Saturn": {"Mercury": 1, "Venus": 1, "Jupiter": 0, "Sun": -1, "Moon": -1, "Mars": -1}
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

def independent_sapta_vargaja(chart: IndependentChart, planet: str, varga_suite) -> float:
    vargas_to_check = ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]
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

    if "D9" in varga_suite.vargas and planet in varga_suite.vargas["D9"].placements:
        d9_sign = varga_suite.vargas["D9"].placements[planet].varga_sign_index
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

def independent_tribhaga(chart: IndependentChart, planet: str) -> float:
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
    kranti = 23.44 * math.sin(math.radians(trop_lon))
    if planet in ["Sun", "Mars", "Jupiter", "Venus", "Mercury"]: ayana = (24 + kranti) * 1.25
    else: ayana = (24 - kranti) * 1.25
    ayana = max(0.0, min(60.0, ayana))

    # Tribhaga
    tribhaga = independent_tribhaga(chart, planet)

    # Vara, Hora, Masa, Varsha
    jd = chart.julian_day
    weekday = int(jd + 1.5) % 7
    vara_lord = VARA_LORDS[weekday]
    hora_idx = (chart.hour - 6) % 24
    start_hora = HORA_SEQUENCE.index(vara_lord) if vara_lord in HORA_SEQUENCE else 0
    hora_lord = HORA_SEQUENCE[(start_hora + hora_idx) % 7]
    masa_lord = VARA_LORDS[(weekday + (chart.month * 2)) % 7]
    varsha_lord = VARA_LORDS[(weekday + (chart.year * 3)) % 7]

    vara = 45.0 if planet == vara_lord else 0.0
    hora = 60.0 if planet == hora_lord else 0.0
    masa = 30.0 if planet == masa_lord else 0.0
    varsha = 15.0 if planet == varsha_lord else 0.0

    return nathonnatha + paksha + ayana + tribhaga + vara + hora + masa + varsha

def independent_cheshta_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets or "Sun" not in chart.planets or "Moon" not in chart.planets:
        return 0.0
    if planet == "Sun":
        p_lon = chart.planets[planet].longitude
        trop_lon = (p_lon + chart.ayanamsha) % 360.0
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
        vel = chart.planets[planet].velocity
        avg_v = AVG_DAILY_VELOCITY[planet]
        if vel < 0: return 60.0
        elif abs(vel) < 0.005: return 15.0
        elif vel > 1.15 * avg_v: return 45.0
        elif 0.85 * avg_v <= vel <= 1.15 * avg_v: return 30.0
        else: return 15.0

def independent_naisargika_bala(chart: IndependentChart, planet: str) -> float:
    return NAISARGIKA_BALA.get(planet, 0.0)

def independent_drik_bala(chart: IndependentChart, planet: str) -> float:
    if planet not in chart.planets: return 0.0
    planets_to_eval = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    p_lon = chart.planets[planet].longitude
    drik_total = 0.0

    for asp_name in planets_to_eval:
        if asp_name == planet or asp_name not in chart.planets: continue
        asp_lon = chart.planets[asp_name].longitude
        dist = (p_lon - asp_lon) % 360.0

        drishti = 0.0
        if 30.0 <= dist <= 60.0: drishti = (dist - 30.0) * 0.5
        elif 60.0 < dist <= 90.0: drishti = (dist - 60.0) + 15.0
        elif 90.0 < dist <= 120.0: drishti = (120.0 - dist) * 1.5
        elif 120.0 < dist <= 150.0: drishti = 0.0
        elif 150.0 < dist <= 180.0: drishti = (dist - 150.0) * 2.0
        elif 180.0 < dist <= 300.0: drishti = (300.0 - dist) / 2.0

        if asp_name == "Mars":
            if 90.0 <= dist <= 120.0 or 210.0 <= dist <= 240.0: drishti += 15.0
        elif asp_name == "Jupiter":
            if 120.0 <= dist <= 150.0 or 240.0 <= dist <= 270.0: drishti += 30.0
        elif asp_name == "Saturn":
            if 60.0 <= dist <= 90.0 or 270.0 <= dist <= 300.0: drishti += 45.0

        drishti = min(60.0, drishti)

        is_benefic = asp_name in ["Jupiter", "Venus", "Moon", "Mercury"]
        if is_benefic: drik_total += drishti / 4.0
        else: drik_total -= drishti / 4.0

    return drik_total

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

