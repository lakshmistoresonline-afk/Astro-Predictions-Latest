"""
Gate G42 Git Working Tree Integrity Test Harness for Phase 2E-R4.1-R12-R5.
Executes real subprocess calls to `git status --porcelain` and tests fail-closed behavior across:
  A. Clean repository -> PASS
  B. Modify tracked file -> FAIL
  C. Create untracked file -> FAIL
  D. Delete tracked file -> FAIL
  E. Modify report file -> FAIL
  F. Restore exact original state -> PASS
Returns exit code 0 if all 6 test scenarios pass; otherwise exit code 1.
"""
import subprocess
import sys
from pathlib import Path

def check_git_status_porcelain() -> bool:
    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=False)
    return res.returncode == 0 and res.stdout.strip() == ""

def main():
    print("============================================================")
    print("STARTING GATE G42 GIT INTEGRITY TEST HARNESS")
    print("============================================================")

    # A. Initial Clean Check
    if not check_git_status_porcelain():
        print("[FAIL] Scenario A Failed: Initial working tree is dirty!")
        sys.exit(1)
    print("[PASS] Scenario A Passed: Clean working tree returns PASS (git status --porcelain == '')")

    # B. Modify Tracked File Test
    target_file = Path("apps/api/config.py")
    orig_bytes = target_file.read_bytes()
    try:
        target_file.write_bytes(orig_bytes + b"\n# G42_TEMPORARY_MODIFICATION\n")
        if check_git_status_porcelain():
            print("[FAIL] Scenario B Failed: Modified tracked file was NOT detected by G42!")
            sys.exit(1)
        print("[PASS] Scenario B Passed: Modified tracked file causes G42 FAIL")
    finally:
        target_file.write_bytes(orig_bytes)

    # C. Create Untracked File Test
    untracked_file = Path("untracked_temp_test_g42.tmp")
    try:
        untracked_file.write_text("temporary untracked file")
        if check_git_status_porcelain():
            print("[FAIL] Scenario C Failed: Untracked file was NOT detected by G42!")
            sys.exit(1)
        print("[PASS] Scenario C Passed: Untracked file causes G42 FAIL")
    finally:
        if untracked_file.exists():
            untracked_file.unlink()

    # D. Delete Tracked File Test
    del_file = Path("docs/PHASE_2E_R12_R5_FORENSIC_INVENTORY.md")
    del_bytes = del_file.read_bytes()
    try:
        del_file.unlink()
        if check_git_status_porcelain():
            print("[FAIL] Scenario D Failed: Deleted tracked file was NOT detected by G42!")
            sys.exit(1)
        print("[PASS] Scenario D Passed: Deleted tracked file causes G42 FAIL")
    finally:
        del_file.write_bytes(del_bytes)

    # E. Modify Report File Test
    rep_file = Path("docs/PHASE_2E_R4_1_R12_R3_FINAL_CERTIFICATION.md")
    rep_bytes = rep_file.read_bytes()
    try:
        rep_file.write_bytes(rep_bytes + b"\n# TEMPORARY_REPORT_EDIT\n")
        if check_git_status_porcelain():
            print("[FAIL] Scenario E Failed: Modified report file was NOT detected by G42!")
            sys.exit(1)
        print("[PASS] Scenario E Passed: Modified report file causes G42 FAIL")
    finally:
        rep_file.write_bytes(rep_bytes)

    # F. Restore Exact Original State Check
    if not check_git_status_porcelain():
        print("[FAIL] Scenario F Failed: Restored working tree is not clean!")
        sys.exit(1)
    print("[PASS] Scenario F Passed: Restored working tree returns PASS (git status --porcelain == '')")

    print("============================================================")
    print("GATE G42 GIT INTEGRITY TEST HARNESS PASSED 100%!")
    print("============================================================")

if __name__ == "__main__":
    main()
