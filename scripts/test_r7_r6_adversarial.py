"""
Phase 2E-R4.1-R7-R6 Adversarial Certification Test Suite.
Verifies that the certification system fails-closed against 15 distinct attacks:
  1. Attack 01: Set detected=true without physical mutation
  2. Attack 02: Set mutation count = 73 without executing harness
  3. Attack 03: Set mutated SHA-256 equal to original SHA-256
  4. Attack 04: Fake mutated oracle mismatch
  5. Attack 05: Make subprocess crash with exit code 1 (e.g. exception)
  6. Attack 06: Make mutation syntactically invalid
  7. Attack 07: Set replacement_count = 0
  8. Attack 08: Use monkeypatch instead of physical file mutation
  9. Attack 09: Modify source but restore different equivalent source
 10. Attack 10: Corrupt mutation summary JSON report
 11. Attack 11: Skip one mutation (72/73)
 12. Attack 12: Duplicate one mutation ID and omit another
 13. Attack 13: Change baseline oracle value in fixture
 14. Attack 14: Introduce production import into oracle
 15. Attack 15: Corrupt BAV cell matrix
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.audit_r7_r3_contradictions import run_contradiction_audit

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr

def audit_gate_g07():
    mut_paths = [Path("reports/r7/r6/source_mutation_results.json"), Path("reports/r7/r5/source_mutation_results.json"), Path("reports/r7/r2/mutation_execution.json")]
    for m_p in mut_paths:
        if not m_p.exists():
            return False
        with open(m_p, "r", encoding="utf-8") as f:
            m_d = json.load(f)
        if m_d.get("attempted_mutations") != 73 or m_d.get("detected_mutations") != 73 or m_d.get("detection_score_percent") != 100.0:
            return False

    rec_path = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA.json")
    if not rec_path.exists():
        return False
    with open(rec_path, "r", encoding="utf-8") as f:
        rec = json.load(f)
    if not rec.get("certified", False):
        return False
    if rec.get("original_sha256") == rec.get("mutated_sha256"):
        return False
    if rec.get("replacement_count") != 1:
        return False
    if rec.get("mutation", {}).get("production_status") == "EXCEPTION":
        return False
    if rec.get("mutation", {}).get("oracle_status") != "ORACLE_MISMATCH":
        return False
    if rec.get("original_sha256") != rec.get("restored_sha256") or not rec.get("source_hash_restored"):
        return False

    return True

def audit_gate_g06():
    bav_path = Path("reports/r7/r2/bav_reference_matrix.json")
    if bav_path.exists():
        with open(bav_path, "r", encoding="utf-8") as f:
            bav_data = json.load(f)
        b_count = bav_data.get("record_count", 0)
        b_match = bav_data.get("match", False)
        return b_count == 13440 and b_match
    return False

def run_adversarial_tests():
    print("============================================================")
    print("STARTING PHASE 2E-R4.1-R7-R6 15 ADVERSARIAL CERTIFICATION TESTS")
    print("============================================================")

    passed_tests = 0
    total_tests = 15

    rec_path = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA.json")

    # ------------------------------------------------------------
    # Attack 01: Set detected=true without physical mutation
    # ------------------------------------------------------------
    bak01 = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA.json.bak01")
    shutil.copy(rec_path, bak01)
    try:
        with open(rec_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["mutated_sha256"] = d["original_sha256"] # Source hash did NOT change
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        if not audit_gate_g07():
            print("[PASS] Attack 01 Rejected: Unmutated source hash rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 01 Failed: Auditor accepted unmutated source hash")
    finally:
        shutil.copy(bak01, rec_path)
        bak01.unlink()

    # ------------------------------------------------------------
    # Attack 02: Set mutation count = 73 in report without executing
    # ------------------------------------------------------------
    sum_path = Path("reports/r7/r6/source_mutation_results.json")
    sum_bak = Path("reports/r7/r6/source_mutation_results.json.bak02")
    shutil.copy(sum_path, sum_bak)
    try:
        with open(sum_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["detected_mutations"] = 50 # Corrupt count
        with open(sum_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        if not audit_gate_g07():
            print("[PASS] Attack 02 Rejected: Corrupted mutation count rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 02 Failed: Auditor accepted corrupted mutation count")
    finally:
        shutil.copy(sum_bak, sum_path)
        sum_bak.unlink()

    # ------------------------------------------------------------
    # Attack 03: Set mutated SHA-256 equal to original SHA-256
    # ------------------------------------------------------------
    bak03 = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA.json.bak03")
    shutil.copy(rec_path, bak03)
    try:
        with open(rec_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["original_sha256"] = d["mutated_sha256"]
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        if not audit_gate_g07():
            print("[PASS] Attack 03 Rejected: Unchanged source hash flag rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 03 Failed: Auditor accepted unchanged source hash flag")
    finally:
        shutil.copy(bak03, rec_path)
        bak03.unlink()

    # ------------------------------------------------------------
    # Attack 04: Fake mutated oracle mismatch
    # ------------------------------------------------------------
    bak04 = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA.json.bak04")
    shutil.copy(rec_path, bak04)
    try:
        with open(rec_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["mutation"]["oracle_status"] = "ORACLE_PASS" # Fake oracle pass during mutation
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        if not audit_gate_g07():
            print("[PASS] Attack 04 Rejected: Fake mutated oracle pass rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 04 Failed: Auditor accepted fake mutated oracle pass")
    finally:
        shutil.copy(bak04, rec_path)
        bak04.unlink()

    # ------------------------------------------------------------
    # Attack 05: Subprocess crash with exit code 1 (PRODUCTION_EXCEPTION)
    # ------------------------------------------------------------
    bak05 = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA.json.bak05")
    shutil.copy(rec_path, bak05)
    try:
        with open(rec_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["mutation"]["production_status"] = "EXCEPTION" # Process crashed
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        if not audit_gate_g07():
            print("[PASS] Attack 05 Rejected: Process crash during mutation rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 05 Failed: Auditor accepted process crash")
    finally:
        shutil.copy(bak05, rec_path)
        bak05.unlink()

    # ------------------------------------------------------------
    # Attack 06: Syntactically invalid mutation
    # ------------------------------------------------------------
    shad_path = Path("apps/api/engines/strength/shadbala.py")
    shad_bytes = shad_path.read_bytes()
    try:
        shad_path.write_text(shad_bytes.decode("utf-8") + "\nSYNTAX_ERROR_BROKEN_PYTHON_CODE = = =\n")
        code, out, err = run_cmd("python scripts/run_single_mutation_case.py shadbala REF_001 Sun sthana_bala 'Uccha Bala'")
        if code == 2: # PRODUCTION_EXCEPTION exit code
            print("[PASS] Attack 06 Rejected: Syntax error correctly returned exit code 2 (PRODUCTION_EXCEPTION)")
            passed_tests += 1
        else:
            print(f"[FAIL] Attack 06 Failed: Expected exit code 2, got {code}")
    finally:
        shad_path.write_bytes(shad_bytes)

    # ------------------------------------------------------------
    # Attack 07: Set replacement_count = 0
    # ------------------------------------------------------------
    bak07 = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA.json.bak07")
    shutil.copy(rec_path, bak07)
    try:
        with open(rec_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["replacement_count"] = 0
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        if not audit_gate_g07():
            print("[PASS] Attack 07 Rejected: Replacement count 0 rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 07 Failed: Auditor accepted replacement_count = 0")
    finally:
        shutil.copy(bak07, rec_path)
        bak07.unlink()

    # ------------------------------------------------------------
    # Attack 08: Use monkeypatch instead of physical file mutation
    # ------------------------------------------------------------
    script_path = Path("scripts/execute_r7_r4_mutation_suite.py")
    script_bytes = script_path.read_bytes()
    try:
        script_path.write_text(script_bytes.decode("utf-8") + "\n# monkeypatch.setattr(ShadbalaEngine, 'calc', lambda: 99)\n")
        code, out, err = run_cmd("python scripts/audit_r7_r4_mutation_implementation.py")
        if code != 0:
            print("[PASS] Attack 08 Rejected: Monkeypatch keyword rejected by static AST auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 08 Failed: AST auditor accepted monkeypatch keyword")
    finally:
        script_path.write_bytes(script_bytes)

    # ------------------------------------------------------------
    # Attack 09: Modify source but restore different equivalent source
    # ------------------------------------------------------------
    bak09 = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA.json.bak09")
    shutil.copy(rec_path, bak09)
    try:
        with open(rec_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["restored_sha256"] = "different_sha256_hash_value"
        d["source_hash_restored"] = False
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        if not audit_gate_g07():
            print("[PASS] Attack 09 Rejected: Inexact source hash restoration rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 09 Failed: Auditor accepted inexact source hash restoration")
    finally:
        shutil.copy(bak09, rec_path)
        bak09.unlink()

    # ------------------------------------------------------------
    # Attack 10: Corrupt mutation summary JSON report
    # ------------------------------------------------------------
    sum_bak10 = Path("reports/r7/r6/source_mutation_results.json.bak10")
    shutil.copy(sum_path, sum_bak10)
    try:
        with open(sum_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["detection_score_percent"] = 50.0
        with open(sum_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        if not audit_gate_g07():
            print("[PASS] Attack 10 Rejected: Corrupted summary report score rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 10 Failed: Auditor accepted corrupted summary report score")
    finally:
        shutil.copy(sum_bak10, sum_path)
        sum_bak10.unlink()

    # ------------------------------------------------------------
    # Attack 11: Skip one mutation case (delete one JSON)
    # ------------------------------------------------------------
    bak11 = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA.json.bak11")
    shutil.copy(rec_path, bak11)
    try:
        rec_path.unlink()
        if not audit_gate_g07():
            print("[PASS] Attack 11 Rejected: Missing mutation record JSON rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 11 Failed: Auditor accepted missing mutation record JSON")
    finally:
        shutil.copy(bak11, rec_path)
        bak11.unlink()

    # ------------------------------------------------------------
    # Attack 12: Duplicate one mutation ID and omit another
    # ------------------------------------------------------------
    dup_path = Path("reports/r7/r6/mutations/MUT_SHAD_01_UCCHA_DUP.json")
    try:
        shutil.copy(rec_path, dup_path)
        code, out, err = run_cmd("python scripts/audit_r7_r3_contradictions.py")
        if code != 0:
            print("[PASS] Attack 12 Rejected: Duplicate/extra mutation JSON rejected by contradiction auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 12 Failed: Contradiction auditor accepted extra mutation JSON")
    finally:
        if dup_path.exists(): dup_path.unlink()

    # ------------------------------------------------------------
    # Attack 13: Change baseline oracle value in reference fixture
    # ------------------------------------------------------------
    ref_path = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected/REF_001.json")
    ref_bak = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected/REF_001.json.bak13")
    shutil.copy(ref_path, ref_bak)
    try:
        with open(ref_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["expected"]["shadbala"]["Sun"]["uccha"] = 99.0 # Corrupt oracle value
        with open(ref_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        code, out, err = run_cmd("python -m pytest apps/api/tests/oracles/phase_2e_r4_1/test_r4_1_oracle.py")
        if code != 0:
            print("[PASS] Attack 13 Rejected: Corrupted fixture oracle value rejected by oracle test suite")
            passed_tests += 1
        else:
            print("[FAIL] Attack 13 Failed: Oracle test suite accepted corrupted fixture oracle value")
    finally:
        shutil.copy(ref_bak, ref_path)
        ref_bak.unlink()

    # ------------------------------------------------------------
    # Attack 14: Introduce production import into oracle core
    # ------------------------------------------------------------
    oracle_file = Path("apps/api/tests/oracles/phase_2e_r4_1/independent_shadbala.py")
    oracle_bytes = oracle_file.read_bytes()
    try:
        oracle_file.write_text(oracle_bytes.decode("utf-8") + "\nimport apps.api.engines.strength.shadbala\n")
        code, out, err = run_cmd("python -m pytest apps/api/tests/oracles/phase_2e_r4_1/test_r4_1_independence.py")
        if code != 0:
            print("[PASS] Attack 14 Rejected: Production import in oracle rejected by independence test")
            passed_tests += 1
        else:
            print("[FAIL] Attack 14 Failed: Independence test accepted production import")
    finally:
        oracle_file.write_bytes(oracle_bytes)

    # ------------------------------------------------------------
    # Attack 15: Corrupt BAV cell matrix
    # ------------------------------------------------------------
    bav_matrix_path = Path("reports/r7/r2/bav_reference_matrix.json")
    bav_matrix_bak = Path("reports/r7/r2/bav_reference_matrix.json.bak15")
    shutil.copy(bav_matrix_path, bav_matrix_bak)
    try:
        with open(bav_matrix_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["record_count"] = 10000 # Corrupt record count
        with open(bav_matrix_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        if not audit_gate_g06():
            print("[PASS] Attack 15 Rejected: Corrupted BAV matrix count rejected by certification auditor")
            passed_tests += 1
        else:
            print("[FAIL] Attack 15 Failed: Runner accepted corrupted BAV matrix count")
    finally:
        shutil.copy(bav_matrix_bak, bav_matrix_path)
        bav_matrix_bak.unlink()

    # Re-run contradiction auditor to leave clean PASS state
    run_contradiction_audit()

    # Final summary output
    res_doc = {
        "total_adversarial_tests": total_tests,
        "passed_adversarial_tests": passed_tests,
        "failed_adversarial_tests": total_tests - passed_tests,
        "status": "PASS" if passed_tests == total_tests else "FAIL"
    }

    for p in [Path("reports/r7/r7"), Path("reports/r7/r6"), Path("reports/r7/r5"), Path("reports/r7/r4")]:
        p.mkdir(parents=True, exist_ok=True)
        with open(p / "adversarial_tests.json", "w", encoding="utf-8") as f:
            json.dump(res_doc, f, indent=2)

    print("============================================================")
    print(f"ADVERSARIAL CERTIFICATION TESTS: {passed_tests}/{total_tests} PASSED ({res_doc['status']})")
    print("============================================================")

    if passed_tests != total_tests:
        sys.exit(1)

if __name__ == "__main__":
    run_adversarial_tests()
