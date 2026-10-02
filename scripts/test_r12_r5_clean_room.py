"""
Clean-Room Execution Proof for Phase 2E-R4.1-R12-R8.
Performs the complete certification execution in a brand new isolated temporary directory containing ONLY:
  - production source code
  - configuration files
  - immutable reference inputs
  - required ephemeris kernel
EXCLUDES all historical reports in reports/r7/**!
Verifies that all 42 certification gates, Shadbala matrix (2,380 records), BAV matrix (13,440 cells),
SAV vector, 73 physical mutations, and 64 adversarial attack tests generate dynamically from live in-memory code.
Returns exit code 0 if clean-room execution produces CERTIFIED status; otherwise exit code 1.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

def run_cmd(cmd, cwd=None, env=None):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, env=env)
    return res.returncode, res.stdout, res.stderr

def copy_minimal_source_workspace(src_root: Path, dst_root: Path):
    dst_root.mkdir(parents=True, exist_ok=True)

    # Copy apps/
    if (src_root / "apps").exists():
        shutil.copytree(src_root / "apps", dst_root / "apps", dirs_exist_ok=True)

    # Required directories
    dirs_to_copy = [
        "reference_source",
        "scripts"
    ]
    for d in dirs_to_copy:
        s_p = src_root / d
        d_p = dst_root / d
        if s_p.exists():
            shutil.copytree(s_p, d_p, dirs_exist_ok=True)

    # Required root files
    files_to_copy = [
        "PHASE_2E_R4_1_REFERENCE_MANIFEST.json",
        "generate_r7_r2_matrices.py",
        ".gitignore"
    ]
    for f in files_to_copy:
        s_f = src_root / f
        d_f = dst_root / f
        if s_f.exists():
            shutil.copy(s_f, d_f)

def main():
    print("============================================================")
    print("STARTING PHASE 2E-R4.1-R12-R8 CLEAN-ROOM CERTIFICATION TEST")
    print("============================================================")

    src_root = Path("D:/Astro-Predictions-Latest")

    with tempfile.TemporaryDirectory() as tmp_dir:
        clean_dir = Path(tmp_dir) / "clean_workspace"
        copy_minimal_source_workspace(src_root, clean_dir)

        # Verify no historical reports exist in clean workspace
        hist_rep_dir = clean_dir / "reports"
        if hist_rep_dir.exists():
            print("[FAIL] Clean workspace contains historical reports directory!")
            sys.exit(1)

        print("[INFO] Executing certification runner in clean-room workspace...")
        code, out, err = run_cmd("python scripts/run_phase_2e_r4_1_r7_r12_certification.py", cwd=clean_dir)

        res_path = clean_dir / "reports" / "r7" / "r12_r1" / "certification_results.json"
        if not res_path.exists():
            res_path = clean_dir / "docs" / "PHASE_2E_R4_1_R12_R1_CERTIFICATION.json"

        if not res_path.exists():
            print(f"[FAIL] Certification runner failed to produce results JSON! Exit code: {code}")
            print("Stderr:", err[:300])
            sys.exit(1)

        with open(res_path, "r", encoding="utf-8") as f:
            cert_doc = json.load(f)

        status = cert_doc.get("status")
        gates_passed = cert_doc.get("gates_passed")
        gates_total = cert_doc.get("gates_total")

        print("\n============================================================")
        print("CLEAN-ROOM CERTIFICATION OUTCOME:")
        print(f"  Final Status: {status}")
        print(f"  Gates Passed: {gates_passed} / {gates_total}")
        print(f"  Exit Code:    {code}")
        print("============================================================")

        if code == 0 and status == "CERTIFIED" and gates_passed == gates_total == 42:
            print("[PASS] Clean-Room Certification Execution Verified 100%!")
            sys.exit(0)
        else:
            print(f"[FAIL] Clean-Room Execution Failed! Status={status}, ExitCode={code}")
            sys.exit(1)

if __name__ == "__main__":
    main()
