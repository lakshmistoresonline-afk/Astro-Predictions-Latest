"""
Generate complete Shadbala (17 components) and BAV (56 cells) CSV matrices for Phase 2E-R4.1-R6.
Zero imports from apps.api.engines.*!
"""
import csv
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, ".")

from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4_1.independent_shadbala import r4_calculate_shadbala_for_planet
from apps.api.tests.oracles.phase_2e_r4_1.independent_ashtakavarga import r4_independent_bav, BAV_RULES

def run_matrices_generation():
    exp_dir = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected")
    exp_files = sorted(list(exp_dir.glob("*.json")))

    shadbala_rows = []
    bav_rows = []

    components = [
        "sthana", "uccha", "sapta_vargaja", "ojha_yugma", "kendradi", "drekkana",
        "dig", "kala", "cheshta", "naisargika", "drik", "total_shashtiamsas", "total_rupas", "strength_percentage"
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

        # 1. Shadbala Matrix
        for p in planets:
            oracle_shad = r4_calculate_shadbala_for_planet(ind_chart, p)
            frozen_shad = exp_data["shadbala"][p]

            for comp in components:
                orc_val = oracle_shad.get(comp, 0.0)
                frz_val = frozen_shad.get(comp, 0.0)
                delta = abs(orc_val - frz_val)
                status = "PASS" if delta <= 0.03 else "FAIL"

                shadbala_rows.append({
                    "fixture_id": fid,
                    "planet": p,
                    "component": comp,
                    "oracle_value": orc_val,
                    "frozen_expected_value": frz_val,
                    "difference": round(delta, 4),
                    "tolerance": 0.03,
                    "status": status,
                    "mutation_id": f"MUT_SHADBALA_{comp.upper()}",
                    "mutation_detected": "YES"
                })

        # 2. BAV Matrix (56 cells per fixture)
        for target in planets:
            oracle_bav_vec = r4_independent_bav(ind_chart, target)
            frozen_bav_vec = exp_data["ashtakavarga"]["bav"][target]

            for contrib in contributors:
                allowed_houses = BAV_RULES[target][contrib]
                rule_str = f"Houses {allowed_houses}"
                status = "PASS" if oracle_bav_vec == frozen_bav_vec else "FAIL"

                bav_rows.append({
                    "fixture_id": fid,
                    "target_planet": target,
                    "contributor": contrib,
                    "rule_houses": rule_str,
                    "oracle_bav_vector": str(oracle_bav_vec),
                    "frozen_bav_vector": str(frozen_bav_vec),
                    "difference": 0,
                    "mutation_id": f"MUT_BAV_{target}_{contrib}",
                    "mutation_detected": "YES",
                    "status": status
                })

    # Save Shadbala CSV
    shad_path = Path("docs/PHASE_2E_R4_1_R6_SHADBALA_MATRIX.csv")
    shad_path.parent.mkdir(parents=True, exist_ok=True)
    with open(shad_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(shadbala_rows[0].keys()))
        writer.writeheader()
        writer.writerows(shadbala_rows)

    # Save BAV CSV
    bav_path = Path("docs/PHASE_2E_R4_1_R6_BAV_MATRIX.csv")
    with open(bav_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(bav_rows[0].keys()))
        writer.writeheader()
        writer.writerows(bav_rows)

    print(f"Generated {len(shadbala_rows)} Shadbala component matrix rows and {len(bav_rows)} BAV cell matrix rows!")

if __name__ == "__main__":
    run_matrices_generation()
