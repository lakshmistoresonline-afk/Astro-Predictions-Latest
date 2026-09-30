"""
Section 28 Final Zero-Trust Architecture Test.
Temporarily isolates all previous R7 certification reports and runs the R7-R7 certification runner.
Verifies that certification status is derived 100% from live execution and does NOT depend on old JSON files.
"""
import shutil
import subprocess
import sys
from pathlib import Path

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr

def run_zero_trust_test():
    print("============================================================")
    print("STARTING SECTION 28 FINAL ZERO-TRUST ARCHITECTURE TEST")
    print("============================================================")

    reports_dir = Path("reports/r7")
    isolated_dir = Path("reports/r7_isolated_backup")

    # 1. Temporarily isolate all historical R7 report directories
    if isolated_dir.exists():
        shutil.rmtree(isolated_dir)
    shutil.copytree(reports_dir, isolated_dir)

    try:
        # Wipe reports/r7 completely
        shutil.rmtree(reports_dir)
        reports_dir.mkdir(parents=True, exist_ok=True)

        print("[INFO] Historical R7 reports isolated. Executing R7-R7 certification runner on clean directory...")

        # 2. Run R7-R7 certification runner on clean directory
        code, out, err = run_cmd("python scripts/run_phase_2e_r4_1_r7_r7_certification.py")
        print("Certification exit code on clean directory:", code)

        assert code == 0, f"Zero-trust architecture test failed! Runner failed without old reports. Exit code: {code}\nOutput:\n{out}\nError:\n{err}"
        assert "FINAL CERTIFICATION STATUS: CERTIFIED" in out, "Zero-trust architecture test failed to reach CERTIFIED status!"

        print("[PASS] Zero-Trust Architecture Test Passed! Certification runner independently derived CERTIFIED status with ZERO dependency on old report files!")

    finally:
        # Restore historical report copies
        if isolated_dir.exists():
            for sub_dir in isolated_dir.iterdir():
                dst = reports_dir / sub_dir.name
                if dst.exists():
                    shutil.rmtree(dst) if dst.is_dir() else dst.unlink()
                if sub_dir.is_dir():
                    shutil.copytree(sub_dir, dst)
                else:
                    shutil.copy(sub_dir, dst)
            shutil.rmtree(isolated_dir)

    # 3. Re-run clean certification runner
    code, out, err = run_cmd("python scripts/run_phase_2e_r4_1_r7_r7_certification.py")
    assert code == 0, "Post-restoration certification runner failed!"
    print("[PASS] Post-Restoration Certification Execution PASS (Exit code 0)")

    print("============================================================")
    print("ZERO-TRUST ARCHITECTURE TEST VERIFIED 100%!")
    print("============================================================")

if __name__ == "__main__":
    run_zero_trust_test()
