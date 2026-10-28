"""
Truthful Programmatic Execution Reconciliation Ledger Generator (reports/test_execution_reconciliation.json).
Orchestrates fresh execution of repository test batches into a run-isolated evidence directory (reports/runs/<run_id>/),
writes a pre-execution Run Manifest (run_manifest.json), captures per-batch metadata and JUnit XML reports,
and performs exact mathematical set reconciliation against test_node_inventory.json.
Supports modular batch execution to prevent runner timeout while maintaining strict run isolation.
"""
import json
import subprocess
import sys
import argparse
import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

def get_git_commit_sha(root: Path) -> str:
    res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Git rev-parse HEAD failed with exit code {res.returncode}: {res.stderr}")
    sha = res.stdout.strip()
    if not sha or len(sha) != 40:
        raise RuntimeError(f"Invalid Git commit SHA retrieved: '{sha}'")
    return sha

def is_working_tree_clean(root: Path) -> bool:
    res = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Git status check failed with exit code {res.returncode}: {res.stderr}")
    return len(res.stdout.strip()) == 0

def compute_inventory_hash(node_ids: list) -> str:
    content = "\n".join(sorted(node_ids)).encode("utf-8")
    return hashlib.sha256(content).hexdigest()

TEST_BATCHES = [
    ("Batch 1 (Oracles)", ["apps/api/tests/oracles/"]),
    ("Batch 2 (Core Astronomy & PDF)", ["apps/api/tests/test_astronomy_provider.py", "apps/api/tests/test_planetary_schema_integrity.py", "apps/api/tests/test_vedic_foundation.py", "apps/api/tests/test_pdf_report_engine.py", "apps/api/tests/test_golden_reference_report.py", "apps/api/tests/test_gold_standard_export.py"]),
    ("Batch 3 (Security & Persistence)", ["apps/api/tests/test_auth_security.py", "apps/api/tests/test_authorization_matrix.py", "apps/api/tests/test_persistence_idor.py", "apps/api/tests/test_persistence_lifecycle.py", "apps/api/tests/test_admin_security.py"]),
    ("Batch 4 (Engines)", ["apps/api/tests/test_dasha_engine.py", "apps/api/tests/test_yoga_engine.py", "apps/api/tests/test_dosha_engine.py", "apps/api/tests/test_varga_engine.py"]),
    ("Batch 5 (AI, Validation & Red Team)", ["apps/api/tests/test_ai_service.py", "apps/api/tests/test_ai_validation_pipeline.py", "apps/api/tests/test_compatibility_engine.py", "apps/api/tests/test_date_validation_strict.py", "apps/api/tests/test_geocoding_timezone.py", "apps/api/tests/test_health_readiness.py", "apps/api/tests/test_jwt_security_hardening.py", "apps/api/tests/test_personalization.py", "apps/api/tests/test_prediction_evidence.py", "apps/api/tests/test_quota_governance.py", "apps/api/tests/test_rate_limiter.py", "apps/api/tests/test_red_team_audit.py", "apps/api/tests/test_reference_chart.py", "apps/api/tests/test_sav_reconciliation.py", "apps/api/tests/test_secret_management.py", "apps/api/tests/test_security_ownership.py", "apps/api/tests/test_structured_error_handling.py", "apps/api/tests/test_svg_xss_security.py", "apps/api/tests/test_timezone_historical.py", "apps/api/tests/test_treatise_builder.py", "apps/api/tests/test_api_abuse_protection.py", "apps/api/tests/test_api_contract.py", "apps/api/tests/test_audit_logging.py", "apps/api/tests/test_auth_constant_time.py", "apps/api/tests/test_database_migrations.py", "apps/api/tests/test_fixture_adapter.py", "apps/api/tests/test_timestamp_integrity.py", "apps/api/tests/test_evidence_validator.py"]),
    ("Batch 6 (Full User Journey)", ["apps/api/tests/test_full_user_journey.py"]),
    ("Batch 7 (Scripts Integrity)", ["scripts/test_r7_r3_frozen_reference_integrity.py"]),
    ("Batch 8 (Ephemeris & Oracle Benchmark)", ["apps/api/tests/ephemeris_benchmark/test_ephemeris_accuracy.py", "apps/api/tests/test_engines.py", "apps/api/tests/test_yoga_independent_oracle.py"]),
    ("Batch 9 (Release Gates Jaimini, Transits, Panchanga, Muhurta, Predictive Timing)", ["apps/api/tests/test_release_gate_g12_jaimini.py", "apps/api/tests/test_release_gate_g13_transits.py", "apps/api/tests/test_release_gate_g14_panchanga.py", "apps/api/tests/test_release_gate_g15_muhurta.py", "apps/api/tests/test_release_gate_g16_predictive_timing.py"]),
    ("Batch 10 (Runner Self Tests)", ["apps/api/tests/test_release_certification_runner.py"])
]

def generate_reconciliation_ledger(start_batch: int = 1, end_batch: int = 10, run_id_override: str = None, root: Path = None):
    if root is None:
        root = Path(__file__).resolve().parent.parent
    else:
        root = Path(root).resolve()

    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    source_sha = get_git_commit_sha(root)
    clean_tree = is_working_tree_clean(root)

    # Load inventory
    inventory_path = reports_dir / "test_node_inventory.json"
    if not inventory_path.exists():
        raise RuntimeError("test_node_inventory.json missing. Must generate inventory first.")

    with open(inventory_path, "r", encoding="utf-8") as f:
        inv_data = json.load(f)

    inv_nodes = inv_data.get("node_ids", [])
    inv_sha = inv_data.get("inventory_sha256", compute_inventory_hash(inv_nodes))
    inventory_set = set(inv_nodes)

    overall_start_utc = datetime.now(timezone.utc)

    if run_id_override:
        run_id = run_id_override
    else:
        run_id = f"RUN_{overall_start_utc.strftime('%Y%m%d_%H%M%S')}_{source_sha[:8]}"

    run_dir = reports_dir / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = run_dir / "run_manifest.json"
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
            if manifest_data.get("source_sha") != source_sha:
                raise RuntimeError(f"Run resumption failed: Run SHA ({manifest_data.get('source_sha')}) differs from current SHA ({source_sha})")
            if manifest_data.get("inventory_sha256") != inv_sha:
                raise RuntimeError("Run resumption failed: Inventory SHA-256 mismatch")
    else:
        manifest_data = {
            "run_id": run_id,
            "source_sha": source_sha,
            "working_tree_clean": clean_tree,
            "inventory_sha256": inv_sha,
            "total_inventory_unique_nodes": len(inv_nodes),
            "expected_batch_count": len(TEST_BATCHES),
            "expected_batches": [b[0] for b in TEST_BATCHES],
            "start_timestamp_utc": overall_start_utc.isoformat()
        }
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)

    selected_batches = TEST_BATCHES[start_batch - 1 : end_batch]

    print(f"Executing Run '{run_id}' for Batches {start_batch} through {end_batch} (SHA: {source_sha}, Clean: {clean_tree})...")
    sys.stdout.flush()

    for offset, (batch_name, targets) in enumerate(selected_batches):
        batch_idx = start_batch + offset
        batch_start_utc = datetime.now(timezone.utc)
        xml_path = run_dir / f"pytest_batch_{batch_idx}.xml"
        meta_path = run_dir / f"pytest_batch_{batch_idx}_meta.json"

        cmd = [sys.executable, "-m", "pytest", f"--junitxml={xml_path}", "-q"] + targets
        res = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        exit_code = res.returncode
        batch_end_utc = datetime.now(timezone.utc)
        batch_duration = (batch_end_utc - batch_start_utc).total_seconds()

        print(f"[{batch_idx}/{len(TEST_BATCHES)}] Finished {batch_name} in {batch_duration:.2f}s (Exit Code: {exit_code})")
        sys.stdout.flush()

        b_meta = {
            "run_id": run_id,
            "batch_idx": batch_idx,
            "batch_id": f"BATCH_{batch_idx}",
            "batch_name": batch_name,
            "targets": targets,
            "cmd": cmd,
            "exit_code": exit_code,
            "source_sha": source_sha,
            "inventory_sha256": inv_sha,
            "working_tree_clean": clean_tree,
            "start_timestamp_utc": batch_start_utc.isoformat(),
            "end_timestamp_utc": batch_end_utc.isoformat(),
            "duration_seconds": batch_duration,
            "xml_report_path": str(xml_path.relative_to(root))
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(b_meta, f, indent=2)

    # Parse and reconcile ALL expected 10 batches for this run_id
    executed_nodes_raw = {}
    execution_counts = {}
    batch_metadata = []
    xml_parsing_errors = []

    earliest_start = None
    latest_end = None

    for b_idx in range(1, len(TEST_BATCHES) + 1):
        b_name = TEST_BATCHES[b_idx - 1][0]
        xml_file = run_dir / f"pytest_batch_{b_idx}.xml"
        meta_file = run_dir / f"pytest_batch_{b_idx}_meta.json"

        b_exit_code = -1
        b_start_str = ""
        b_end_str = ""

        if meta_file.exists():
            try:
                m_data = json.loads(meta_file.read_text(encoding="utf-8"))
                b_exit_code = m_data.get("exit_code", -1)
                b_start_str = m_data.get("start_timestamp_utc", "")
                b_end_str = m_data.get("end_timestamp_utc", "")

                if b_start_str:
                    dt_s = datetime.fromisoformat(b_start_str)
                    if earliest_start is None or dt_s < earliest_start:
                        earliest_start = dt_s
                if b_end_str:
                    dt_e = datetime.fromisoformat(b_end_str)
                    if latest_end is None or dt_e > latest_end:
                        latest_end = dt_e
            except Exception:
                pass

        coll_err = 1 if b_exit_code not in [0, 1] else 0
        interrupted = 1 if b_exit_code > 5 else 0

        b_entry = {
            "batch_idx": b_idx,
            "batch_id": f"BATCH_{b_idx}",
            "batch_name": b_name,
            "exit_code": b_exit_code,
            "collection_error": coll_err,
            "interrupted": interrupted,
            "start_timestamp_utc": b_start_str,
            "end_timestamp_utc": b_end_str,
            "xml_path": str(xml_file.relative_to(root)) if xml_file.exists() else "MISSING"
        }
        batch_metadata.append(b_entry)

        if not xml_file.exists() or xml_file.stat().st_size == 0:
            b_entry["xml_parsing_error"] = "JUnit XML report file missing or empty"
            xml_parsing_errors.append(f"Batch {b_idx} XML missing/empty")
            continue

        try:
            tree = ET.parse(xml_file)
            xml_root = tree.getroot()
            for testcase in xml_root.iter("testcase"):
                file_attr = testcase.get("file", "").replace("\\", "/")
                name_attr = testcase.get("name", "")
                classname = testcase.get("classname", "").replace("\\", "/")
                time_attr = float(testcase.get("time", "0.0"))

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

                execution_counts[node_id] = execution_counts.get(node_id, 0) + 1

                if node_id not in executed_nodes_raw:
                    executed_nodes_raw[node_id] = {
                        "file": file_attr or node_id.split("::")[0],
                        "name": name_attr,
                        "status": status,
                        "batch_or_run_id": b_name,
                        "source_sha": source_sha,
                        "duration_seconds": time_attr,
                        "execution_occurrences": 1
                    }
                else:
                    executed_nodes_raw[node_id]["execution_occurrences"] += 1
                    if status != "PASSED":
                        executed_nodes_raw[node_id]["status"] = status
        except Exception as xml_exc:
            b_entry["xml_parsing_error"] = str(xml_exc)
            xml_parsing_errors.append(f"Batch {b_idx} XML parse error: {xml_exc}")

    executed_set = set(executed_nodes_raw.keys())

    duplicate_ids = [node for node, count in execution_counts.items() if count > 1]
    never_executed = sorted(list(inventory_set - executed_set))
    unexpected_ids = sorted(list(executed_set - inventory_set))

    all_known_nodes = sorted(list(inventory_set | executed_set))
    reconciled_nodes = {}

    passed_count = 0
    failed_count = 0
    skipped_count = 0
    setup_error_count = 0
    teardown_error_count = 0
    not_executed_count = 0
    collection_error_count = sum(b["collection_error"] for b in batch_metadata)
    interrupted_run_count = sum(b["interrupted"] for b in batch_metadata)

    for node_id in all_known_nodes:
        in_inventory = node_id in inventory_set
        was_executed = node_id in executed_set
        exec_info = executed_nodes_raw.get(node_id, {})

        status = exec_info.get("status", "NOT_EXECUTED")
        if not was_executed:
            status = "NOT_EXECUTED"
            not_executed_count += 1
        else:
            if status == "PASSED":
                passed_count += 1
            elif status == "FAILED":
                failed_count += 1
            elif status == "SKIPPED":
                skipped_count += 1
            elif status == "ERROR":
                setup_error_count += 1

        reconciled_nodes[node_id] = {
            "exact_pytest_node_id": node_id,
            "test_source_file": exec_info.get("file", node_id.split("::")[0] if "::" in node_id else ""),
            "inventory_membership": in_inventory,
            "executed": was_executed,
            "execution_batch_or_run_id": exec_info.get("batch_or_run_id", "N/A"),
            "source_sha": exec_info.get("source_sha", source_sha),
            "final_result": status,
            "execution_duration_seconds": exec_info.get("duration_seconds", 0.0),
            "occurrences": exec_info.get("execution_occurrences", 0)
        }

    total_discovered = len(inventory_set)
    total_executed = len(executed_set & inventory_set)

    run_start_final = earliest_start.isoformat() if earliest_start else overall_start_utc.isoformat()
    run_end_final = latest_end.isoformat() if latest_end else datetime.now(timezone.utc).isoformat()
    wall_clock_sec = (datetime.fromisoformat(run_end_final) - datetime.fromisoformat(run_start_final)).total_seconds()

    # Check if ALL 10 canonical batches were completed
    all_batches_complete = len(batch_metadata) == 10 and all(b.get("exit_code") in [0, 1] for b in batch_metadata) and len(xml_parsing_errors) == 0

    is_perfect_match = (
        all_batches_complete and
        total_executed == total_discovered and
        total_discovered > 0 and
        failed_count == 0 and
        skipped_count == 0 and
        setup_error_count == 0 and
        teardown_error_count == 0 and
        len(duplicate_ids) == 0 and
        len(never_executed) == 0 and
        len(unexpected_ids) == 0 and
        collection_error_count == 0 and
        interrupted_run_count == 0
    )

    reconciliation_data = {
        "repository": "Astrovision",
        "run_id": run_id,
        "source_sha": source_sha,
        "working_tree_clean": clean_tree,
        "inventory_sha256": inv_sha,
        "start_timestamp_utc": run_start_final,
        "end_timestamp_utc": run_end_final,
        "total_wall_clock_duration_seconds": wall_clock_sec,
        "metrics": {
            "total_discovered_unique_inventory_ids": total_discovered,
            "duplicate_execution_ids_count": len(duplicate_ids),
            "total_executed_unique_ids": total_executed,
            "ids_executed_more_than_once": duplicate_ids,
            "ids_never_executed": never_executed,
            "unexpected_ids_not_in_inventory": unexpected_ids,
            "passed_count": passed_count,
            "failed_count": failed_count,
            "skipped_count": skipped_count,
            "setup_error_count": setup_error_count,
            "teardown_error_count": teardown_error_count,
            "not_executed_count": not_executed_count,
            "collection_errors": collection_error_count,
            "interrupted_runs": interrupted_run_count,
            "xml_parsing_errors_count": len(xml_parsing_errors),
            "reconciliation_verdict": "MATCH_100_PERCENT_PASSED" if is_perfect_match else "MISMATCH"
        },
        "batch_execution_metadata": batch_metadata,
        "reconciled_nodes": reconciled_nodes
    }

    reconciliation_file = reports_dir / "test_execution_reconciliation.json"
    with open(reconciliation_file, "w", encoding="utf-8") as f:
        json.dump(reconciliation_data, f, indent=2)

    run_reconciliation_file = run_dir / "test_execution_reconciliation.json"
    with open(run_reconciliation_file, "w", encoding="utf-8") as f:
        json.dump(reconciliation_data, f, indent=2)

    print(f"Reconciliation Ledger saved to {reconciliation_file} (Run ID: {run_id}).")
    print(f"Total Discovered Inventory: {total_discovered}, Executed: {total_executed}, Verdict: {reconciliation_data['metrics']['reconciliation_verdict']}")
    sys.stdout.flush()
    return reconciliation_data, run_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-batch", type=int, default=1)
    parser.add_argument("--end-batch", type=int, default=10)
    parser.add_argument("--run-id", type=str, default=None)
    args = parser.parse_args()

    generate_reconciliation_ledger(args.start_batch, args.end_batch, args.run_id)
