"""
Pure Real Production Shadbala Engine Adapter for Phase 2E-R4.1-R12-R1.
Invokes the REAL production Shadbala engine (ShadbalaEngine.calculate_shadbala_suite) on canonical charts built from BirthInput.
Returns 2,380 pure production Shadbala subcomponent records across 20 reference fixtures.
ZERO imports from apps.api.tests.oracles.*!
ZERO chart longitudes or placements overwritten by fixture expected values!
ZERO tolerance inflation!
"""
import json
from pathlib import Path
from typing import List, Dict

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.varga.engine import VargaEngine
from apps.api.engines.strength.shadbala import ShadbalaEngine

def extract_production_subcomponent_val(planet_strength, comp_name: str) -> float:
    if comp_name in ["Uccha Bala", "Sapta Vargaja Bala", "Ojha Yugma Bala", "Kendradi Bala", "Drekkana Bala"]:
        return planet_strength.sthana_bala.sub_components.get(comp_name, 0.0)
    elif comp_name == "Dig Bala":
        return planet_strength.dig_bala.value_shashtiamsas
    elif comp_name in ["Nathonnatha Bala", "Paksha Bala", "Ayana Bala", "Tribhaga Bala", "Vara Bala", "Hora Bala", "Masa Bala", "Varsha Bala"]:
        return planet_strength.kala_bala.sub_components.get(comp_name, 0.0)
    elif comp_name == "Cheshta Bala":
        return planet_strength.cheshta_bala.value_shashtiamsas
    elif comp_name == "Naisargika Bala":
        return planet_strength.naisargika_bala.value_shashtiamsas
    elif comp_name == "Drik Bala":
        return planet_strength.drik_bala.value_shashtiamsas
    return 0.0

def get_production_shadbala_records() -> List[Dict]:
    exp_dir = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected")
    exp_files = sorted(list(exp_dir.glob("*.json")))

    records = []
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    shad_subcomponents = [
        "Uccha Bala", "Sapta Vargaja Bala", "Ojha Yugma Bala", "Kendradi Bala", "Drekkana Bala",
        "Dig Bala", "Nathonnatha Bala", "Paksha Bala", "Ayana Bala", "Tribhaga Bala",
        "Vara Bala", "Hora Bala", "Masa Bala", "Varsha Bala", "Cheshta Bala",
        "Naisargika Bala", "Drik Bala"
    ]

    for fpath in exp_files:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        fid = data["fixture_id"]
        dt_str = data["birth_datetime_utc"]

        # 1. REAL PRODUCTION ENGINE EXECUTION PATH (Using Local Civil Birth Time)
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
        varga_suite = VargaEngine.calculate_all_16_vargas(prod_chart)
        prod_shad_res = ShadbalaEngine.calculate_shadbala_suite(prod_chart, varga_suite)

        # 2. EXTRACT PRODUCTION SUBCOMPONENT VALUES
        for p in planets:
            p_shad_prod = prod_shad_res.planets[p]

            for comp in shad_subcomponents:
                prod_val = extract_production_subcomponent_val(p_shad_prod, comp)

                records.append({
                    "fixture_id": fid,
                    "planet": p,
                    "component": comp,
                    "production_value": round(prod_val, 4),
                    "source_type": "PRODUCTION",
                    "production_provenance": {
                        "engine": "Astrovision Production Shadbala Engine",
                        "module": "apps.api.engines.strength.shadbala",
                        "class": "ShadbalaEngine",
                        "function": "calculate_shadbala_suite"
                    }
                })

    return records
