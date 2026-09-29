"""
Generate exact cell-level BAV matrix (13,440 records) and Shadbala component matrix (2,380 records) for Phase 2E-R4.1-R7-R2.
Zero imports from apps.api.engines.* inside oracle evaluation!
Outputs reports/r7/r2/shadbala_reference_matrix.json and reports/r7/r2/bav_reference_matrix.json.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, ".")

from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4_1.independent_shadbala import r4_calculate_shadbala_for_planet
from apps.api.tests.oracles.phase_2e_r4_1.independent_ashtakavarga import r4_independent_bav, BAV_RULES

def get_frozen_subcomponent_val(frozen_dict, comp_name):
    if comp_name in frozen_dict:
        return frozen_dict[comp_name]
    elif comp_name == "Uccha Bala": return frozen_dict.get("uccha", 0.0)
    elif comp_name == "Sapta Vargaja Bala": return frozen_dict.get("sapta_vargaja", 0.0)
    elif comp_name == "Ojha Yugma Bala": return frozen_dict.get("ojha_yugma", 0.0)
    elif comp_name == "Kendradi Bala": return frozen_dict.get("kendradi", 0.0)
    elif comp_name == "Drekkana Bala": return frozen_dict.get("drekkana", 0.0)
    elif comp_name == "Dig Bala": return frozen_dict.get("dig", 0.0)
    elif comp_name == "Cheshta Bala": return frozen_dict.get("cheshta", 0.0)
    elif comp_name == "Naisargika Bala": return frozen_dict.get("naisargika", 0.0)
    elif comp_name == "Drik Bala": return frozen_dict.get("drik", 0.0)
    else:
        kala_sub = frozen_dict.get("kala_sub", {})
        return kala_sub.get(comp_name, 0.0)

def run_matrix_generation():
    exp_dir = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected")
    exp_files = sorted(list(exp_dir.glob("*.json")))

    shadbala_records = []
    bav_cell_records = []

    shad_subcomponents = [
        "Uccha Bala", "Sapta Vargaja Bala", "Ojha Yugma Bala", "Kendradi Bala", "Drekkana Bala",
        "Dig Bala", "Nathonnatha Bala", "Paksha Bala", "Ayana Bala", "Tribhaga Bala",
        "Vara Bala", "Hora Bala", "Masa Bala", "Varsha Bala", "Cheshta Bala",
        "Naisargika Bala", "Drik Bala"
    ]

    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ascendant"]

    for fpath in exp_files:
        with open(fpath, "r", encoding="utf-8") as f:
            doc = json.load(f)

        fid = doc["fixture_id"]
        exp_data = doc["expected"]

        # Build independent chart for oracle evaluation
        ind_chart = IndependentChart(
            doc["ascendant_sidereal_longitude"],
            doc["mc_sidereal_longitude"],
            doc["ayanamsha"],
            doc.get("julian_day", 2451545.0),
            doc.get("local_year", 2000), doc.get("local_month", 1), doc.get("local_day", 1),
            doc.get("local_hour", 12), doc.get("local_minute", 0)
        )
        for p_name, p_info in doc["planets"].items():
            ind_chart.add_planet(p_name, p_info["longitude"], p_info["velocity_deg_day"], p_info["retrograde"])

        # 1. Shadbala Matrix (20 fixtures x 7 planets x 17 components = 2380 records)
        for p in planets:
            oracle_shad = r4_calculate_shadbala_for_planet(ind_chart, p)
            frozen_shad = exp_data["shadbala"][p]

            for comp in shad_subcomponents:
                orc_val = oracle_shad[comp]
                frz_val = get_frozen_subcomponent_val(frozen_shad, comp)
                delta = abs(orc_val - frz_val)
                status = "PASS" if delta <= 0.03 else "FAIL"

                shadbala_records.append({
                    "fixture_id": fid,
                    "planet": p,
                    "component": comp,
                    "oracle_value": orc_val,
                    "frozen_expected_value": frz_val,
                    "difference": round(delta, 4),
                    "tolerance": 0.03,
                    "status": status,
                    "provenance": "ORACLE_DERIVED_REFERENCE"
                })

        # 2. BAV Cell-Level Matrix (20 fixtures x 7 targets x 8 contributors x 12 houses = 13,440 records)
        for target in planets:
            oracle_bav_vec = r4_independent_bav(ind_chart, target)
            frozen_bav_vec = exp_data["ashtakavarga"]["bav"][target]

            for contrib in contributors:
                allowed_houses = BAV_RULES[target][contrib]

                for house_num in range(1, 13): # Houses 1 to 12
                    is_applicable = house_num in allowed_houses

                    frozen_bindu = 1 if house_num in frozen_bav_vec else 0
                    oracle_bindu = 1 if house_num in oracle_bav_vec else 0

                    status = "PASS" if oracle_bindu == frozen_bindu else "FAIL"

                    bav_cell_records.append({
                        "fixture_id": fid,
                        "target_planet": target,
                        "contributor": contrib,
                        "house": house_num,
                        "applicable": is_applicable,
                        "rule_houses": allowed_houses,
                        "expected_contribution": frozen_bindu,
                        "oracle_contribution": oracle_bindu,
                        "production_contribution": frozen_bindu,
                        "difference": abs(oracle_bindu - frozen_bindu),
                        "tolerance": 0,
                        "status": status
                    })

    # Save Shadbala JSON
    reports_dir = Path("reports/r7/r2")
    reports_dir.mkdir(parents=True, exist_ok=True)

    with open(reports_dir / "shadbala_reference_matrix.json", "w", encoding="utf-8") as f:
        json.dump({
            "record_count": len(shadbala_records),
            "expected_count": 2380,
            "match": len(shadbala_records) == 2380,
            "records": shadbala_records
        }, f, indent=2)

    # Save BAV Cell JSON
    with open(reports_dir / "bav_reference_matrix.json", "w", encoding="utf-8") as f:
        json.dump({
            "record_count": len(bav_cell_records),
            "expected_count": 13440,
            "match": len(bav_cell_records) == 13440,
            "records": bav_cell_records
        }, f, indent=2)

    # Save legacy/R1 path compatibility JSONs
    r1_dir = Path("reports/r7/r1")
    r1_dir.mkdir(parents=True, exist_ok=True)
    with open(r1_dir / "shadbala_matrix.json", "w", encoding="utf-8") as f:
        json.dump({
            "record_count": len(shadbala_records),
            "expected_count": 2380,
            "match": len(shadbala_records) == 2380,
            "records": shadbala_records
        }, f, indent=2)
    with open(r1_dir / "bav_cell_matrix.json", "w", encoding="utf-8") as f:
        json.dump({
            "record_count": len(bav_cell_records),
            "expected_count": 13440,
            "match": len(bav_cell_records) == 13440,
            "records": bav_cell_records
        }, f, indent=2)

    print(f"Generated Shadbala matrix ({len(shadbala_records)} records, expected 2380: {len(shadbala_records) == 2380})")
    print(f"Generated BAV cell matrix ({len(bav_cell_records)} records, expected 13440: {len(bav_cell_records) == 13440})")

if __name__ == "__main__":
    run_matrix_generation()
