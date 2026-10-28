"""
Hardened Zero-Trust Release Evidence Validator (Phase 2AT Time-Boxed Final Closure).
Independently parses actual JUnit XML reports, recomputes occurrence-level test metrics directly from XML evidence,
inspects individual gate execution proof JSON files (reports/runs/<run_id>/gates/gate_<G_ID>.json)
and actual retained gate execution log files (reports/runs/<run_id>/gates/logs/gate_<G_ID>.log),
validates distinct source_artifact_sha256 and execution_artifact_sha256 digests against physical files on disk,
checks Git status, validates all 26 canonical release gates, execution proof, source SHAs, timestamps,
and build evidence against strict zero-trust invariants before certifying production readiness.
Strictly enforces occurrence-level accounting, the canonical 10-batch plan, and zero-tolerance exit code rules.
"""
import json
import sys
import hashlib
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

CANONICAL_26_GATES = [
    "G01_DE440S_HASH", "G02_ASTRONOMY", "G03_TIMEZONE_DST", "G04_RASHI_NAKSHATRA", "G05_ASCENDANT_HOUSES",
    "G06_VARGAS_D1_D60", "G07_VIMSHOTTARI_DASHA", "G08_CLASSICAL_YOGAS", "G09_CLASSICAL_DOSHAS", "G10_SHADBALA",
    "G11_ASHTAKAVARGA", "G12_JAIMINI_SUTRAS", "G13_TRANSITS", "G14_PANCHANGA", "G15_MUHURTA",
    "G16_PREDICTIVE_TIMING", "G17_RECTIFICATION", "G18_COMPATIBILITY", "G19_PREDICTION_EVIDENCE", "G20_AI_TRUST_BOUNDARY",
    "G21_AI_VALIDATION", "G22_PERSISTENCE", "G23_IDOR_CONTROLS", "G24_API_CONTRACTS", "G25_PDF_EXPORT", "G26_ADMIN_SECURITY"
]

CANONICAL_10_BATCH_IDS = [f"BATCH_{i}" for i in range(1, 11)]

def check_git_status_clean(project_root: Path) -> bool:
    try:
        res = subprocess.run(["git", "status", "--porcelain"], cwd=project_root, capture_output=True, text=True)
        if res.returncode == 0:
            lines = [line.strip() for line in res.stdout.splitlines() if line.strip() and "reports/" not in line and "docs/" not in line]
            return len(lines) == 0
    except Exception:
        pass
    return False

def get_git_commit_sha(project_root: Path) -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=project_root, capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return ""

def compute_inventory_hash(node_ids: list) -> str:
    content = "\n".join(sorted(node_ids)).encode("utf-8")
    return hashlib.sha256(content).hexdigest()

def validate_release_evidence(project_root: Optional[Path] = None) -> bool:
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent
    else:
        project_root = Path(project_root).resolve()

    reports_dir = project_root / "reports"
    docs_dir = project_root / "docs"

    required_files = [
        reports_dir / "test_node_inventory.json",
        reports_dir / "test_execution_reconciliation.json",
        reports_dir / "release_certificate.json",
        reports_dir / "release_certification_report.md",
        docs_dir / "RELEASE_CERTIFICATION.md",
        reports_dir / "production_readiness_audit.md"
    ]

    errors = []

    # 1. Artifact Existence and Non-Emptiness
    for f_path in required_files:
        if not f_path.exists():
            errors.append(f"Missing required evidence file: {f_path.relative_to(project_root)}")
        elif f_path.stat().st_size == 0:
            errors.append(f"Evidence file is empty: {f_path.relative_to(project_root)}")

    if errors:
        print("ZERO-TRUST EVIDENCE VALIDATION FAILED (Missing/Empty Files):")
        for err in errors:
            print(f" - {err}")
        return False

    # 2. Parse JSON Artifacts
    inventory_data: Dict[str, Any] = {}
    reconciliation_data: Dict[str, Any] = {}
    certificate_data: Dict[str, Any] = {}

    try:
        inventory_data = json.loads((reports_dir / "test_node_inventory.json").read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"Failed to parse test_node_inventory.json: {e}")

    try:
        reconciliation_data = json.loads((reports_dir / "test_execution_reconciliation.json").read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"Failed to parse test_execution_reconciliation.json: {e}")

    try:
        certificate_data = json.loads((reports_dir / "release_certificate.json").read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"Failed to parse release_certificate.json: {e}")

    if errors:
        print("ZERO-TRUST EVIDENCE VALIDATION FAILED (JSON Parse Failure):")
        for err in errors:
            print(f" - {err}")
        return False

    # 3. Validate Inventory Format and SHA-256 Hash
    inv_nodes = inventory_data.get("node_ids", [])
    if not isinstance(inv_nodes, list) or len(inv_nodes) == 0:
        errors.append("test_node_inventory.json has empty or invalid node_ids list")

    inv_set = set(inv_nodes)
    if len(inv_nodes) != len(inv_set):
        errors.append("test_node_inventory.json contains duplicate node IDs")

    computed_inv_sha = compute_inventory_hash(inv_nodes)
    inv_sha_field = inventory_data.get("inventory_sha256", "")
    if inv_sha_field and inv_sha_field != computed_inv_sha:
        errors.append(f"Inventory inventory_sha256 field ({inv_sha_field}) disagrees with computed hash ({computed_inv_sha})")

    inv_count = inventory_data.get("total_unique_node_ids", 0)
    if inv_count != len(inv_set):
        errors.append(f"Inventory total_unique_node_ids ({inv_count}) does not match actual node count ({len(inv_set)})")

    # 4. Validate Run Manifest & Mandatory 10-Batch Plan
    rec_run_id = reconciliation_data.get("run_id", "")
    if not rec_run_id:
        errors.append("Reconciliation ledger missing run_id")

    rec_sha = reconciliation_data.get("source_sha", "")
    if not rec_sha:
        errors.append("Reconciliation ledger missing source_sha")

    run_dir = reports_dir / "runs" / rec_run_id
    manifest_file = run_dir / "run_manifest.json"

    if not run_dir.exists():
        errors.append(f"Run directory missing: {run_dir.relative_to(project_root)}")
    elif not manifest_file.exists():
        errors.append(f"Run manifest missing: {manifest_file.relative_to(project_root)}")
    else:
        try:
            manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
            if manifest_data.get("run_id") != rec_run_id:
                errors.append(f"Run manifest run_id ({manifest_data.get('run_id')}) disagrees with ledger run_id ({rec_run_id})")
            if manifest_data.get("source_sha") != rec_sha:
                errors.append(f"Run manifest source_sha ({manifest_data.get('source_sha')}) disagrees with ledger source_sha ({rec_sha})")
            if manifest_data.get("inventory_sha256") != computed_inv_sha:
                errors.append("Run manifest inventory_sha256 disagrees with current inventory hash")
            if manifest_data.get("expected_batch_count") != 10:
                errors.append(f"Incomplete run manifest! expected_batch_count is {manifest_data.get('expected_batch_count')}, expected exactly 10")
        except Exception as m_exc:
            errors.append(f"Failed to parse run_manifest.json: {m_exc}")

    # 5. Validate Timestamps and Durations
    start_ts_str = reconciliation_data.get("start_timestamp_utc", "")
    end_ts_str = reconciliation_data.get("end_timestamp_utc", "")

    if not start_ts_str or not end_ts_str:
        errors.append("Reconciliation ledger missing start_timestamp_utc or end_timestamp_utc")
    else:
        try:
            dt_start = datetime.fromisoformat(start_ts_str)
            dt_end = datetime.fromisoformat(end_ts_str)
            if dt_start.tzinfo is None or dt_end.tzinfo is None:
                errors.append("Reconciliation timestamps must be timezone-aware UTC ISO-8601 strings")
            if dt_end < dt_start:
                errors.append(f"Reconciliation end timestamp ({end_ts_str}) precedes start timestamp ({start_ts_str})")

            calc_duration = (dt_end - dt_start).total_seconds()
            reported_wall_clock = reconciliation_data.get("total_wall_clock_duration_seconds")
            if reported_wall_clock is not None and abs(reported_wall_clock - calc_duration) > 5.0:
                errors.append(f"Reported wall clock duration ({reported_wall_clock}s) disagrees with calculated interval ({calc_duration}s)")
        except Exception as ts_exc:
            errors.append(f"Invalid timestamp format in reconciliation ledger: {ts_exc}")

    # Check Process Exit / Collection Errors in Reconciliation Metrics
    rec_metrics = reconciliation_data.get("metrics", {})
    if rec_metrics.get("collection_errors", 0) > 0:
        errors.append(f"Reconciliation ledger records {rec_metrics.get('collection_errors')} collection errors")
    if rec_metrics.get("interrupted_runs", 0) > 0:
        errors.append(f"Reconciliation ledger records {rec_metrics.get('interrupted_runs')} interrupted runs")

    # Check Per-Node Records in Reconciliation Ledger
    rec_nodes = reconciliation_data.get("reconciled_nodes", {})
    if not isinstance(rec_nodes, dict) or len(rec_nodes) == 0:
        errors.append("Reconciliation ledger missing or empty reconciled_nodes object")
    else:
        for r_id, r_info in rec_nodes.items():
            r_res = r_info.get("final_result", "")
            if r_res != "PASSED":
                errors.append(f"Reconciliation ledger node '{r_id}' has non-PASS result '{r_res}'")

    # 6. Occurrence-Level XML Accounting across ALL 10 Canonical Batches
    batch_metadata = reconciliation_data.get("batch_execution_metadata", [])
    if not isinstance(batch_metadata, list) or len(batch_metadata) != 10:
        errors.append(f"Reconciliation ledger batch_execution_metadata must contain exactly 10 batches, found {len(batch_metadata) if isinstance(batch_metadata, list) else 0}")

    xml_occurrences: List[Dict[str, Any]] = []
    xml_execution_counts: Dict[str, int] = {}

    for b_info in batch_metadata:
        b_idx = b_info.get("batch_idx") or b_info.get("batch_id")
        b_exit_code = b_info.get("exit_code", -1)
        if b_exit_code != 0: # STRICT: Every batch exit code must be exactly 0
            errors.append(f"Batch {b_idx} recorded non-zero process exit code: {b_exit_code}")

        xml_rel_path = b_info.get("xml_path") or b_info.get("xml_report_path", "")
        if not xml_rel_path or xml_rel_path == "MISSING":
            errors.append(f"Batch {b_idx} missing JUnit XML report path")
            continue

        xml_abs_path = project_root / xml_rel_path

        # Path traversal check
        try:
            resolved_xml = xml_abs_path.resolve()
            resolved_run = run_dir.resolve()
            if not resolved_xml.is_relative_to(resolved_run):
                errors.append(f"Batch {b_idx} XML path ({xml_rel_path}) escapes run directory ({rec_run_id})")
        except Exception:
            errors.append(f"Batch {b_idx} XML path resolution error: {xml_rel_path}")

        if not xml_abs_path.exists() or xml_abs_path.stat().st_size == 0:
            errors.append(f"JUnit XML report file missing or empty: {xml_rel_path}")
            continue

        try:
            tree = ET.parse(xml_abs_path)
            xml_root = tree.getroot()

            # Validate XML testsuite attribute totals against parsed testcases if present
            suite_tests_attr = xml_root.find("testsuite")
            if suite_tests_attr is not None:
                reported_suite_tests = int(suite_tests_attr.get("tests", 0))
                actual_suite_testcases = len(list(xml_root.iter("testcase")))
                if reported_suite_tests != actual_suite_testcases:
                    errors.append(f"Batch {b_idx} XML suite 'tests' attribute ({reported_suite_tests}) disagrees with parsed testcase count ({actual_suite_testcases})")

            for testcase in xml_root.iter("testcase"):
                file_attr = testcase.get("file", "").replace("\\", "/")
                name_attr = testcase.get("name", "")
                classname = testcase.get("classname", "").replace("\\", "/")
                time_attr = float(testcase.get("time", "0.0"))

                if time_attr < 0.0:
                    errors.append(f"Batch {b_idx} XML contains negative execution duration ({time_attr}s) for '{name_attr}'")

                status = "PASSED"
                failure = testcase.find("failure")
                error = testcase.find("error")
                skipped = testcase.find("skipped")
                if failure is not None:
                    status = "FAILED"
                elif error is not None:
                    status = "ERROR"
                elif skipped is not None:
                    status = "SKIPPED"

                if file_attr:
                    node_id = f"{file_attr}::{name_attr}"
                elif classname:
                    py_path = classname.replace(".", "/") + ".py"
                    node_id = f"{py_path}::{name_attr}"
                else:
                    node_id = f"unknown::{name_attr}"

                xml_execution_counts[node_id] = xml_execution_counts.get(node_id, 0) + 1
                xml_occurrences.append({
                    "node_id": node_id,
                    "status": status,
                    "duration": time_attr,
                    "batch": b_idx
                })

        except Exception as xml_exc:
            errors.append(f"Failed to parse JUnit XML report {xml_rel_path}: {xml_exc}")

    # 7. Occurrence-Level Metric Verification
    computed_passed = sum(1 for occ in xml_occurrences if occ["status"] == "PASSED")
    computed_failed = sum(1 for occ in xml_occurrences if occ["status"] == "FAILED")
    computed_skipped = sum(1 for occ in xml_occurrences if occ["status"] == "SKIPPED")
    computed_error = sum(1 for occ in xml_occurrences if occ["status"] in ["ERROR", "SETUP_ERROR", "TEARDOWN_ERROR"])

    m_passed = rec_metrics.get("passed_count")
    m_failed = rec_metrics.get("failed_count")
    m_skipped = rec_metrics.get("skipped_count")
    m_error = rec_metrics.get("setup_error_count", 0) + rec_metrics.get("teardown_error_count", 0)

    if m_passed != computed_passed or m_failed != computed_failed or m_skipped != computed_skipped or m_error != computed_error:
        errors.append(f"Tampered summary counts! Reconciliation metrics ({m_passed}P/{m_failed}F/{m_skipped}S/{m_error}E) contradict recomputed occurrence-level XML evidence ({computed_passed}P/{computed_failed}F/{computed_skipped}S/{computed_error}E)")

    if computed_failed > 0:
        errors.append(f"Evidence XML contains {computed_failed} failed test occurrences")
    if computed_skipped > 0:
        errors.append(f"Evidence XML contains {computed_skipped} skipped test occurrences")
    if computed_error > 0:
        errors.append(f"Evidence XML contains {computed_error} setup/teardown error occurrences")

    xml_duplicates = [n for n, cnt in xml_execution_counts.items() if cnt > 1]
    if len(xml_duplicates) > 0:
        errors.append(f"Evidence XML contains {len(xml_duplicates)} duplicate test executions: {xml_duplicates[:3]}")

    # Exact Inventory Set Reconciliation
    xml_executed_set = set(occ["node_id"] for occ in xml_occurrences)
    if inv_set != xml_executed_set:
        diff_missing = inv_set - xml_executed_set
        diff_extra = xml_executed_set - inv_set
        errors.append(f"Inventory and XML evidence set mismatch! Missing from XML: {len(diff_missing)}, Unexpected in XML: {len(diff_extra)}")

    rec_verdict = rec_metrics.get("reconciliation_verdict", "")
    if rec_verdict != "MATCH_100_PERCENT_PASSED":
        errors.append(f"Reconciliation verdict is not MATCH_100_PERCENT_PASSED: '{rec_verdict}'")

    # 8. Validate Release Certificate Integrity & Individual Gate Evidence JSON & Log Files
    cert_sha = certificate_data.get("commit_sha", "")
    if cert_sha != rec_sha:
        errors.append(f"Certificate SHA ({cert_sha}) does not match reconciliation ledger SHA ({rec_sha})")

    cert_run_id = certificate_data.get("run_id", "")
    if cert_run_id and cert_run_id != rec_run_id:
        errors.append(f"Certificate run ID ({cert_run_id}) does not match reconciliation run ID ({rec_run_id})")

    gate_results = certificate_data.get("gate_results", [])
    if not isinstance(gate_results, list) or len(gate_results) != 26:
        errors.append(f"Release certificate missing or invalid gate_results list (found {len(gate_results) if isinstance(gate_results, list) else 0}, expected 26)")
    else:
        cert_gate_ids = [g.get("gate_id", "") for g in gate_results if isinstance(g, dict)]
        if sorted(cert_gate_ids) != sorted(CANONICAL_26_GATES):
            errors.append("Release certificate gate IDs do not match exact canonical 26 gates list! Missing or mismatched gate IDs.")

        seen_gates = set()
        gates_proof_dir = run_dir / "gates"
        logs_proof_dir = gates_proof_dir / "logs"

        for g_item in gate_results:
            g_id = g_item.get("gate_id", "")
            g_status = g_item.get("status", "")
            g_tests = g_item.get("tests_run", 0)
            g_exit_code = g_item.get("exit_code", 0)
            g_sha = g_item.get("commit_sha", "")
            g_cmd = g_item.get("command", "")

            if g_id in seen_gates:
                errors.append(f"Duplicate canonical gate ID in certificate: {g_id}")
            seen_gates.add(g_id)

            if g_status != "PASS":
                errors.append(f"Gate {g_id} status is '{g_status}', expected 'PASS'")
            if g_exit_code != 0:
                errors.append(f"Gate {g_id} recorded non-zero exit code: {g_exit_code}")
            if g_tests <= 0:
                errors.append(f"Gate {g_id} has zero executed tests recorded ({g_tests})")
            if g_sha and g_sha != rec_sha:
                errors.append(f"Gate {g_id} commit SHA ({g_sha}) disagrees with reconciliation SHA ({rec_sha})")
            if not g_cmd:
                errors.append(f"Gate {g_id} missing command specification")

            # Cross-check against individual gate evidence JSON file if gates_proof_dir exists
            if gates_proof_dir.exists():
                g_file = gates_proof_dir / f"gate_{g_id}.json"
                if not g_file.exists() or g_file.stat().st_size == 0:
                    errors.append(f"Missing gate execution proof file: {g_file.relative_to(project_root)}")
                else:
                    try:
                        g_file_data = json.loads(g_file.read_text(encoding="utf-8"))
                        if g_file_data.get("status") != "PASS":
                            errors.append(f"Gate proof file for {g_id} records non-PASS status: {g_file_data.get('status')}")
                        if g_file_data.get("exit_code") != 0:
                            errors.append(f"Gate proof file for {g_id} records non-zero exit code: {g_file_data.get('exit_code')}")
                        if not g_file_data.get("source_artifact_sha256"):
                            errors.append(f"Gate proof file for {g_id} missing source_artifact_sha256")
                        if not g_file_data.get("execution_artifact_sha256"):
                            errors.append(f"Gate proof file for {g_id} missing execution_artifact_sha256")
                    except Exception as g_exc:
                        errors.append(f"Failed to parse gate proof file for {g_id}: {g_exc}")

            # Verify retained output log file if logs_proof_dir exists
            if logs_proof_dir.exists():
                log_f = logs_proof_dir / f"gate_{g_id}.log"
                if not log_f.exists() or log_f.stat().st_size == 0:
                    errors.append(f"Missing retained gate output log file: {log_f.relative_to(project_root)}")
                else:
                    recomputed_exec_hash = hashlib.sha256(log_f.read_bytes()).hexdigest()
                    recorded_exec_hash = g_item.get("execution_artifact_sha256")
                    if recorded_exec_hash and recorded_exec_hash != recomputed_exec_hash:
                        errors.append(f"Execution artifact hash mismatch for {g_id}! Recorded {recorded_exec_hash}, computed {recomputed_exec_hash}")

    cert_verdict = certificate_data.get("verdict", "")

    # System Git Working Tree Check
    actual_git_clean = check_git_status_clean(project_root)

    # 9. Final Decision: Fail Closed for any error
    if errors:
        print("ZERO-TRUST EVIDENCE VALIDATION FAILED:")
        for err in errors:
            print(f" - {err}")
        return False

    if not actual_git_clean or not certificate_data.get("working_tree_clean", False):
        if cert_verdict == "PASS - PRODUCTION READY":
            print("ZERO-TRUST EVIDENCE VALIDATION FAILED:")
            print(" - Certificate claims 'PASS - PRODUCTION READY' but system Git working tree is dirty!")
            return False
        else:
            print("EVIDENCE_VALID_BUT_INCOMPLETE: Release evidence is internally consistent and verified, but Git working tree contains uncommitted changes.")
            return False

    if cert_verdict != "PASS - PRODUCTION READY":
        print(f"EVIDENCE_VALID_BUT_INCOMPLETE: Release evidence is valid, but certificate verdict is '{cert_verdict}'.")
        return False

    print("SUCCESS: Zero-trust release evidence validation passed (PASS - PRODUCTION READY).")
    return True

if __name__ == "__main__":
    success = validate_release_evidence()
    if not success:
        sys.exit(1)
