"""
Authoritative Mathematical Rules for 16 Parashari Vargas (D1 through D60).
Operates strictly on full-precision sidereal longitudes without pre-rounding.
"""
import math
from typing import Tuple
from apps.api.engines.vedic.rashi import ZODIAC_SIGNS

VARGA_METADATA = {
    "D1": {"name": "Rashi", "number": 1, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D2": {"name": "Hora", "number": 2, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D3": {"name": "Drekkana", "number": 3, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D4": {"name": "Chaturthamsa", "number": 4, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D7": {"name": "Saptamsa", "number": 7, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D9": {"name": "Navamsa", "number": 9, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D10": {"name": "Dasamsa", "number": 10, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D12": {"name": "Dvadasamsa", "number": 12, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D16": {"name": "Shodasamsa", "number": 16, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D20": {"name": "Vimsamsa", "number": 20, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D24": {"name": "Chaturvimsamsa", "number": 24, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D27": {"name": "Saptavimsamsa", "number": 27, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D30": {"name": "Trimsamsa", "number": 30, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D40": {"name": "Khavedamsa", "number": 40, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D45": {"name": "Akshavedamsa", "number": 45, "source": "Brihat Parasara Hora Sastra Chapter 6"},
    "D60": {"name": "Shashtiamsa", "number": 60, "source": "Brihat Parasara Hora Sastra Chapter 6"},
}

def _get_sign_and_deg(sidereal_lon_deg: float) -> Tuple[int, float]:
    """Returns 1-based sign index (1..12) and degree within sign [0.0, 30.0)."""
    lon = sidereal_lon_deg % 360.0
    sign_idx = int(lon / 30.0) % 12 + 1
    deg_in_sign = lon % 30.0
    return sign_idx, deg_in_sign

def compute_varga_sign_and_div(division: str, sidereal_lon_deg: float) -> Tuple[int, str, int, float]:
    """
    Computes (varga_sign_index [1..12], varga_sign_name, division_index [1..N], degree_in_varga_sign).
    Enforces exact Parashari traditional algorithms for all 16 Vargas.
    """
    S, d = _get_sign_and_deg(sidereal_lon_deg)
    is_odd = (S % 2 == 1)

    # Classification of sign mobility
    # Movable (1, 4, 7, 10), Fixed (2, 5, 8, 11), Dual (3, 6, 9, 12)
    mod4 = S % 3
    is_movable = (mod4 == 1)
    is_fixed = (mod4 == 2)
    is_dual = (mod4 == 0)

    # Classification of elemental triad
    # Fiery (1, 5, 9), Earthy (2, 6, 10), Airy (3, 7, 11), Watery (4, 8, 12)
    mod_element = S % 4

    varga_sign_idx = S
    div_idx = 1
    effective_deg = d

    if division == "D1":
        varga_sign_idx = S
        div_idx = 1
        effective_deg = d

    elif division == "D2":
        # Hora (15 degrees per division)
        div_idx = 1 if d < 15.0 else 2
        effective_deg = (d % 15.0) * 2.0
        if is_odd:
            varga_sign_idx = 5 if div_idx == 1 else 4 # Sun (Leo=5) or Moon (Cancer=4)
        else:
            varga_sign_idx = 4 if div_idx == 1 else 5 # Moon (Cancer=4) or Sun (Leo=5)

    elif division == "D3":
        # Drekkana (10 degrees per division)
        div_idx = min(int(d / 10.0) + 1, 3)
        effective_deg = (d % 10.0) * 3.0
        if div_idx == 1:
            varga_sign_idx = S
        elif div_idx == 2:
            varga_sign_idx = (S - 1 + 4) % 12 + 1
        else:
            varga_sign_idx = (S - 1 + 8) % 12 + 1

    elif division == "D4":
        # Chaturthamsa (7.5 degrees per division)
        div_idx = min(int(d / 7.5) + 1, 4)
        effective_deg = (d % 7.5) * 4.0
        varga_sign_idx = (S - 1 + (div_idx - 1) * 3) % 12 + 1

    elif division == "D7":
        # Saptamsa (30/7 degrees per division)
        seg = 30.0 / 7.0
        div_idx = min(int(d / seg) + 1, 7)
        effective_deg = (d % seg) * 7.0
        start = S if is_odd else (S - 1 + 6) % 12 + 1
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    elif division == "D9":
        # Navamsa (3.3333333 degrees per division)
        seg = 30.0 / 9.0
        div_idx = min(int(d / seg) + 1, 9)
        effective_deg = (d % seg) * 9.0
        if is_movable:
            start = S
        elif is_fixed:
            start = (S - 1 + 8) % 12 + 1
        else: # Dual
            start = (S - 1 + 4) % 12 + 1
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    elif division == "D10":
        # Dasamsa (3.0 degrees per division)
        div_idx = min(int(d / 3.0) + 1, 10)
        effective_deg = (d % 3.0) * 10.0
        start = S if is_odd else (S - 1 + 8) % 12 + 1
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    elif division == "D12":
        # Dvadasamsa (2.5 degrees per division)
        div_idx = min(int(d / 2.5) + 1, 12)
        effective_deg = (d % 2.5) * 12.0
        varga_sign_idx = (S - 1 + div_idx - 1) % 12 + 1

    elif division == "D16":
        # Shodasamsa (1.875 degrees per division)
        seg = 30.0 / 16.0
        div_idx = min(int(d / seg) + 1, 16)
        effective_deg = (d % seg) * 16.0
        start = 1 if is_movable else (5 if is_fixed else 9)
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    elif division == "D20":
        # Vimsamsa (1.5 degrees per division)
        seg = 30.0 / 20.0
        div_idx = min(int(d / seg) + 1, 20)
        effective_deg = (d % seg) * 20.0
        start = 1 if is_movable else (9 if is_fixed else 5)
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    elif division == "D24":
        # Chaturvimsamsa (1.25 degrees per division)
        seg = 30.0 / 24.0
        div_idx = min(int(d / seg) + 1, 24)
        effective_deg = (d % seg) * 24.0
        start = 5 if is_odd else 4 # Leo (5) for odd, Cancer (4) for even
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    elif division == "D27":
        # Saptavimsamsa (30/27 degrees per division)
        seg = 30.0 / 27.0
        div_idx = min(int(d / seg) + 1, 27)
        effective_deg = (d % seg) * 27.0
        if mod_element == 1: # Fiery (1, 5, 9)
            start = 1 # Aries
        elif mod_element == 2: # Earthy (2, 6, 10)
            start = 4 # Cancer
        elif mod_element == 3: # Airy (3, 7, 11)
            start = 7 # Libra
        else: # Watery (4, 8, 12)
            start = 10 # Capricorn
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    elif division == "D30":
        # Trimsamsa (Unequal Parashari partitions)
        if is_odd:
            if d < 5.0:
                varga_sign_idx, div_idx, effective_deg = 1, 1, d * 6.0 # Mars / Aries
            elif d < 10.0:
                varga_sign_idx, div_idx, effective_deg = 11, 2, (d - 5.0) * 6.0 # Saturn / Aquarius
            elif d < 18.0:
                varga_sign_idx, div_idx, effective_deg = 9, 3, (d - 10.0) * (30.0 / 8.0) # Jupiter / Sagittarius
            elif d < 25.0:
                varga_sign_idx, div_idx, effective_deg = 3, 4, (d - 18.0) * (30.0 / 7.0) # Mercury / Gemini
            else:
                varga_sign_idx, div_idx, effective_deg = 7, 5, (d - 25.0) * 6.0 # Venus / Libra
        else:
            if d < 5.0:
                varga_sign_idx, div_idx, effective_deg = 2, 1, d * 6.0 # Venus / Taurus
            elif d < 12.0:
                varga_sign_idx, div_idx, effective_deg = 6, 2, (d - 5.0) * (30.0 / 7.0) # Mercury / Virgo
            elif d < 20.0:
                varga_sign_idx, div_idx, effective_deg = 12, 3, (d - 12.0) * (30.0 / 8.0) # Jupiter / Pisces
            elif d < 25.0:
                varga_sign_idx, div_idx, effective_deg = 10, 4, (d - 20.0) * 6.0 # Saturn / Capricorn
            else:
                varga_sign_idx, div_idx, effective_deg = 8, 5, (d - 25.0) * 6.0 # Mars / Scorpio

    elif division == "D40":
        # Khavedamsa (0.75 degrees per division)
        seg = 30.0 / 40.0
        div_idx = min(int(d / seg) + 1, 40)
        effective_deg = (d % seg) * 40.0
        start = 1 if is_odd else 7 # Aries (1) for odd, Libra (7) for even
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    elif division == "D45":
        # Akshavedamsa (30/45 = 2/3 degrees per division)
        seg = 30.0 / 45.0
        div_idx = min(int(d / seg) + 1, 45)
        effective_deg = (d % seg) * 45.0
        start = 1 if is_movable else (5 if is_fixed else 9)
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    elif division == "D60":
        # Shashtiamsa (0.5 degrees per division)
        seg = 0.5
        div_idx = min(int(d / seg) + 1, 60)
        effective_deg = (d % seg) * 60.0
        start = S
        varga_sign_idx = (start - 1 + div_idx - 1) % 12 + 1

    else:
        raise ValueError(f"Unsupported Varga division identifier: '{division}'")

    sign_name = ZODIAC_SIGNS[varga_sign_idx - 1]
    return varga_sign_idx, sign_name, div_idx, round(effective_deg, 6)
