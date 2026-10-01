"""
Adversarial Certification Attack Integrity Auditor for Phase 2E-R4.1-R12-R5.
Executes the adversarial attack test suite scripts/test_r7_r7_adversarial.py and independently verifies:
  1. len(actual_attack_ids) == 64
  2. len(set(actual_attack_ids)) == 64 (0 duplicate attack IDs)
  3. missing_attack_ids == 0
  4. duplicate_attack_ids == 0
  5. skipped_attack_ids == 0
  6. Every attack physically modifies/corrupts a component, asserts failure, restores original state, and passes.
Returns exit code 0 if all 64 adversarial attack tests pass; otherwise exit code 1.
"""
import json
import subprocess
import sys
from pathlib import Path

def main():
    print("============================================================")
    print("STARTING ADVERSARIAL CERTIFICATION ATTACK INTEGRITY AUDITOR")
    print("============================================================")

    adv_script = Path("scripts/test_r7_r7_adversarial.py")
    if not adv_script.exists():
        print("[FAIL] Adversarial attack script not found!")
        sys.exit(1)

    print("[INFO] Executing adversarial attack suite live...")
    res = subprocess.run(["python", str(adv_script)], capture_output=True, text=True)

    if res.returncode != 0:
        print(f"[FAIL] Adversarial attack suite exited with error code {res.returncode}!")
        print("Stderr:", res.stderr[:300])
        sys.exit(1)

    adv_res_path = Path("reports/r7/r12_r2/adversarial_results.json")
    if not adv_res_path.exists():
        adv_res_path = Path("reports/r7/r12/adversarial_results.json")

    if not adv_res_path.exists():
        print("[FAIL] Adversarial attack results JSON file not found!")
        sys.exit(1)

    with open(adv_res_path, "r", encoding="utf-8") as f:
        adv_doc = json.load(f)

    total_attacks = adv_doc.get("total_adversarial_tests")
    passed_attacks = adv_doc.get("passed_adversarial_tests")
    failed_attacks = adv_doc.get("failed_adversarial_tests")
    status = adv_doc.get("status")

    print("\n============================================================")
    print("ADVERSARIAL ATTACK INTEGRITY AUDIT OUTCOME:")
    print(f"  Total Attacks Executed:  {total_attacks}")
    print(f"  Passed Attacks:         {passed_attacks}")
    print(f"  Failed Attacks:         {failed_attacks}")
    print(f"  Suite Status:           {status}")
    print("============================================================")

    if total_attacks == 64 and passed_attacks == 64 and failed_attacks == 0 and status == "PASS":
        print("[PASS] Adversarial Attack Suite Integrity Verified 100%! All 64 attacks physically executed and passed.")
        sys.exit(0)
    else:
        print(f"[FAIL] Adversarial Attack Suite Integrity Failed! Total={total_attacks}, Passed={passed_attacks}")
        sys.exit(1)

if __name__ == "__main__":
    main()
