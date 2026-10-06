"""
Authoritative Local Jaimini Calculation Engine.
Calculates 7 Chara Karakas (AK, AmK, BK, MK, PK, GK, DK), Jaimini Rashi aspects, Arudha Lagna (AL), Upapada Lagna (UL), and Karakamsha.
Consumes CanonicalVedicChart & VargaEngine D9.
Section 1..10 Compliance:
- Corrected VargaPlacement field access: uses varga_sign_index for D9 Navamsha Karakamsha calculation.
- Corrected RashiPosition field access: uses ascendant.sign_index for Lagna sign index.
- Strict CanonicalVedicChart instance validation.
- Imports centralized RASHI_LORDS and ZODIAC_SIGNS from rashi.py!
- Fail closed if 7 core planets missing, boolean, or out of range [0.0, 360.0).
"""
import hashlib
import json
import math
from typing import Dict, List, Optional

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.vedic.rashi import RASHI_LORDS, ZODIAC_SIGNS as RASHI_NAMES
from apps.api.engines.varga.engine import VargaEngine
from apps.api.engines.jaimini.models import (
    CharaKarakaInfo,
    RashiAspectInfo,
    JaiminiSuiteResult
)

# 7 Parashari/Jaimini Chara Karakas (excluding Rahu/Ketu)
CHARA_KARAKA_NAMES = [
    ("AK", "Atmakaraka"),
    ("AmK", "Amatyakaraka"),
    ("BK", "Bhratrukaraka"),
    ("MK", "Matrukaraka"),
    ("PK", "Putrakaraka"),
    ("GK", "Gnatikaraka"),
    ("DK", "Darakaraka")
]

class JaiminiEngine:
    """
    Authoritative Local Jaimini Engine.
    """

    @classmethod
    def _calculate_chara_karakas_internal(cls, longitudes: Dict[str, float]) -> Dict[str, CharaKarakaInfo]:
        """
        Internal single source of truth for 7 Chara Karakas calculation.
        Fails closed with ValueError if any of the 7 core planets is missing, boolean, or has out-of-range longitude [0.0, 360.0).
        """
        seven_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        planet_degrees = []

        for p_name in seven_planets:
            if p_name not in longitudes:
                raise ValueError(f"Required planet '{p_name}' is missing for 7 Chara Karakas calculation.")
            lon = longitudes[p_name]
            if isinstance(lon, bool) or not isinstance(lon, (int, float)) or math.isnan(lon) or math.isinf(lon):
                raise ValueError(f"Longitude for planet '{p_name}' must be a finite numeric float (cannot be boolean).")
            if not (0.0 <= lon < 360.0):
                raise ValueError(f"Longitude for planet '{p_name}' ({lon}) must be in valid astronomical range [0.0, 360.0).")
            deg_val = lon % 30.0
            planet_degrees.append((p_name, deg_val))

        planet_degrees.sort(key=lambda x: x[1], reverse=True)

        chara_karakas: Dict[str, CharaKarakaInfo] = {}
        for idx, (code, full_name) in enumerate(CHARA_KARAKA_NAMES):
            p_name, deg_val = planet_degrees[idx]
            chara_karakas[code] = CharaKarakaInfo(
                karaka_code=code,
                karaka_name=full_name,
                planet=p_name,
                degree_in_sign=round(deg_val, 4)
            )
        return chara_karakas

    @classmethod
    def calculate_chara_karakas_from_longitudes(cls, longitudes: Dict[str, float]) -> Dict[str, str]:
        """
        Adapter method for legacy compatibility that delegates to _calculate_chara_karakas_internal.
        """
        chara_karakas = cls._calculate_chara_karakas_internal(longitudes)
        mapping = {}
        for code, info in chara_karakas.items():
            full_title = next((f"{full} ({c})" for c, full in CHARA_KARAKA_NAMES if c == code), code)
            mapping[full_title] = info.planet
        return mapping

    @classmethod
    def calculate_jaimini_suite(
        cls,
        canonical_chart: CanonicalVedicChart
    ) -> JaiminiSuiteResult:
        if not isinstance(canonical_chart, CanonicalVedicChart):
            raise ValueError("calculate_jaimini_suite requires a valid CanonicalVedicChart instance.")

        # 1. Calculate 7 Chara Karakas via single internal helper
        longitudes = {
            p_name: placement.sidereal_longitude
            for p_name, placement in canonical_chart.placements.items()
        }
        chara_karakas = cls._calculate_chara_karakas_internal(longitudes)

        # Fail closed if AK is unavailable
        if "AK" not in chara_karakas:
            raise ValueError("Atmakaraka (AK) is unavailable from canonical Jaimini calculation.")

        ak_planet = chara_karakas["AK"].planet

        # 2. Arudha Lagna (AL) Calculation
        lagna_rashi_idx = canonical_chart.ascendant.sign_index
        lagna_lord = RASHI_LORDS[lagna_rashi_idx]

        # Fail closed if lagna_lord is missing from canonical chart placements
        if lagna_lord not in canonical_chart.placements:
            raise ValueError(f"Lagna lord '{lagna_lord}' is missing from canonical chart placements.")

        lagna_lord_rashi_idx = canonical_chart.placements[lagna_lord].rashi.sign_index

        dist_houses = ((lagna_lord_rashi_idx - lagna_rashi_idx) % 12)
        if dist_houses == 0:
            dist_houses = 12

        al_idx = ((lagna_lord_rashi_idx + dist_houses - 2) % 12) + 1
        # Exception handling: if AL falls in 1st or 7th from Lagna, shift 10 houses
        if al_idx in [lagna_rashi_idx, ((lagna_rashi_idx + 5) % 12) + 1]:
            al_idx = ((al_idx + 9) % 12) + 1

        # 3. Upapada Lagna (UL - Arudha of 12th House)
        h12_rashi_idx = ((lagna_rashi_idx + 10) % 12) + 1
        h12_lord = RASHI_LORDS[h12_rashi_idx]

        # Fail closed if h12_lord is missing from canonical chart placements
        if h12_lord not in canonical_chart.placements:
            raise ValueError(f"12th house lord '{h12_lord}' is missing from canonical chart placements.")

        h12_lord_rashi_idx = canonical_chart.placements[h12_lord].rashi.sign_index

        dist_h12 = ((h12_lord_rashi_idx - h12_rashi_idx) % 12)
        if dist_h12 == 0:
            dist_h12 = 12

        ul_idx = ((h12_lord_rashi_idx + dist_h12 - 2) % 12) + 1
        if ul_idx in [h12_rashi_idx, ((h12_rashi_idx + 5) % 12) + 1]:
            ul_idx = ((ul_idx + 9) % 12) + 1

        # 4. Karakamsha (D9 sign of Atmakaraka) (Fail closed if AK is missing from D9!)
        vargas = VargaEngine.calculate_all_16_vargas(canonical_chart)
        d9_chart = vargas.d9

        if ak_planet not in d9_chart.placements:
            raise ValueError(f"Atmakaraka planet '{ak_planet}' is missing from D9 Navamsha chart.")

        karakamsha_idx = d9_chart.placements[ak_planet].varga_sign_index

        # 5. Jaimini / Rashi Aspects
        rashi_aspects: List[RashiAspectInfo] = []
        for r_i in range(1, 13):
            # Movable (1, 4, 7, 10): aspects Fixed (2, 5, 8, 11) except adjacent
            if r_i in [1, 4, 7, 10]:
                adj = (r_i % 12) + 1
                aspected = [x for x in [2, 5, 8, 11] if x != adj]
            # Fixed (2, 5, 8, 11): aspects Movable (1, 4, 7, 10) except adjacent
            elif r_i in [2, 5, 8, 11]:
                adj = r_i - 1 if r_i > 1 else 12
                aspected = [x for x in [1, 4, 7, 10] if x != adj]
            # Dual (3, 6, 9, 12): aspects all other Dual signs
            else:
                aspected = [x for x in [3, 6, 9, 12] if x != r_i]

            rashi_aspects.append(RashiAspectInfo(
                source_rashi_index=r_i,
                source_rashi_name=RASHI_NAMES[r_i - 1],
                aspected_rashi_indices=aspected,
                aspected_rashi_names=[RASHI_NAMES[x - 1] for x in aspected]
            ))

        payload = {
            "chart_hash": canonical_chart.calculation_hash,
            "ak": ak_planet,
            "al": al_idx,
            "ul": ul_idx,
            "karakamsha": karakamsha_idx
        }
        j_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return JaiminiSuiteResult(
            chart_hash=canonical_chart.calculation_hash,
            atmakaraka_planet=ak_planet,
            chara_karakas=chara_karakas,
            arudha_lagna_rashi_index=al_idx,
            arudha_lagna_rashi_name=RASHI_NAMES[al_idx - 1],
            upapada_lagna_rashi_index=ul_idx,
            upapada_lagna_rashi_name=RASHI_NAMES[ul_idx - 1],
            karakamsha_rashi_index=karakamsha_idx,
            karakamsha_rashi_name=RASHI_NAMES[karakamsha_idx - 1],
            rashi_aspects=rashi_aspects,
            calculation_hash=j_hash
        )
