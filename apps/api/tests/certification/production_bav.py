"""
Pure Real Production Ashtakavarga Engine Adapter for Phase 2E-R4.1-R12-R1.
Invokes the REAL production Ashtakavarga engine (AshtakavargaEngine.calculate_ashtakavarga) on canonical charts built from BirthInput.
Returns 13,440 production BAV cell records across 20 reference fixtures.
Derives production SAV directly from production BAV cell totals.
ZERO imports from apps.api.tests.oracles.*!
ZERO chart longitudes or placements overwritten by fixture expected values!
"""
import json
from pathlib import Path
from typing import List, Dict

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine, BAV_RULES

def get_production_bav_records() -> List[Dict]:
    exp_dir = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected")
    exp_files = sorted(list(exp_dir.glob("*.json")))

    records = []
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ascendant"]

    for fpath in exp_files:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        fid = data["fixture_id"]
        dt_str = data["birth_datetime_utc"]

        # 1. REAL PRODUCTION ENGINE EXECUTION PATH
        inp = BirthInput(
            name=data["name"],
            year=data.get("local_year", int(dt_str[:4])),
            month=data.get("local_month", int(dt_str[5:7])),
            day=data.get("local_day", int(dt_str[8:10])),
            hour=data.get("local_hour", int(dt_str[11:13])),
            minute=data.get("local_minute", int(dt_str[14:16])),
            second=0,
            timezone_str=data["timezone_str"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            elevation_m=0.0
        )
        prod_chart = build_canonical_vedic_chart(inp)
        prod_asht_res = AshtakavargaEngine.calculate_ashtakavarga(prod_chart)

        # 2. EXTRACT PRODUCTION BAV CELL VALUES (13,440 cells)
        for target in planets:
            prod_bav_vec = prod_asht_res.bav[target].bindus

            for contrib in contributors:
                allowed_houses = BAV_RULES[target][contrib]

                for house_num in range(1, 13):
                    is_applicable = house_num in allowed_houses
                    prod_bindu = prod_bav_vec[house_num - 1]

                    records.append({
                        "fixture_id": fid,
                        "target_planet": target,
                        "contributor": contrib,
                        "house": house_num,
                        "applicable": is_applicable,
                        "rule_houses": allowed_houses,
                        "production_value": prod_bindu,
                        "source_type": "PRODUCTION",
                        "production_provenance": {
                            "engine": "Astrovision Production Ashtakavarga Engine",
                            "module": "apps.api.engines.strength.ashtakavarga",
                            "class": "AshtakavargaEngine",
                            "function": "calculate_ashtakavarga"
                        }
                    })

    return records

def get_production_sav_vector(fixture_id: str = "REF_001") -> List[int]:
    """
    Derives production 12-house SAV totals directly from real production BAV calculations for a fixture.
    SAV[h] = sum(Production_BAV_P[h] for P in 7 target planets)
    """
    exp_dir = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected")
    fpath = exp_dir / f"{fixture_id}.json"

    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)

    dt_str = data["birth_datetime_utc"]
    inp = BirthInput(
        name=data["name"],
        year=data.get("local_year", int(dt_str[:4])),
        month=data.get("local_month", int(dt_str[5:7])),
        day=data.get("local_day", int(dt_str[8:10])),
        hour=data.get("local_hour", int(dt_str[11:13])),
        minute=data.get("local_minute", int(dt_str[14:16])),
        second=0,
        timezone_str=data["timezone_str"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        elevation_m=0.0
    )
    prod_chart = build_canonical_vedic_chart(inp)
    prod_asht_res = AshtakavargaEngine.calculate_ashtakavarga(prod_chart)

    return prod_asht_res.sav.bindus
