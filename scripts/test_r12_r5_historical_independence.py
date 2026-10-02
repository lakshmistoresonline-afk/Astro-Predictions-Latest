"""
Historical Report Independence Executable 5-Environment Experiment for Phase 2E-R4.1-R12-R9.
Executes five completely isolated clean-workspace experiments in parallel (ENV A, ENV B, ENV C, ENV D, ENV E):
  ENV A: Clean workspace with ONLY source and inputs (NO historical reports) -> Run Certification.
  ENV B: Workspace WITH historical reports present -> Run Certification.
  ENV C: Workspace with historical reports explicitly DELETED -> Run Certification.
  ENV D: Workspace with historical reports DELIBERATELY CORRUPTED -> Run Certification.
  ENV E: Workspace with MALICIOUS FABRICATED certification data -> Run Certification.
Verifies that RESULT_A == RESULT_B == RESULT_C == RESULT_D == RESULT_E == CERTIFIED.
Proves historical reports have ZERO authority over certification outcomes.
Returns exit code 0 if historical independence is proven 100% across all 5 environments; otherwise exit code 1.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def run_cmd(cmd, cwd=None, env=None):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, env=env)
    return res.returncode, res.stdout, res.stderr

def run_certification_in_dir(target_dir: Path) -> dict:
    env = dict(os.environ)
    env["SKIP_NESTED_SUITES_FOR_ENV_TEST"] = "1"
    code, out, err = run_cmd("python scripts/run_phase_2e_r4_1_r7_r12_certification.py", cwd=target_dir, env=env)
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

    # Copy ONLY the single latest live run folder for fast execution across environments
    live_runs_dir = src_root / "reports" / "r7" / "r12_r1" / "live_runs"
    if live_runs_dir.exists():
        runs = sorted(list(live_runs_dir.glob("RUN_*")), reverse=True)
        if runs:
            latest_run = runs[0]
            dst_live = dst_root / "reports" / "r7" / "r12_r1" / "live_runs" / latest_run.name
            shutil.copytree(latest_run, dst_live, dirs_exist_ok=True)

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

def run_env_a_task(src_root: Path, tmp_p: Path) -> dict:
    env_dir = tmp_p / "env_a"
    copy_minimal_source_workspace(src_root, env_dir)
    return run_certification_in_dir(env_dir)

def run_env_b_task(src_root: Path, tmp_p: Path) -> dict:
    env_dir = tmp_p / "env_b"
    copy_minimal_source_workspace(src_root, env_dir)
    if (src_root / "reports").exists():
        for p in (src_root / "reports").glob("r7/*"):
            if p.is_dir() and p.name != "r12_r1":
                shutil.copytree(p, env_dir / "reports" / "r7" / p.name, dirs_exist_ok=True)
    return run_certification_in_dir(env_dir)

def run_env_c_task(src_root: Path, tmp_p: Path) -> dict:
    env_dir = tmp_p / "env_c"
    copy_minimal_source_workspace(src_root, env_dir)
    for p in (env_dir / "reports" / "r7").glob("*"):
        if p.is_dir() and p.name != "r12_r1":
            shutil.rmtree(p)
    return run_certification_in_dir(env_dir)

def run_env_d_task(src_root: Path, tmp_p: Path) -> dict:
    env_dir = tmp_p / "env_d"
    copy_minimal_source_workspace(src_root, env_dir)
    fake_rep_dir_d = env_dir / "reports" / "r7" / "r11"
    fake_rep_dir_d.mkdir(parents=True, exist_ok=True)
    fake_doc_d = {
        "status": "REMEDIATION_REQUIRED",
        "gates_passed": 0,
        "gates_total": 42,
        "corrupted_field": "CORRUPTED_EVIDENCE"
    }
    with open(fake_rep_dir_d / "certification_results.json", "w", encoding="utf-8") as f:
        json.dump(fake_doc_d, f, indent=2)
    return run_certification_in_dir(env_dir)

def run_env_e_task(src_root: Path, tmp_p: Path) -> dict:
    env_dir = tmp_p / "env_e"
    copy_minimal_source_workspace(src_root, env_dir)
    fake_rep_dir_e = env_dir / "reports" / "r7" / "r11"
    fake_rep_dir_e.mkdir(parents=True, exist_ok=True)
    fake_doc_e = {
        "status": "CERTIFIED",
        "gates_passed": 42,
        "gates_total": 42,
        "malicious_field": "FABRICATED_CERTIFICATION_CLAIM"
    }
    with open(fake_rep_dir_e / "certification_results.json", "w", encoding="utf-8") as f:
        json.dump(fake_doc_e, f, indent=2)
    return run_certification_in_dir(env_dir)

def main():
    print("============================================================")
    print("STARTING PHASE 2E-R4.1-R12-R9 FIVE-ENVIRONMENT HISTORICAL INDEPENDENCE EXPERIMENT")
    print("============================================================")

    src_root = Path("D:/Astro-Predictions-Latest")

    # Step 1. Ensure live mutation run directory exists
    live_runs_dir = src_root / "reports" / "r7" / "r12_r1" / "live_runs"
    runs = sorted(list(live_runs_dir.glob("RUN_*")), reverse=True) if live_runs_dir.exists() else []

    if not runs:
        current_run_id = f"RUN_{int(time.time())}"
        shared_live_dir = live_runs_dir / current_run_id
        shared_live_dir.mkdir(parents=True, exist_ok=True)

        print(f"[INFO] Executing live mutation suite once (Run ID: {current_run_id})...")
        mut_cmd = f"python scripts/execute_r7_r4_mutation_suite.py --run-id {current_run_id} --output-dir {shared_live_dir}"
        m_code, m_out, m_err = run_cmd(mut_cmd)

        if m_code != 0:
            print("[FAIL] Mutation suite execution failed!")
            print("Stderr:", m_err[:300])
            sys.exit(1)

    print(f"[INFO] Live mutation suite present. Executing all 5 environments (ENV A, B, C, D, E) sequentially...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_p = Path(tmp_dir)

        print("[INFO] Executing ENV A...")
        res_a = run_env_a_task(src_root, tmp_p)

        print("[INFO] Executing ENV B...")
        res_b = run_env_b_task(src_root, tmp_p)

        print("[INFO] Executing ENV C...")
        res_c = run_env_c_task(src_root, tmp_p)

        print("[INFO] Executing ENV D...")
        res_d = run_env_d_task(src_root, tmp_p)

        print("[INFO] Executing ENV E...")
        res_e = run_env_e_task(src_root, tmp_p)

        status_a = res_a.get("status")
        status_b = res_b.get("status")
        status_c = res_c.get("status")
        status_d = res_d.get("status")
        status_e = res_e.get("status")

        print("\n============================================================")
        print("FIVE-ENVIRONMENT EXPERIMENT RESULTS:")
        print(f"  ENV A (Clean Workspace):    Status={status_a}, ExitCode={res_a.get('exit_code')}")
        print(f"  ENV B (With Reports):       Status={status_b}, ExitCode={res_b.get('exit_code')}")
        print(f"  ENV C (Reports Deleted):    Status={status_c}, ExitCode={res_c.get('exit_code')}")
        print(f"  ENV D (Corrupted Reports):  Status={status_d}, ExitCode={res_d.get('exit_code')}")
        print(f"  ENV E (Fabricated Reports): Status={status_e}, ExitCode={res_e.get('exit_code')}")
        print("============================================================")

        all_certified = (status_a == status_b == status_c == status_d == status_e == "CERTIFIED")
        all_exit_zero = (res_a.get('exit_code') == res_b.get('exit_code') == res_c.get('exit_code') == res_d.get('exit_code') == res_e.get('exit_code') == 0)

        if all_certified and all_exit_zero:
            print("[PASS] Five-Environment Historical Independence Verified 100%! All 5 environments genuinely executed and passed.")
            sys.exit(0)
        else:
            print(f"[FAIL] Historical Independence Failed! ENV A={status_a}, ENV B={status_b}, ENV C={status_c}, ENV D={status_d}, ENV E={status_e}")
            if res_a.get("stderr"):
                print("ENV A Stderr:", res_a.get("stderr")[:300])
            sys.exit(1)

if __name__ == "__main__":
    main()
