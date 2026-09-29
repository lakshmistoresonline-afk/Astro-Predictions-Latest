"""
Phase 2E-R4.1 Expected Value Generator.
Reads reference input JSON files from apps/api/tests/fixtures/phase_2e_r4_1_reference/
and evaluates the expected BAV, SAV, and Shadbala outputs using ONLY the pure R4.1 independent oracle.
Zero imports from apps.api.engines.*!
Explicitly preserves all 17 granular BPHS Shadbala subcomponents as top-level keys.
"""
import glob
import hashlib
import json
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent.parent))

from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4_1.independent_ashtakavarga import r4_independent_bav, r4_independent_sav
from apps.api.tests.oracles.phase_2e_r4_1.independent_shadbala import r4_calculate_shadbala_for_planet

def generate_frozen_expected_fixtures():
    ref_dir = Path(__file__).parent.parent.parent / "fixtures" / "phase_2e_r4_1_reference"
    exp_dir = Path(__file__).parent.parent.parent / "fixtures" / "phase_2e_r4_1_expected"
    exp_dir.mkdir(parents=True, exist_ok=True)

    ref_files = sorted(list(ref_dir.glob("*.json")))

    for ref_file in ref_files:
        with open(ref_file, "r", encoding="utf-8") as f:
            ref_data = json.load(f)

        fid = ref_data["fixture_id"]

        # Instantiate pure R4.1 independent chart
        ind_chart = IndependentChart(
            ref_data["ascendant_sidereal_longitude"],
            ref_data["mc_sidereal_longitude"],
            ref_data["ayanamsha"],
            ref_data["julian_day"],
            ref_data["local_year"],
            ref_data["local_month"],
            ref_data["local_day"],
            ref_data["local_hour"],
            ref_data["local_minute"]
        )
        for p_name, p_info in ref_data["planets"].items():
            ind_chart.add_planet(p_name, p_info["longitude"], p_info["velocity_deg_day"], p_info["retrograde"])

        # Compute pure independent BAV & SAV
        bav_expected = {p: r4_independent_bav(ind_chart, p) for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
        sav_expected = r4_independent_sav(ind_chart)

        # Compute pure independent Shadbala (all 17 subcomponents top-level)
        shadbala_expected = {p: r4_calculate_shadbala_for_planet(ind_chart, p) for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}

        # Build expected fixture document
        expected_doc = {
            "fixture_id": fid,
            "name": ref_data["name"],
            "reference_file": ref_file.name,
            "local_year": ref_data["local_year"],
            "local_month": ref_data["local_month"],
            "local_day": ref_data["local_day"],
            "local_hour": ref_data["local_hour"],
            "local_minute": ref_data["local_minute"],
            "timezone_str": ref_data["timezone_str"],
            "birth_datetime_utc": ref_data["birth_datetime_utc"],
            "julian_day": ref_data["julian_day"],
            "latitude": ref_data["latitude"],
            "longitude": ref_data["longitude"],
            "ascendant_sidereal_longitude": ref_data["ascendant_sidereal_longitude"],
            "mc_sidereal_longitude": ref_data["mc_sidereal_longitude"],
            "ayanamsha": ref_data["ayanamsha"],
            "planets": ref_data["planets"],
            "expected": {
                "shadbala": shadbala_expected,
                "ashtakavarga": {
                    "bav": bav_expected,
                    "sav": sav_expected,
                    "sav_total": sum(sav_expected)
                }
            }
        }

        # Compute SHA-256 integrity hash
        payload_bytes = json.dumps(expected_doc, sort_keys=True).encode("utf-8")
        integrity_hash = hashlib.sha256(payload_bytes).hexdigest()
        expected_doc["integrity_hash"] = integrity_hash

        out_file = exp_dir / f"{fid}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(expected_doc, f, indent=2)

if __name__ == "__main__":
    generate_frozen_expected_fixtures()
    print("Successfully generated all frozen expected JSON fixtures with zero production engine imports!")
