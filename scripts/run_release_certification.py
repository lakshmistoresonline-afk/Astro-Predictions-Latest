"""
Canonical Release Certification System Runner for Astrovision (Version 6.0.0).
Executes REAL test suites programmatically via Pytest across all 26 Release Gates.
Outputs machine-readable JSON release certificate (reports/release_certificate.json) and markdown report (docs/RELEASE_CERTIFICATION.md).
"""
import os
import sys
import json
import hashlib
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import pytest

EXPECTED_DE440S_SHA256 = "c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2"

RELEASE_GATES = [
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
    ("G16_PREDICTIVE_TIMING", "Convergent Domain Timing Windows", "apps/api/tests/test_release_gate_g16_predictive_timing.py"),
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
            return len(res.stdout.strip()) == 0
    except Exception:
        pass
    return False

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
    output_dir: Optional[Path] = None
) -> Dict[str, Any]:
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    commit_sha = get_git_commit_sha(project_root)
    clean_tree = is_git_working_tree_clean(project_root)

    canonical_ids = [g[0] for g in RELEASE_GATES]
    gates_to_run = custom_gates if custom_gates is not None else RELEASE_GATES

    # Strict input validation on custom_gates
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

    if is_malformed:
        all_passed = False
        gate_results.append({
            "gate_id": "G_MALFORMED_GATES",
            "gate_title": "Custom Gate Definition Validation",
            "status": "FAIL",
            "tests_run": 0,
            "details": f"Validation failed: {malformed_reason}"
        })

    # Pre-flight check for production runs
    if not is_custom_run and (not clean_tree or commit_sha == "unknown_commit"):
        all_passed = False
        gate_results.append({
            "gate_id": "G00_PREFLIGHT_GIT_CLEAN",
            "gate_title": "Git Working Tree Clean Preflight Check",
            "status": "FAIL",
            "tests_run": 0,
            "details": f"Production certification requires clean working tree and valid commit SHA. (clean={clean_tree}, sha={commit_sha})"
        })

    # Handle G01_DE440S_HASH if present in gates_to_run
    if not is_malformed:
        g1_tuple = next((g for g in gates_to_run if g[0] == "G01_DE440S_HASH"), None)
        if g1_tuple:
            de440s_path = project_root / "apps" / "api" / "engines" / "astronomy" / "de440s.bsp"
            kernel_hash = ""
            if de440s_path.exists() and de440s_path.stat().st_size > 30000000:
                with open(de440s_path, "rb") as f:
                    kernel_hash = hashlib.sha256(f.read()).hexdigest()

                if kernel_hash == EXPECTED_DE440S_SHA256:
                    gate_results.append({
                        "gate_id": "G01_DE440S_HASH",
                        "gate_title": "NASA JPL DE440s Kernel SHA-256 Checksum",
                        "status": "PASS",
                        "tests_run": 1,
                        "details": f"DE440s kernel verified ({de440s_path.stat().st_size:,} bytes, SHA-256: {kernel_hash[:16]}...)"
                    })
                    total_tests_executed += 1
                else:
                    all_passed = False
                    gate_results.append({
                        "gate_id": "G01_DE440S_HASH",
                        "gate_title": "NASA JPL DE440s Kernel SHA-256 Checksum",
                        "status": "FAIL",
                        "tests_run": 1,
                        "details": f"Checksum mismatch: got {kernel_hash}, expected {EXPECTED_DE440S_SHA256}"
                    })
            else:
                all_passed = False
                gate_results.append({
                    "gate_id": "G01_DE440S_HASH",
                    "gate_title": "NASA JPL DE440s Kernel SHA-256 Checksum",
                    "status": "FAIL",
                    "tests_run": 0,
                    "details": f"DE440s kernel missing or invalid at {de440s_path}"
                })

        # Remaining Gates: Programmatic Pytest execution
        pytest_gates = [g for g in gates_to_run if g[0] != "G01_DE440S_HASH"]
        for gate_id, title, test_files in pytest_gates:
            file_list = test_files if isinstance(test_files, list) else [test_files]
            collector = PytestPluginCollector()
            gate_failed = False
            last_exit_code = 0

            for tf in file_list:
                rel_path = project_root / tf
                if not rel_path.exists():
                    gate_failed = True
                    last_exit_code = 1
                    continue

                try:
                    exit_code = pytest.main([str(rel_path), "-q"], plugins=[collector])
                    if exit_code != 0:
                        gate_failed = True
                        last_exit_code = exit_code
                except Exception as exc:
                    gate_failed = True
                    last_exit_code = 2

            tests_run = collector.passed + collector.failed
            if collector.skipped > 0 or collector.setup_errors > 0 or collector.teardown_errors > 0:
                gate_failed = True

            if tests_run == 0 or gate_failed:
                all_passed = False
                gate_results.append({
                    "gate_id": gate_id,
                    "gate_title": title,
                    "status": "FAIL",
                    "tests_run": tests_run,
                    "details": f"Pytest failed (Exit code {last_exit_code}, {collector.failed} failed, {collector.skipped} skipped)"
                })
            else:
                gate_results.append({
                    "gate_id": gate_id,
                    "gate_title": title,
                    "status": "PASS",
                    "tests_run": tests_run,
                    "details": f"Pytest executed successfully ({collector.passed} tests passed)"
                })
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

    cert_data = {
        "release_version": "6.0.0",
        "commit_sha": commit_sha,
        "working_tree_clean": clean_tree,
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

    with open(cert_json_path, "w", encoding="utf-8") as f:
        json.dump(cert_data, f, indent=2)

    report_md_path = docs_dir / "RELEASE_CERTIFICATION.md"
    report_copy_path = cert_dir / "release_certification_report.md"

    md_lines = [
        "# Astrovision Version 6.0.0 Release Certification Report\n",
        f"- **Commit SHA**: `{commit_sha}`",
        f"- **Working Tree Clean**: `{clean_tree}`",
        f"- **Timestamp**: `{cert_data['timestamp_utc']}`",
        f"- **Overall Certification Verdict**: **{cert_data['verdict']}**",
        f"- **Total Executed Tests**: `{total_tests_executed}`",
        f"- **Total Gates Evaluated**: `{len(gate_results)}`",
        f"- **Passed Gates**: `{cert_data['passed_gates']}`",
        f"- **Failed Gates**: `{cert_data['failed_gates']}`\n",
        "## Release Certification Gate Summary Table\n",
        "| Gate ID | Release Gate Title | Status | Tests | Details |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    for g in gate_results:
        status_str = f"**{g['status']}**"
        md_lines.append(f"| `{g['gate_id']}` | {g['gate_title']} | {status_str} | {g['tests_run']} | {g['details']} |")

    md_text = "\n".join(md_lines) + "\n"

    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    with open(report_copy_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    print(f"\nJSON Release Certificate saved to {cert_json_path}")
    print(f"Markdown Certification Report saved to {report_md_path} and {report_copy_path}")
    print(f"Verdict: {cert_data['verdict']}")
    print("================================================================================")

    return cert_data

if __name__ == "__main__":
    res = run_release_certification()
    if res["verdict"] != "PASS - PRODUCTION READY":
        sys.exit(1)
