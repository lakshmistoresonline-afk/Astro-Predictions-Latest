"""
Astrovision Version 6.0.0 Release Certification System Runner (Phase 2AT Final Closure).
Executes and evaluates the 26 canonical release gates (G01 - G26), generating traceable,
independently verifiable gate execution evidence files in reports/runs/<run_id>/gates/gate_<G_ID>.json
and genuine captured process stdout/stderr output log files in reports/runs/<run_id>/gates/logs/gate_<G_ID>.log
with distinct source_artifact_sha256 and execution_artifact_sha256 digests.
"""
import os
import sys
import io
import json
import hashlib
import platform
import subprocess
import contextlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Tuple

# Canonical Expected SHA-256 Digest for NASA JPL DE440s Ephemeris Kernel (32.7 MB)
EXPECTED_DE440S_SHA256 = "c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2"

# Authoritative 26 Canonical Release Gate Definitions (G01 - G26)
RELEASE_GATES: List[Tuple[str, str, Any]] = [
    ("G01_DE440S_HASH", "NASA JPL DE440s Kernel SHA-256 Checksum", "apps/api/engines/astronomy/de440s.bsp"),
    ("G02_ASTRONOMY", "Sub-Arcsecond Astronomy Accuracy", ["apps/api/tests/test_astronomy_provider.py", "apps/api/tests/test_planetary_schema_integrity.py"]),
    ("G03_TIMEZONE_DST", "Historical IANA Timezones & DST Transitions", ["apps/api/tests/test_timezone_historical.py", "apps/api/tests/test_date_validation_strict.py"]),
    ("G04_RASHI_NAKSHATRA", "Rashi, Nakshatra & Pada Boundary Handling", "apps/api/tests/test_vedic_foundation.py"),
    ("G05_ASCENDANT_HOUSES", "Ascendant & Whole Sign House Divisions", "apps/api/tests/test_vedic_foundation.py"),
    ("G06_VARGAS_D1_D60", "16 Parashari Divisional Charts D1 through D60", "apps/api/tests/test_varga_engine.py"),
    ("G07_VIMSHOTTARI_DASHA", "5-Level Vimshottari Dasha Hierarchy & Timeline", "apps/api/tests/test_dasha_engine.py"),
    ("G08_CLASSICAL_YOGAS", "Parashari Yogas & Independent Oracle Verification", "apps/api/tests/test_yoga_engine.py"),
    ("G09_CLASSICAL_DOSHAS", "Parashari Doshas & Structured Cancellations", "apps/api/tests/test_dosha_engine.py"),
    ("G10_SHADBALA", "Shadbala 6-Bala Strengths & Subcomponents", "apps/api/tests/oracles/phase_2e_shadbala/test_shadbala_oracle.py"),
    ("G11_ASHTAKAVARGA", "Ashtakavarga BAV & Dynamic SAV Bindu Matrix", "apps/api/tests/oracles/phase_2e_ashtakavarga/test_ashtakavarga_oracle.py"),
    ("G12_JAIMINI_SUTRAS", "Jaimini Chara Karakas, Arudha Lagna & Karakamsha", "apps/api/tests/test_release_gate_g12_jaimini.py"),
    ("G13_TRANSITS", "Geocentric Planetary Transits & Aspect Contacts", "apps/api/tests/test_release_gate_g13_transits.py"),
    ("G14_PANCHANGA", "Panchanga Elements & Local Solar Day Timing", "apps/api/tests/test_release_gate_g14_panchanga.py"),
    ("G15_MUHURTA", "Activity Suitability & Rule Precedence", "apps/api/tests/test_release_gate_g15_muhurta.py"),
    ("G16_PREDICTIVE_TIMING", "Convergent Domain Timing Windows", ["apps/api/tests/test_prediction_evidence.py", "apps/api/tests/test_api_contract.py"]),
    ("G17_RECTIFICATION", "Event-Date Driven Birth Time Rectification", "apps/api/tests/test_timezone_historical.py"),
    ("G18_COMPATIBILITY", "Vedic Ashtakoota 36-Point Compatibility", "apps/api/tests/test_compatibility_engine.py"),
    ("G19_PREDICTION_EVIDENCE", "14 Domain Prediction Evidence Synthesis", "apps/api/tests/test_prediction_evidence.py"),
    ("G20_AI_TRUST_BOUNDARY", "Server-Owned Evidence AI Boundary Defense", "apps/api/tests/test_ai_service.py"),
    ("G21_AI_VALIDATION", "Structured Semantic Validation & Repair Pipeline", "apps/api/tests/test_ai_validation_pipeline.py"),
    ("G22_PERSISTENCE", "SQLAlchemy Persistent Relational Models & CRUD", "apps/api/tests/test_persistence_idor.py"),
    ("G23_IDOR_CONTROLS", "Server-Enforced User Ownership & IDOR Security", "apps/api/tests/test_persistence_idor.py"),
    ("G24_API_CONTRACTS", "Versioned /api/v1 OpenAPI & Error Shapes", "apps/api/tests/test_api_contract.py"),
    ("G25_PDF_EXPORT", "30-Section Master Celestial Dossier Treatise PDF Report", ["apps/api/tests/test_pdf_report_engine.py", "apps/api/tests/test_golden_reference_report.py"]),
    ("G26_ADMIN_SECURITY", "Server-Side Admin Key Authentication", "apps/api/tests/test_admin_security.py"),
]

def get_git_commit_sha(root: Path) -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return "unknown_commit"

def is_git_working_tree_clean(root: Path) -> bool:
    try:
        res = subprocess.run(["git", "status", "--porcelain=v1"], cwd=root, capture_output=True, text=True)
        if res.returncode == 0:
            lines = [line.strip() for line in res.stdout.splitlines() if line.strip() and "reports/" not in line and "docs/" not in line]
            return len(lines) == 0
    except Exception:
        pass
    return False

def compute_inventory_hash(node_ids: list) -> str:
    content = "\n".join(sorted(node_ids)).encode("utf-8")
    return hashlib.sha256(content).hexdigest()

class PytestPluginCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.setup_errors = 0
        self.teardown_errors = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1
            elif report.skipped:
                self.skipped += 1
        elif report.when == "setup":
            if report.failed:
                self.setup_errors += 1
                self.failed += 1
            elif report.skipped:
                self.skipped += 1
        elif report.when == "teardown":
            if report.failed:
                self.teardown_errors += 1
                self.failed += 1

def run_release_certification(
    project_root: Optional[Path] = None,
    custom_gates: Optional[List] = None,
    output_dir: Optional[Path] = None,
    run_id: str = "RUN_CERTIFICATION"
) -> Dict[str, Any]:
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    import pytest

    commit_sha = get_git_commit_sha(project_root)
    clean_tree = is_git_working_tree_clean(project_root)

    inv_path = project_root / "reports" / "test_node_inventory.json"
    inv_sha = ""
    if inv_path.exists():
        try:
            inv_data = json.loads(inv_path.read_text(encoding="utf-8"))
            inv_sha = inv_data.get("inventory_sha256", "")
        except Exception:
            pass

    canonical_ids = [g[0] for g in RELEASE_GATES]
    gates_to_run = custom_gates if custom_gates is not None else RELEASE_GATES

    is_custom_run = custom_gates is not None
    is_malformed = False
    malformed_reason = ""

    if is_custom_run:
        if not isinstance(custom_gates, list) or len(custom_gates) == 0:
            is_malformed = True
            malformed_reason = "Custom gates list is empty or not a list."
        else:
            seen_ids = set()
            for g in custom_gates:
                if not (isinstance(g, tuple) or isinstance(g, list)) or len(g) != 3:
                    is_malformed = True
                    malformed_reason = f"Gate definition {g} is not a 3-tuple."
                    break
                g_id, g_title, g_paths = g
                if not isinstance(g_id, str) or not g_id.strip():
                    is_malformed = True
                    malformed_reason = f"Gate ID in {g} is blank or invalid."
                    break
                if g_id in seen_ids:
                    is_malformed = True
                    malformed_reason = f"Duplicate gate ID '{g_id}' detected."
                    break
                seen_ids.add(g_id)
                if not isinstance(g_title, str) or not g_title.strip():
                    is_malformed = True
                    malformed_reason = f"Gate title in {g} is blank or invalid."
                    break

    evaluated_ids = [g[0] for g in gates_to_run] if not is_malformed else []
    if evaluated_ids != canonical_ids:
        is_custom_run = True

    print("================================================================================")
    print("      ASTROVISION VERSION 6.0.0 RELEASE CERTIFICATION SYSTEM RUNNER             ")
    print(f"      Commit SHA: {commit_sha}")
    print(f"      Working Tree Clean: {clean_tree}")
    print("================================================================================")

    gate_results = []
    all_passed = True
    total_tests_executed = 0

    run_base_dir = (output_dir or project_root) / "reports" / "runs" / run_id
    gates_dir = run_base_dir / "gates"
    logs_dir = gates_dir / "logs"
    gates_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    if is_malformed:
        all_passed = False
        log_file = logs_dir / "gate_G_MALFORMED_GATES.log"
        log_text = f"Custom Gate Definition Validation Failed: {malformed_reason}\n"
        log_file.write_text(log_text, encoding="utf-8")
        exec_hash = hashlib.sha256(log_file.read_bytes()).hexdigest()

        m_entry = {
            "gate_id": "G_MALFORMED_GATES",
            "gate_title": "Custom Gate Definition Validation",
            "command": "validate_custom_gates",
            "commit_sha": commit_sha,
            "inventory_sha256": inv_sha,
            "run_id": run_id,
            "exit_code": 1,
            "start_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "end_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": 0.0,
            "tests_collected": 0,
            "tests_passed": 0,
            "tests_failed": 1,
            "tests_skipped": 0,
            "errors": 0,
            "source_artifact_sha256": "malformed_gate_spec",
            "execution_artifact_sha256": exec_hash,
            "artifact_hash": exec_hash,
            "status": "FAIL",
            "tests_run": 0,
            "details": f"Validation failed: {malformed_reason}"
        }
        gate_results.append(m_entry)
        (gates_dir / "gate_G_MALFORMED_GATES.json").write_text(json.dumps(m_entry, indent=2), encoding="utf-8")

    # Pre-flight check for production runs — SHORT-CIRCUIT if dirty working tree or invalid SHA
    if not is_custom_run and (not clean_tree or commit_sha == "unknown_commit"):
        all_passed = False
        log_file = logs_dir / "gate_G00_PREFLIGHT_GIT_CLEAN.log"
        log_text = f"Preflight Clean Working Tree Check Failed (clean={clean_tree}, sha={commit_sha})\n"
        log_file.write_text(log_text, encoding="utf-8")
        exec_hash = hashlib.sha256(log_file.read_bytes()).hexdigest()

        pf_entry = {
            "gate_id": "G00_PREFLIGHT_GIT_CLEAN",
            "gate_title": "Git Working Tree Clean Preflight Check",
            "command": "git status --porcelain",
            "commit_sha": commit_sha,
            "inventory_sha256": inv_sha,
            "run_id": run_id,
            "exit_code": 1,
            "start_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "end_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": 0.0,
            "tests_collected": 0,
            "tests_passed": 0,
            "tests_failed": 1,
            "tests_skipped": 0,
            "errors": 0,
            "source_artifact_sha256": "preflight_git_clean_failed",
            "execution_artifact_sha256": exec_hash,
            "artifact_hash": exec_hash,
            "status": "FAIL",
            "tests_run": 0,
            "details": f"Production certification requires clean working tree and valid commit SHA. (clean={clean_tree}, sha={commit_sha})"
        }
        gate_results.append(pf_entry)
        (gates_dir / "gate_G00_PREFLIGHT_GIT_CLEAN.json").write_text(json.dumps(pf_entry, indent=2), encoding="utf-8")

    # Execute gates only if pre-flight passed and not malformed
    if not is_malformed and (is_custom_run or clean_tree):
        # Handle G01_DE440S_HASH if present in gates_to_run
        g1_tuple = next((g for g in gates_to_run if g[0] == "G01_DE440S_HASH"), None)
        if g1_tuple:
            t_start = datetime.now(timezone.utc)
            path_arg = g1_tuple[2] if isinstance(g1_tuple[2], str) else "apps/api/engines/astronomy/de440s.bsp"
            de440s_path = project_root / path_arg
            if not de440s_path.exists():
                de440s_path = project_root / "apps" / "api" / "engines" / "astronomy" / "de440s.bsp"

            kernel_hash = ""
            if de440s_path.exists() and de440s_path.stat().st_size > 30000000:
                with open(de440s_path, "rb") as f:
                    kernel_hash = hashlib.sha256(f.read()).hexdigest()

                t_end = datetime.now(timezone.utc)
                dur = (t_end - t_start).total_seconds()

                log_file = logs_dir / "gate_G01_DE440S_HASH.log"
                log_text = f"DE440s Kernel Verification Log\nPath: {de440s_path}\nSize: {de440s_path.stat().st_size} bytes\nSHA-256: {kernel_hash}\nExpected: {EXPECTED_DE440S_SHA256}\n"
                log_file.write_text(log_text, encoding="utf-8")
                exec_hash = hashlib.sha256(log_file.read_bytes()).hexdigest()

                if kernel_hash == EXPECTED_DE440S_SHA256:
                    g1_entry = {
                        "gate_id": "G01_DE440S_HASH",
                        "gate_title": "NASA JPL DE440s Kernel SHA-256 Checksum",
                        "command": "apps/api/engines/astronomy/de440s.bsp",
                        "commit_sha": commit_sha,
                        "inventory_sha256": inv_sha,
                        "run_id": run_id,
                        "exit_code": 0,
                        "start_timestamp_utc": t_start.isoformat(),
                        "end_timestamp_utc": t_end.isoformat(),
                        "duration_seconds": dur,
                        "tests_collected": 1,
                        "tests_passed": 1,
                        "tests_failed": 0,
                        "tests_skipped": 0,
                        "errors": 0,
                        "source_artifact_sha256": kernel_hash,
                        "execution_artifact_sha256": exec_hash,
                        "artifact_hash": exec_hash,
                        "status": "PASS",
                        "tests_run": 1,
                        "details": f"DE440s kernel verified ({de440s_path.stat().st_size:,} bytes, SHA-256: {kernel_hash[:16]}...)"
                    }
                    gate_results.append(g1_entry)
                    (gates_dir / "gate_G01_DE440S_HASH.json").write_text(json.dumps(g1_entry, indent=2), encoding="utf-8")
                    total_tests_executed += 1
                else:
                    all_passed = False
                    g1_entry = {
                        "gate_id": "G01_DE440S_HASH",
                        "gate_title": "NASA JPL DE440s Kernel SHA-256 Checksum",
                        "command": "apps/api/engines/astronomy/de440s.bsp",
                        "commit_sha": commit_sha,
                        "inventory_sha256": inv_sha,
                        "run_id": run_id,
                        "exit_code": 1,
                        "start_timestamp_utc": t_start.isoformat(),
                        "end_timestamp_utc": t_end.isoformat(),
                        "duration_seconds": dur,
                        "tests_collected": 1,
                        "tests_passed": 0,
                        "tests_failed": 1,
                        "tests_skipped": 0,
                        "errors": 0,
                        "source_artifact_sha256": kernel_hash or "checksum_mismatch",
                        "execution_artifact_sha256": exec_hash,
                        "artifact_hash": exec_hash,
                        "status": "FAIL",
                        "tests_run": 1,
                        "details": f"Checksum mismatch: got {kernel_hash}, expected {EXPECTED_DE440S_SHA256}"
                    }
                    gate_results.append(g1_entry)
                    (gates_dir / "gate_G01_DE440S_HASH.json").write_text(json.dumps(g1_entry, indent=2), encoding="utf-8")
            else:
                t_end = datetime.now(timezone.utc)
                dur = (t_end - t_start).total_seconds()
                all_passed = False
                log_file = logs_dir / "gate_G01_DE440S_HASH.log"
                log_text = f"DE440s Kernel Verification Log\nMissing kernel file at {de440s_path}\n"
                log_file.write_text(log_text, encoding="utf-8")
                exec_hash = hashlib.sha256(log_file.read_bytes()).hexdigest()

                g1_entry = {
                    "gate_id": "G01_DE440S_HASH",
                    "gate_title": "NASA JPL DE440s Kernel SHA-256 Checksum",
                    "command": "apps/api/engines/astronomy/de440s.bsp",
                    "commit_sha": commit_sha,
                    "inventory_sha256": inv_sha,
                    "run_id": run_id,
                    "exit_code": 1,
                    "start_timestamp_utc": t_start.isoformat(),
                    "end_timestamp_utc": t_end.isoformat(),
                    "duration_seconds": dur,
                    "tests_collected": 0,
                    "tests_passed": 0,
                    "tests_failed": 1,
                    "tests_skipped": 0,
                    "errors": 0,
                    "source_artifact_sha256": "missing_de440s_kernel",
                    "execution_artifact_sha256": exec_hash,
                    "artifact_hash": exec_hash,
                    "status": "FAIL",
                    "tests_run": 0,
                    "details": f"DE440s kernel missing or invalid at {de440s_path}"
                }
                gate_results.append(g1_entry)
                (gates_dir / "gate_G01_DE440S_HASH.json").write_text(json.dumps(g1_entry, indent=2), encoding="utf-8")

        # Remaining Gates: Programmatic Pytest execution with Captured Output Logs
        pytest_gates = [g for g in gates_to_run if g[0] != "G01_DE440S_HASH"]
        for gate_id, title, test_files in pytest_gates:
            t_start = datetime.now(timezone.utc)
            file_list = test_files if isinstance(test_files, list) else [test_files]
            collector = PytestPluginCollector()
            gate_failed = False
            last_exit_code = 0

            cmd_str = ", ".join(file_list)

            file_bytes = b""
            for tf in file_list:
                p = project_root / tf
                if p.exists():
                    file_bytes += p.read_bytes()
                else:
                    gate_failed = True
                    last_exit_code = 1

            src_hash = hashlib.sha256(file_bytes).hexdigest()

            out_buffer = io.StringIO()
            err_buffer = io.StringIO()

            for tf in file_list:
                rel_path = project_root / tf
                if not rel_path.exists():
                    continue

                try:
                    with contextlib.redirect_stdout(out_buffer), contextlib.redirect_stderr(err_buffer):
                        exit_code = pytest.main([str(rel_path), "-q"], plugins=[collector])
                    if exit_code != 0:
                        gate_failed = True
                        last_exit_code = exit_code
                except Exception as exc:
                    gate_failed = True
                    last_exit_code = 2

            t_end = datetime.now(timezone.utc)
            dur = (t_end - t_start).total_seconds()

            tests_run = collector.passed + collector.failed
            err_count = collector.setup_errors + collector.teardown_errors
            if collector.skipped > 0 or err_count > 0:
                gate_failed = True

            captured_output = out_buffer.getvalue() + "\n" + err_buffer.getvalue()
            log_file = logs_dir / f"gate_{gate_id}.log"
            log_text = f"=== GATE {gate_id} CAPTURED PROCESS STDOUT/STDERR ===\nCommand: {cmd_str}\nExit Code: {last_exit_code}\nCollected: {tests_run + collector.skipped}\nPassed: {collector.passed}\nFailed: {collector.failed}\nSkipped: {collector.skipped}\nErrors: {err_count}\n=== RAW OUTPUT ===\n{captured_output}"
            log_file.write_text(log_text, encoding="utf-8")
            exec_hash = hashlib.sha256(log_file.read_bytes()).hexdigest()

            if tests_run == 0 or gate_failed or last_exit_code != 0:
                all_passed = False
                g_entry = {
                    "gate_id": gate_id,
                    "gate_title": title,
                    "command": cmd_str,
                    "commit_sha": commit_sha,
                    "inventory_sha256": inv_sha,
                    "run_id": run_id,
                    "exit_code": last_exit_code if last_exit_code != 0 else 1,
                    "start_timestamp_utc": t_start.isoformat(),
                    "end_timestamp_utc": t_end.isoformat(),
                    "duration_seconds": dur,
                    "tests_collected": tests_run + collector.skipped,
                    "tests_passed": collector.passed,
                    "tests_failed": collector.failed,
                    "tests_skipped": collector.skipped,
                    "errors": err_count,
                    "source_artifact_sha256": src_hash,
                    "execution_artifact_sha256": exec_hash,
                    "artifact_hash": exec_hash,
                    "status": "FAIL",
                    "tests_run": tests_run,
                    "details": f"Pytest failed (Exit code {last_exit_code}, {collector.failed} failed, {collector.skipped} skipped)"
                }
                gate_results.append(g_entry)
                (gates_dir / f"gate_{gate_id}.json").write_text(json.dumps(g_entry, indent=2), encoding="utf-8")
            else:
                g_entry = {
                    "gate_id": gate_id,
                    "gate_title": title,
                    "command": cmd_str,
                    "commit_sha": commit_sha,
                    "inventory_sha256": inv_sha,
                    "run_id": run_id,
                    "exit_code": 0,
                    "start_timestamp_utc": t_start.isoformat(),
                    "end_timestamp_utc": t_end.isoformat(),
                    "duration_seconds": dur,
                    "tests_collected": collector.passed,
                    "tests_passed": collector.passed,
                    "tests_failed": 0,
                    "tests_skipped": 0,
                    "errors": 0,
                    "source_artifact_sha256": src_hash,
                    "execution_artifact_sha256": exec_hash,
                    "artifact_hash": exec_hash,
                    "status": "PASS",
                    "tests_run": collector.passed,
                    "details": f"Pytest executed successfully ({collector.passed} tests passed)"
                }
                gate_results.append(g_entry)
                (gates_dir / f"gate_{gate_id}.json").write_text(json.dumps(g_entry, indent=2), encoding="utf-8")
            total_tests_executed += tests_run

    # Determine Verdict
    is_production_run = (not is_custom_run) and (evaluated_ids == canonical_ids)
    if all_passed and is_production_run and clean_tree:
        verdict = "PASS - PRODUCTION READY"
    elif all_passed and is_custom_run:
        verdict = "PASS - CUSTOM RUN"
    else:
        verdict = "FAIL - GATE FAILURE"

    # Determine output directories
    if output_dir:
        cert_dir = output_dir / "reports"
        docs_dir = output_dir / "docs"
    else:
        cert_dir = project_root / "reports"
        docs_dir = project_root / "docs"

    cert_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    cert_json_path = cert_dir / "release_certificate.json"
    doc_md_path = docs_dir / "RELEASE_CERTIFICATION.md"

    cert_data = {
        "release_version": "6.0.0",
        "commit_sha": commit_sha,
        "working_tree_clean": clean_tree,
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "total_gates_evaluated": len(gate_results),
        "passed_gates": sum(1 for g in gate_results if g["status"] == "PASS"),
        "failed_gates": sum(1 for g in gate_results if g["status"] == "FAIL"),
        "total_executed_tests": total_tests_executed,
        "gate_results": gate_results,
        "system_info": {
            "python_version": platform.python_version(),
            "os": platform.platform()
        }
    }

    cert_json_path.write_text(json.dumps(cert_data, indent=2), encoding="utf-8")
    doc_md_path.write_text(f"# RELEASE CERTIFICATION REPORT\nVerdict: {verdict}\nCommit: {commit_sha}\n", encoding="utf-8")

    print(f"\nRelease certificate written to {cert_json_path}")
    print(f"Final Verdict: {verdict}")

    return cert_data

if __name__ == "__main__":
    res = run_release_certification()
    if res["verdict"] != "PASS - PRODUCTION READY":
        sys.exit(1)
