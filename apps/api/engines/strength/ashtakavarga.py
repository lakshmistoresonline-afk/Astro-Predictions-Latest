"""
Authoritative Ashtakavarga Engine (BAV & SAV).
Calculates exact Parashari Ashtakavarga using Canonical Phase 2A Chart Data.
Does not use synthetic logic or arbitrary scaling.
"""
import hashlib
import json
from typing import Dict, List

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.strength.models import (
    BhinnashtakavargaResult,
    SarvashtakavargaResult,
    AshtakavargaSuiteResult
)
from apps.api.engines.strength.exceptions import MissingCanonicalStateError

# Parashari Ashtakavarga Contributor Matrices (1-based relative house positions)
# Format: BAV_RULES[target_planet][contributing_planet] = [list of beneficial houses from contributor's position]

BAV_RULES = {
    "Sun": {
        "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon": [3, 6, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus": [6, 7, 12],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [3, 4, 6, 10, 11, 12]
    },
    "Moon": {
        "Sun": [3, 6, 7, 8, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 4, 7, 8, 10, 11, 12],
        "Venus": [3, 4, 5, 7, 9, 10, 11],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [3, 6, 10, 11]
    },
    "Mars": {
        "Sun": [3, 5, 6, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus": [6, 8, 11, 12],
        "Saturn": [1, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 3, 6, 10, 11]
    },
    "Mercury": {
        "Sun": [5, 6, 9, 11, 12],
        "Moon": [2, 4, 6, 8, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 2, 4, 6, 8, 10, 11]
    },
    "Jupiter": {
        "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon": [2, 5, 7, 9, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus": [2, 5, 6, 9, 10, 11],
        "Saturn": [3, 5, 6, 12],
        "Ascendant": [1, 2, 4, 5, 6, 9, 10, 11, 12]
    },
    "Venus": {
        "Sun": [8, 11, 12],
        "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars": [3, 5, 6, 9, 11, 12],
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn": [3, 4, 5, 8, 9, 10, 11],
        "Ascendant": [1, 2, 3, 4, 5, 8, 9, 11]
    },
    "Saturn": {
        "Sun": [1, 2, 4, 7, 8, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [3, 5, 6, 10, 11, 12],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus": [6, 11, 12],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [1, 3, 4, 6, 10, 11]
    }
}

class AshtakavargaEngine:
    """Production Ashtakavarga Calculation Engine."""

    @staticmethod
    def calculate_bav(canonical_chart: CanonicalVedicChart, target_planet: str) -> BhinnashtakavargaResult:
        if target_planet not in BAV_RULES:
            raise ValueError(f"Invalid target planet for BAV: {target_planet}")

        if target_planet not in canonical_chart.placements:
            raise MissingCanonicalStateError(f"Missing placement for target planet {target_planet}")

        target_sign = canonical_chart.placements[target_planet].rashi.sign_index

        # 12-house bindu array initialized to 0 (0=Aries, 1=Taurus, ..., 11=Pisces)
        bindus = [0] * 12

        target_rules = BAV_RULES[target_planet]

        for contributor, beneficial_houses in target_rules.items():
            if contributor == "Ascendant":
                contrib_sign = canonical_chart.ascendant.sign_index
            else:
                if contributor not in canonical_chart.placements:
                    raise MissingCanonicalStateError(f"Missing placement for contributor {contributor}")
                contrib_sign = canonical_chart.placements[contributor].rashi.sign_index

            for house_rel in beneficial_houses:
                # 1-based relative house offset from 1-based contributor sign to 0-based sign index
                target_house_sign = (contrib_sign + house_rel - 2) % 12
                bindus[target_house_sign] += 1

        total_bindus = sum(bindus)

        return BhinnashtakavargaResult(
            planet=target_planet,
            bindus=bindus,
            total=total_bindus
        )

    @staticmethod
    def calculate_ashtakavarga(canonical_chart: CanonicalVedicChart) -> AshtakavargaSuiteResult:
        classical_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

        bav_dict: Dict[str, BhinnashtakavargaResult] = {}
        sav_bindus = [0] * 12

        for planet in classical_planets:
            bav_res = AshtakavargaEngine.calculate_bav(canonical_chart, planet)
            bav_dict[planet] = bav_res
            for sign_idx in range(12):
                sav_bindus[sign_idx] += bav_res.bindus[sign_idx]

        total_sav = sum(sav_bindus)
        sav_res = SarvashtakavargaResult(bindus=sav_bindus, total=total_sav)

        return AshtakavargaSuiteResult(
            chart_hash=canonical_chart.calculation_hash,
            bav=bav_dict,
            sav=sav_res,
            calculation_hash=hashlib.sha256(json.dumps({"chart_hash": canonical_chart.calculation_hash, "sav": sav_bindus, "total": total_sav}, sort_keys=True).encode("utf-8")).hexdigest()
        )

AuthoritativeAshtakavargaEngine = AshtakavargaEngine
