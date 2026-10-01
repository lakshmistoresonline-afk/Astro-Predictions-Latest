"""
Historical Report Independence Executable Experiment for Phase 2E-R4.1-R12-R5.
Executes isolated clean-workspace experiments:
  RUN A: Clean workspace with ONLY source and inputs (NO historical reports) -> Run Certification.
  RUN D: Isolated workspace with DELIBERATELY FAKED/CORRUPTED historical report -> Run Certification.
Verifies that RUN A == CERTIFIED and RUN D == CERTIFIED (faked report ignored).
Proves historical reports have ZERO authority over certification outcomes.
Returns exit code 0 if historical independence is proven 100%; otherwise exit code 1.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return res.returncode, res.stdout, res.stderr

def run_certification_in_dir(target_dir: Path) -> dict:
    code, out, err = run_cmd("python scripts/run_phase_2e_r4_1_r7_r12_certification.py", cwd=target_dir)
    res_path = target_dir / "reports" / "r7" / "r12_r1" / "certification_results.json"
    if not res_path.exists():
        res_path = target_dir / "docs" / "PHASE_2E_R4_1_R12_R1_CERTIFICATION.json"

    if res_path.exists():
        with open(res_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["exit_code"] = code
        return d
    return {"exit_code": code, "status": "FAILED_TO_PRODUCE_REPORT", "stderr": err}

def copy_minimal_source_workspace(src_root: Path, dst_root: Path):
    dst_root.mkdir(parents=True, exist_ok=True)

    # Copy entire apps/ directory
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
    print("STARTING PHASE 2E-R4.1-R12-R5 HISTORICAL INDEPENDENCE EXPERIMENT")
    print("============================================================")

    src_root = Path("D:/Astro-Predictions-Latest")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_p = Path(tmp_dir)

        # 1. RUN A: Clean workspace with ONLY source and inputs (NO historical reports)
        run_a_dir = tmp_p / "run_a"
        copy_minimal_source_workspace(src_root, run_a_dir)
        print("[INFO] Executing RUN A (Clean workspace without reports)...")
        res_a = run_certification_in_dir(run_a_dir)

        # 2. RUN D: Workspace with FAKED/CORRUPTED historical reports
        run_d_dir = tmp_p / "run_d"
        copy_minimal_source_workspace(src_root, run_d_dir)
        fake_rep_dir = run_d_dir / "reports" / "r7" / "r12_r1"
        fake_rep_dir.mkdir(parents=True, exist_ok=True)
        fake_doc = {
            "status": "REMEDIATION_REQUIRED",
            "gates_passed": 0,
            "gates_total": 42,
            "fake_field": "DELIBERATE_CORRUPTION"
        }
        with open(fake_rep_dir / "certification_results.json", "w", encoding="utf-8") as f:
            json.dump(fake_doc, f, indent=2)
        print("[INFO] Executing RUN D (Workspace with FAKED/CORRUPTED report)...")
        res_d = run_certification_in_dir(run_d_dir)

        status_a = res_a.get("status")
        status_d = res_d.get("status")

        print("\n============================================================")
        print("EXPERIMENT RESULTS:")
        print(f"  RUN A (Clean Workspace): Status={status_a}, ExitCode={res_a.get('exit_code')}")
        print(f"  RUN D (Corrupted Report):Status={status_d}, ExitCode={res_d.get('exit_code')}")
        print("============================================================")

        if status_a == "CERTIFIED" and status_d == "CERTIFIED" and res_a.get("exit_code") == 0 and res_d.get("exit_code") == 0:
            print("[PASS] Historical Independence Verified! Certification status is 100% independent of reports.")
            sys.exit(0)
        else:
            print(f"[FAIL] Historical Independence Failed! RUN A status={status_a}, ExitCode={res_a.get('exit_code')}")
            if res_a.get("stderr"):
                print("RUN A Stderr:", res_a.get("stderr")[:300])
            sys.exit(1)

if __name__ == "__main__":
    main()
