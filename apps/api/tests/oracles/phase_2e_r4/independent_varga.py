"""
Independent Divisional Chart (Varga) Calculations for R4 Oracle.
Computes varga sign index (1-12) for D1, D2, D3, D7, D9, D12, D30 directly from longitude.
Does NOT import VargaEngine.
"""
def calc_d1_sign(longitude: float) -> int:
    return int((longitude % 360.0) / 30.0) + 1

def calc_d2_hora_sign(longitude: float) -> int:
    rashi_idx = int((longitude % 360.0) / 30.0)
    deg_in_rashi = (longitude % 360.0) % 30.0
    is_odd = (rashi_idx % 2 == 0) # Aries (idx 0) is odd
    if is_odd:
        return 5 if deg_in_rashi < 15.0 else 4 # Sun (Leo 5) or Moon (Cancer 4)
    else:
        return 4 if deg_in_rashi < 15.0 else 5

def calc_d3_drekkana_sign(longitude: float) -> int:
    rashi_idx = int((longitude % 360.0) / 30.0)
    part = int(((longitude % 360.0) % 30.0) / 10.0)
    return ((rashi_idx + part * 4) % 12) + 1

def calc_d7_saptamamsa_sign(longitude: float) -> int:
    rashi_idx = int((longitude % 360.0) / 30.0)
    part = int(((longitude % 360.0) % 30.0) / (30.0 / 7.0))
    is_odd = (rashi_idx % 2 == 0)
    start_sign = rashi_idx if is_odd else (rashi_idx + 6) % 12
    return ((start_sign + part) % 12) + 1

def calc_d9_navamsa_sign(longitude: float) -> int:
    nav_index = int((longitude % 360.0) / (30.0 / 9.0))
    return (nav_index % 12) + 1

def calc_d12_dwadasamsa_sign(longitude: float) -> int:
    rashi_idx = int((longitude % 360.0) / 30.0)
    part = int(((longitude % 360.0) % 30.0) / 2.5)
    return ((rashi_idx + part) % 12) + 1

def calc_d30_trimshamsha_sign(longitude: float) -> int:
    rashi_idx = int((longitude % 360.0) / 30.0)
    deg = (longitude % 360.0) % 30.0
    is_odd = (rashi_idx % 2 == 0)
    if is_odd:
        if deg < 5.0: return 1   # Aries
        elif deg < 10.0: return 11 # Aquarius
        elif deg < 18.0: return 9  # Sagittarius
        elif deg < 25.0: return 3  # Gemini
        else: return 7           # Libra
    else:
        if deg < 5.0: return 2   # Taurus
        elif deg < 12.0: return 6  # Virgo
        elif deg < 20.0: return 12 # Pisces
        elif deg < 25.0: return 10 # Capricorn
        else: return 8           # Scorpio

def get_all_7_varga_signs(longitude: float) -> dict:
    return {
        "D1_Rashi": calc_d1_sign(longitude),
        "D2_Hora": calc_d2_hora_sign(longitude),
        "D3_Drekkana": calc_d3_drekkana_sign(longitude),
        "D7_Saptamamsa": calc_d7_saptamamsa_sign(longitude),
        "D9_Navamsa": calc_d9_navamsa_sign(longitude),
        "D12_Dwadasamsa": calc_d12_dwadasamsa_sign(longitude),
        "D30_Trimshamsha": calc_d30_trimshamsha_sign(longitude)
    }
