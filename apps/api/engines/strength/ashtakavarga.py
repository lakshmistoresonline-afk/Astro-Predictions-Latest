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
    """Evaluator for Bhinnashtakavarga (BAV) and Sarvashtakavarga (SAV)."""

    @classmethod
    def calculate_ashtakavarga(cls, canonical_chart: CanonicalVedicChart) -> AshtakavargaSuiteResult:
        bav_results: Dict[str, BhinnashtakavargaResult] = {}
        sav_bindus = [0] * 12 # Indexes 0 to 11 representing Aries to Pisces

        # 1. Determine positions (Sign index: 1-12)
        positions = {}
        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            if p not in canonical_chart.placements:
                raise MissingCanonicalStateError(f"Required planet {p} missing from canonical chart for Ashtakavarga calculation.")
            positions[p] = canonical_chart.placements[p].rashi.sign_index
        positions["Ascendant"] = canonical_chart.ascendant.sign_index

        # 2. Calculate BAV for each of the 7 planets
        for target_planet, contributors in BAV_RULES.items():
            bav_array = [0] * 12
            total_bav = 0
            for contributor, beneficial_houses in contributors.items():
                contributor_sign = positions[contributor] # 1..12
                for house_offset in beneficial_houses: # 1..12
                    # The sign receiving the bindu is (contributor_sign + house_offset - 1)
                    target_sign_index = (contributor_sign + house_offset - 2) % 12 # 0-indexed (Aries=0)
                    bav_array[target_sign_index] += 1
                    total_bav += 1

            bav_results[target_planet] = BhinnashtakavargaResult(
                planet=target_planet,
                bindus=bav_array,
                total=total_bav
            )

            # Aggregate to SAV
            for i in range(12):
                sav_bindus[i] += bav_array[i]

        sav_total = sum(sav_bindus)

        # 3. Create SAV Object
        sav_result = SarvashtakavargaResult(
            bindus=sav_bindus,
            total=sav_total
        )

        # 4. Hash the calculation
        payload = {
            "chart_hash": canonical_chart.calculation_hash,
            "sav": sav_bindus,
            "total": sav_total
        }
        calc_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return AshtakavargaSuiteResult(
            chart_hash=canonical_chart.calculation_hash,
            bav=bav_results,
            sav=sav_result,
            calculation_hash=calc_hash
        )
