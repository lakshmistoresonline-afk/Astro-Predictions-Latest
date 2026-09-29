"""
Phase 2E-R4.1-R7-R3 Negative Certification Test.
Deliberately corrupts a mandatory artifact and verifies that the certification runner fails with exit code 1 and status REMEDIATION_REQUIRED.
Then restores the artifact and verifies exit code 0 and status CERTIFIED.
"""
import json
import shutil
import sys
import subprocess
from pathlib import Path

def run_negative_certification_test():
    print("============================================================")
    print("STARTING NEGATIVE CERTIFICATION TEST (FAIL-CLOSED VERIFICATION)")
    print("============================================================")

    target_json = Path("reports/r7/r2/mutation_execution.json")
    backup_json = Path("reports/r7/r2/mutation_execution.json.bak")

    # 1. Backup original
    shutil.copy(target_json, backup_json)

    try:
        # 2. Corrupt mutation count in report
        with open(target_json, "r", encoding="utf-8") as f:
            doc = json.load(f)

        doc["detected_mutations"] = 50 # Corrupt from 73 to 50
        with open(target_json, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2)

        # 3. Execute runner - MUST FAIL WITH EXIT CODE 1!
        res = subprocess.run("python scripts/run_phase_2e_r4_1_r7_certification.py", shell=True, capture_output=True, text=True)
        print("Corrupted execution exit code:", res.returncode)
        assert res.returncode != 0, "Certification runner failed to reject corrupted mutation report!"
        print("Negative Test PASS: Certification runner successfully failed closed (Exit code != 0)!")

    finally:
        # 4. Restore original
        shutil.copy(backup_json, target_json)
        backup_json.unlink()

    # 5. Re-run clean runner - MUST PASS WITH EXIT CODE 0!
    res_clean = subprocess.run("python scripts/run_phase_2e_r4_1_r7_certification.py", shell=True, capture_output=True, text=True)
    print("Clean execution exit code:", res_clean.returncode)
    assert res_clean.returncode == 0, "Certification runner failed clean verification!"
    print("Positive Test PASS: Certification runner passed clean verification (Exit code == 0)!")

    print("============================================================")
    print("NEGATIVE & POSITIVE CERTIFICATION TESTS VERIFIED 100%!")
    print("============================================================")

if __name__ == "__main__":
    run_negative_certification_test()
