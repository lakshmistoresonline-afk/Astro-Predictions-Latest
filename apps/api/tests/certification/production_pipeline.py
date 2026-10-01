"""
Pure End-to-End Production Pipeline Certification Adapter for Phase 2E-R4.1-R12.
Executes the COMPLETE REAL PRODUCTION ENGINE CHAIN:
  BirthInput -> Astronomy Provider -> Canonical Vedic Chart -> Varga Engine -> Shadbala Engine -> Ashtakavarga Engine.
ZERO imports from apps.api.tests.oracles.*!
ZERO chart longitudes or placements overwritten by fixture expected values!
ZERO tolerance inflation!
"""
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

from apps.api.engines.vedic.models import BirthInput, CanonicalVedicChart
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.varga.engine import VargaEngine
from apps.api.engines.strength.shadbala import ShadbalaEngine
from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine, BAV_RULES

def compute_chart_hash(chart: CanonicalVedicChart) -> str:
    planets_data = {}
    for p_name in sorted(chart.placements.keys()):
        p = chart.placements[p_name]
        planets_data[p_name] = {
            "longitude": round(p.sidereal_longitude, 6),
            "sign_index": p.rashi.sign_index,
            "retrograde": p.retrograde,
            "velocity": round(p.velocity_deg_day, 6)
        }

    data = {
        "ascendant_longitude": round(chart.ascendant.absolute_longitude, 6),
        "ascendant_sign_index": chart.ascendant.sign_index,
        "mc_longitude": round(chart.mc.absolute_longitude, 6),
        "ayanamsha": round(chart.ayanamsha_value_deg, 6),
        "julian_day": round(chart.time_normalization.julian_day_tt, 6),
        "planets": planets_data
    }
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()

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

def execute_pure_production_pipeline_for_fixture(fixture_data: dict) -> Tuple[CanonicalVedicChart, Any, Any, str]:
    """
    Executes the pure production pipeline for a single fixture using ONLY its input fields.
    Does NOT modify the chart using expected longitudes.
    """
    dt_str = fixture_data["birth_datetime_utc"]
    inp = BirthInput(
        name=fixture_data["name"],
        year=fixture_data.get("local_year", int(dt_str[:4])),
        month=fixture_data.get("local_month", int(dt_str[5:7])),
        day=fixture_data.get("local_day", int(dt_str[8:10])),
        hour=fixture_data.get("local_hour", int(dt_str[11:13])),
        minute=fixture_data.get("local_minute", int(dt_str[14:16])),
        second=0,
        timezone_str=fixture_data["timezone_str"],
        latitude=fixture_data["latitude"],
        longitude=fixture_data["longitude"],
        elevation_m=0.0
    )

    # 1. Pure Production Chart Creation
    prod_chart = build_canonical_vedic_chart(inp)
    chart_hash = compute_chart_hash(prod_chart)

    # 2. Pure Production Varga Suite Calculation
    varga_suite = VargaEngine.calculate_all_16_vargas(prod_chart)

    # 3. Pure Production Shadbala Calculation
    prod_shadbala = ShadbalaEngine.calculate_shadbala_suite(prod_chart, varga_suite)

    # 4. Pure Production Ashtakavarga (BAV & SAV) Calculation
    prod_ashtakavarga = AshtakavargaEngine.calculate_ashtakavarga(prod_chart)

    return prod_chart, prod_shadbala, prod_ashtakavarga, chart_hash

def get_pure_production_shadbala_matrix() -> List[Dict]:
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
        prod_chart, prod_shad, _, chart_hash = execute_pure_production_pipeline_for_fixture(data)

        for p in planets:
            p_shad = prod_shad.planets[p]
            for comp in shad_subcomponents:
                val = extract_production_subcomponent_val(p_shad, comp)
                records.append({
                    "fixture_id": fid,
                    "planet": p,
                    "component": comp,
                    "production_value": round(val, 4),
                    "chart_hash": chart_hash,
                    "source_type": "PRODUCTION",
                    "production_provenance": {
                        "engine": "Astrovision Real Production Engine",
                        "module": "apps.api.engines.strength.shadbala",
                        "class": "ShadbalaEngine",
                        "function": "calculate_shadbala_suite"
                    }
                })

    return records

def get_pure_production_bav_matrix() -> List[Dict]:
    exp_dir = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected")
    exp_files = sorted(list(exp_dir.glob("*.json")))

    records = []
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ascendant"]

    for fpath in exp_files:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        fid = data["fixture_id"]
        _, _, prod_asht, chart_hash = execute_pure_production_pipeline_for_fixture(data)

        for target in planets:
            bindus = prod_asht.bav[target].bindus
            for contrib in contributors:
                allowed_houses = BAV_RULES[target][contrib]
                for house_num in range(1, 13):
                    cell_val = bindus[house_num - 1]
                    records.append({
                        "fixture_id": fid,
                        "target_planet": target,
                        "contributor": contrib,
                        "house": house_num,
                        "applicable": house_num in allowed_houses,
                        "production_value": cell_val,
                        "chart_hash": chart_hash,
                        "source_type": "PRODUCTION",
                        "production_provenance": {
                            "engine": "Astrovision Real Production Engine",
                            "module": "apps.api.engines.strength.ashtakavarga",
                            "class": "AshtakavargaEngine",
                            "function": "calculate_ashtakavarga"
                        }
                    })

    return records
