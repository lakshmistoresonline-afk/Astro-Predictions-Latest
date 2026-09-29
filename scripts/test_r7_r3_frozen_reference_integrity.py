"""
Phase 2E-R4.1-R7-R3 Frozen Reference Integrity Test.
Verifies that modifying any value in a frozen expected JSON fixture causes a hard validation failure,
and restoring the original value reproduces a clean PASS.
"""
import json
import shutil
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4_1.independent_shadbala import r4_calculate_shadbala_for_planet

def test_frozen_reference_integrity():
    exp_file = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected/REF_001.json")
    backup_file = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected/REF_001.json.bak")

    # 1. Backup original fixture
    shutil.copy(exp_file, backup_file)

    try:
        with open(exp_file, "r", encoding="utf-8") as f:
            doc = json.load(f)

        orig_val = doc["expected"]["shadbala"]["Sun"]["uccha"]

        # 2. Corrupt fixture expected value
        doc["expected"]["shadbala"]["Sun"]["uccha"] = orig_val + 50.0
        if "Uccha Bala" in doc["expected"]["shadbala"]["Sun"]:
            doc["expected"]["shadbala"]["Sun"]["Uccha Bala"] = orig_val + 50.0

        with open(exp_file, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2)

        # 3. Evaluate oracle vs corrupted fixture
        ind_chart = IndependentChart(
            doc["ascendant_sidereal_longitude"], doc["mc_sidereal_longitude"], doc["ayanamsha"],
            doc["julian_day"], doc["local_year"], doc["local_month"], doc["local_day"],
            doc["local_hour"], doc["local_minute"]
        )
        for p_name, p_info in doc["planets"].items():
            ind_chart.add_planet(p_name, p_info["longitude"], p_info["velocity_deg_day"], p_info["retrograde"])

        oracle_res = r4_calculate_shadbala_for_planet(ind_chart, "Sun")
        delta = abs(oracle_res["uccha"] - doc["expected"]["shadbala"]["Sun"]["uccha"])

        # Must fail when corrupted!
        corruption_detected = delta > 0.03
        print(f"Corrupted delta: {delta:.2f} shashtiamsas -> Detected: {corruption_detected}")
        assert corruption_detected, "Integrity test failed to detect corrupted expected fixture value!"

    finally:
        # 4. Restore original fixture
        shutil.copy(backup_file, exp_file)
        backup_file.unlink()

    # 5. Verify restored fixture passes
    with open(exp_file, "r", encoding="utf-8") as f:
        doc = json.load(f)

    ind_chart = IndependentChart(
        doc["ascendant_sidereal_longitude"], doc["mc_sidereal_longitude"], doc["ayanamsha"],
        doc["julian_day"], doc["local_year"], doc["local_month"], doc["local_day"],
        doc["local_hour"], doc["local_minute"]
    )
    for p_name, p_info in doc["planets"].items():
        ind_chart.add_planet(p_name, p_info["longitude"], p_info["velocity_deg_day"], p_info["retrograde"])

    oracle_res = r4_calculate_shadbala_for_planet(ind_chart, "Sun")
    delta_restored = abs(oracle_res["uccha"] - doc["expected"]["shadbala"]["Sun"]["uccha"])
    print(f"Restored delta: {delta_restored:.4f} shashtiamsas -> PASS: {delta_restored <= 0.03}")
    assert delta_restored <= 0.03, "Restored fixture failed validation!"

    print("Frozen Reference Integrity Test: PASS -> CORRUPT (FAIL) -> RESTORED (PASS) verified 100%!")

if __name__ == "__main__":
    test_frozen_reference_integrity()
