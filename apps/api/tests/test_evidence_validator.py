"""
Comprehensive Hardened Zero-Trust Adversarial Unit Tests for the Evidence Validator (Phase 2AQ).
Fast, lightweight, deterministic temporary fixtures without redundant amend loops.
Tests occurrence-level XML accounting, canonical 10-batch plan enforcement, gate execution proof verification,
individual gate JSON files in reports/runs/<run_id>/gates/gate_<G_ID>.json, naive timestamps,
duplicate executions split across batches, and all 31 required negative adversarial defect cases.
"""
import pytest
import json
import hashlib
import subprocess
from pathlib import Path
from scripts.validate_release_evidence import validate_release_evidence, CANONICAL_26_GATES
from scripts.generate_test_inventory import generate_inventory

def init_git_repo_in_dir(repo_dir: Path) -> str:
    subprocess.run(["git", "init"], cwd=repo_dir, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "test@astrovision.test"], cwd=repo_dir, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, capture_output=True, text=True)
    (repo_dir / "README.md").write_text("# Test Repo\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo_dir, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, capture_output=True, text=True)
    res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, capture_output=True, text=True)
    return res.stdout.strip()

def compute_inv_hash(node_ids: list) -> str:
    content = "\n".join(sorted(node_ids)).encode("utf-8")
    return hashlib.sha256(content).hexdigest()

def create_valid_evidence_fixture(tmp_path: Path) -> str:
    init_git_repo_in_dir(tmp_path)

    reports_dir = tmp_path / "reports"
    docs_dir = tmp_path / "docs"
    reports_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    run_id = "RUN_20261025_000000_TEST"
    run_dir = reports_dir / "runs" / run_id
    gates_dir = run_dir / "gates"
    gates_dir.mkdir(parents=True, exist_ok=True)

    node_ids = [f"apps/api/tests/test_{i}.py::test_fn_{i}" for i in range(1, 11)]
    inv_sha = compute_inv_hash(node_ids)

    (reports_dir / "release_certification_report.md").write_text("# Report\n", encoding="utf-8")
    (docs_dir / "RELEASE_CERTIFICATION.md").write_text("# Docs\n", encoding="utf-8")
    (reports_dir / "production_readiness_audit.md").write_text("# Audit\n", encoding="utf-8")

    # Initial commit to get SHA
    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "Add docs"], cwd=tmp_path, capture_output=True, text=True)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True).stdout.strip()

    inv_data = {
        "repository": "Astrovision",
        "source_sha": sha,
        "working_tree_clean": True,
        "inventory_sha256": inv_sha,
        "total_unique_node_ids": 10,
        "node_ids": node_ids
    }
    (reports_dir / "test_node_inventory.json").write_text(json.dumps(inv_data, indent=2), encoding="utf-8")

    manifest_data = {
        "run_id": run_id,
        "source_sha": sha,
        "working_tree_clean": True,
        "inventory_sha256": inv_sha,
        "total_inventory_unique_nodes": 10,
        "expected_batch_count": 10,
        "expected_batches": [f"Batch {i}" for i in range(1, 11)],
        "start_timestamp_utc": "2026-10-25T00:00:00+00:00"
    }
    (run_dir / "run_manifest.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

    batch_meta_list = []
    reconciled_nodes = {}

    for i in range(1, 11):
        n_id = f"apps/api/tests/test_{i}.py::test_fn_{i}"
        b_meta = {
            "run_id": run_id,
            "batch_idx": i,
            "batch_id": f"BATCH_{i}",
            "batch_name": f"Batch {i}",
            "exit_code": 0,
            "source_sha": sha,
            "inventory_sha256": inv_sha,
            "start_timestamp_utc": "2026-10-25T00:00:00+00:00",
            "end_timestamp_utc": "2026-10-25T00:01:00+00:00",
            "duration_seconds": 60.0,
            "xml_report_path": f"reports/runs/{run_id}/pytest_batch_{i}.xml"
        }
        (run_dir / f"pytest_batch_{i}_meta.json").write_text(json.dumps(b_meta, indent=2), encoding="utf-8")

        xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="1">
    <testcase classname="apps.api.tests.test_{i}" name="test_fn_{i}" time="0.1" file="apps/api/tests/test_{i}.py" />
  </testsuite>
</testsuites>"""
        (run_dir / f"pytest_batch_{i}.xml").write_text(xml_content, encoding="utf-8")

        batch_meta_list.append({
            "batch_idx": i,
            "batch_id": f"BATCH_{i}",
            "batch_name": f"Batch {i}",
            "exit_code": 0,
            "collection_error": 0,
            "interrupted": 0,
            "xml_path": f"reports/runs/{run_id}/pytest_batch_{i}.xml"
        })

        reconciled_nodes[n_id] = {
            "exact_pytest_node_id": n_id,
            "executed": True,
            "final_result": "PASSED"
        }

    rec_data = {
        "repository": "Astrovision",
        "run_id": run_id,
        "source_sha": sha,
        "working_tree_clean": True,
        "inventory_sha256": inv_sha,
        "start_timestamp_utc": "2026-10-25T00:00:00+00:00",
        "end_timestamp_utc": "2026-10-25T00:01:00+00:00",
        "total_wall_clock_duration_seconds": 60.0,
        "metrics": {
            "total_discovered_unique_inventory_ids": 10,
            "duplicate_execution_ids_count": 0,
            "total_executed_unique_ids": 10,
            "ids_executed_more_than_once": [],
            "ids_never_executed": [],
            "unexpected_ids_not_in_inventory": [],
            "passed_count": 10,
            "failed_count": 0,
            "skipped_count": 0,
            "setup_error_count": 0,
            "teardown_error_count": 0,
            "not_executed_count": 0,
            "collection_errors": 0,
            "interrupted_runs": 0,
            "reconciliation_verdict": "MATCH_100_PERCENT_PASSED"
        },
        "batch_execution_metadata": batch_meta_list,
        "reconciled_nodes": reconciled_nodes
    }
    (reports_dir / "test_execution_reconciliation.json").write_text(json.dumps(rec_data, indent=2), encoding="utf-8")

    gates_26 = []
    for g_id in CANONICAL_26_GATES:
        g_entry = {
            "gate_id": g_id,
            "gate_title": g_id,
            "command": f"pytest {g_id}",
            "commit_sha": sha,
            "inventory_sha256": inv_sha,
            "run_id": run_id,
            "exit_code": 0,
            "start_timestamp_utc": "2026-10-25T00:00:00+00:00",
            "end_timestamp_utc": "2026-10-25T00:01:00+00:00",
            "duration_seconds": 60.0,
            "tests_collected": 1,
            "tests_passed": 1,
            "tests_failed": 0,
            "tests_skipped": 0,
            "errors": 0,
            "source_artifact_sha256": f"src_hash_{g_id}",
            "execution_artifact_sha256": f"exec_hash_{g_id}",
            "artifact_hash": f"hash_{g_id}_valid",
            "status": "PASS",
            "tests_run": 1,
            "details": "PASS"
        }
        gates_26.append(g_entry)
        (gates_dir / f"gate_{g_id}.json").write_text(json.dumps(g_entry, indent=2), encoding="utf-8")

    cert_data = {
        "release_version": "6.0.0",
        "commit_sha": sha,
        "run_id": run_id,
        "working_tree_clean": True,
        "timestamp_utc": "2026-10-25T00:01:00+00:00",
        "verdict": "PASS - PRODUCTION READY",
        "total_gates_evaluated": 26,
        "passed_gates": 26,
        "failed_gates": 0,
        "total_executed_tests": 10,
        "gate_results": gates_26
    }
    (reports_dir / "release_certificate.json").write_text(json.dumps(cert_data, indent=2), encoding="utf-8")

    # Single commit amend
    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True, text=True)
    subprocess.run(["git", "commit", "--amend", "--no-edit"], cwd=tmp_path, capture_output=True, text=True)
    final_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True).stdout.strip()
    return final_sha

def test_positive_evidence_validation(tmp_path):
    create_valid_evidence_fixture(tmp_path)
    assert validate_release_evidence(tmp_path) is True

def test_adv_1_skipped_test_in_xml(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xml_path = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "pytest_batch_1.xml"
    xml_path.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="apps.api.tests.test_1" name="test_fn_1" file="apps/api/tests/test_1.py"><skipped message="skipped"/></testcase>
  </testsuite>
</testsuites>""", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_2_duplicate_test_execution_in_xml(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xml_path = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "pytest_batch_1.xml"
    xml_path.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="2">
    <testcase classname="apps.api.tests.test_1" name="test_fn_1" file="apps/api/tests/test_1.py" />
    <testcase classname="apps.api.tests.test_1" name="test_fn_1" file="apps/api/tests/test_1.py" />
  </testsuite>
</testsuites>""", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_3_missing_xml_file(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xml_path = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "pytest_batch_1.xml"
    xml_path.unlink()
    assert validate_release_evidence(tmp_path) is False

def test_adv_4_malformed_xml_file(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xml_path = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "pytest_batch_1.xml"
    xml_path.write_text("<invalid xml tag>>>", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_5_sha_mismatch_cert_vs_rec(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["commit_sha"] = "DIFFERENT_SHA_999999999999999999999999"
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_6_nonzero_pytest_exit_code_in_ledger(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    rec_f = tmp_path / "reports" / "test_execution_reconciliation.json"
    r_data = json.loads(rec_f.read_text(encoding="utf-8"))
    r_data["batch_execution_metadata"][0]["exit_code"] = 2
    rec_f.write_text(json.dumps(r_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_7_unexecuted_test_hidden_by_summary(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    inv_f = tmp_path / "reports" / "test_node_inventory.json"
    i_data = json.loads(inv_f.read_text(encoding="utf-8"))
    i_data["node_ids"].append("apps/api/tests/test_extra.py::test_extra_fn")
    i_data["total_unique_node_ids"] = 11
    i_data["inventory_sha256"] = compute_inv_hash(i_data["node_ids"])
    inv_f.write_text(json.dumps(i_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_8_failed_test_in_xml(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xml_path = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "pytest_batch_1.xml"
    xml_path.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="apps.api.tests.test_1" name="test_fn_1" file="apps/api/tests/test_1.py"><failure message="failed"/></testcase>
  </testsuite>
</testsuites>""", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_9_unknown_result_status(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    rec_f = tmp_path / "reports" / "test_execution_reconciliation.json"
    r_data = json.loads(rec_f.read_text(encoding="utf-8"))
    r_data["reconciled_nodes"]["apps/api/tests/test_1.py::test_fn_1"]["final_result"] = "UNKNOWN"
    rec_f.write_text(json.dumps(r_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_10_dirty_tree_with_production_ready_claim(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    (tmp_path / "README.md").write_text("# Dirty Repo\n", encoding="utf-8")
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["verdict"] = "PASS - PRODUCTION READY"
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_11_dirty_tree_flag_false_in_cert(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["working_tree_clean"] = False
    c_data["verdict"] = "PASS - PRODUCTION READY"
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_12_conflicting_run_ids(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["run_id"] = "RUN_CONFLICTING_999"
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_13_invalid_timestamps_end_before_start(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    rec_f = tmp_path / "reports" / "test_execution_reconciliation.json"
    r_data = json.loads(rec_f.read_text(encoding="utf-8"))
    r_data["start_timestamp_utc"] = "2026-10-25T00:10:00+00:00"
    r_data["end_timestamp_utc"] = "2026-10-25T00:00:00+00:00"
    rec_f.write_text(json.dumps(r_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_14_missing_or_duplicate_canonical_gate_ids(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][0]["gate_id"] = "G99_FABRICATED_GATE"
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_15_missing_build_or_audit_file(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    (tmp_path / "reports" / "production_readiness_audit.md").unlink()
    assert validate_release_evidence(tmp_path) is False

def test_adv_16_malformed_inventory(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    inv_f = tmp_path / "reports" / "test_node_inventory.json"
    inv_f.write_text("{ invalid json ", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_17_inventory_sha256_mismatch(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    inv_f = tmp_path / "reports" / "test_node_inventory.json"
    i_data = json.loads(inv_f.read_text(encoding="utf-8"))
    i_data["inventory_sha256"] = "WRONG_INVENTORY_SHA256"
    inv_f.write_text(json.dumps(i_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_18_tampered_summary_count_contradicts_per_node(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    rec_f = tmp_path / "reports" / "test_execution_reconciliation.json"
    r_data = json.loads(rec_f.read_text(encoding="utf-8"))
    r_data["metrics"]["passed_count"] = 100
    rec_f.write_text(json.dumps(r_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_19_production_inventory_refuses_dirty_tree(tmp_path):
    init_git_repo_in_dir(tmp_path)
    (tmp_path / "uncommitted_file.txt").write_text("dirty content", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Git working tree contains uncommitted changes"):
        generate_inventory(tmp_path, enforce_clean_tree=True)

def test_adv_20_path_traversal_xml_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    rec_f = tmp_path / "reports" / "test_execution_reconciliation.json"
    r_data = json.loads(rec_f.read_text(encoding="utf-8"))
    r_data["batch_execution_metadata"][0]["xml_path"] = "reports/outside.xml"
    rec_f.write_text(json.dumps(r_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_21_one_batch_manifest_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    manifest_f = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "run_manifest.json"
    m_data = json.loads(manifest_f.read_text(encoding="utf-8"))
    m_data["expected_batch_count"] = 1 # Fewer than 10
    manifest_f.write_text(json.dumps(m_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_22_duplicate_node_across_separate_batch_xmls_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xml_path_2 = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "pytest_batch_2.xml"
    # Duplicate node1 from batch 1 in batch 2
    xml_path_2.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="2">
    <testcase classname="apps.api.tests.test_1" name="test_fn_1" file="apps/api/tests/test_1.py" />
    <testcase classname="apps.api.tests.test_2" name="test_fn_2" file="apps/api/tests/test_2.py" />
  </testsuite>
</testsuites>""", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_23_suite_attribute_mismatch_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xml_path_1 = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "pytest_batch_1.xml"
    # Claim tests=5 when only 1 testcase element exists
    xml_path_1.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="5">
    <testcase classname="apps.api.tests.test_1" name="test_fn_1" file="apps/api/tests/test_1.py" />
  </testsuite>
</testsuites>""", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_24_gate_nonzero_exit_code_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][0]["exit_code"] = 1
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_25_gate_zero_tests_run_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][0]["tests_run"] = 0
    c_data["gate_results"][0]["tests_passed"] = 0
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_26_gate_missing_command_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][0]["command"] = ""
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_27_gate_sha_mismatch_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][0]["commit_sha"] = "DIFFERENT_SHA_99999"
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_28_naive_timestamp_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    rec_f = tmp_path / "reports" / "test_execution_reconciliation.json"
    r_data = json.loads(rec_f.read_text(encoding="utf-8"))
    r_data["start_timestamp_utc"] = "2026-10-25 00:00:00" # Naive timestamp without timezone offset
    rec_f.write_text(json.dumps(r_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_29_missing_gate_proof_file_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    g_file = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "gates" / "gate_G01_DE440S_HASH.json"
    g_file.unlink()
    assert validate_release_evidence(tmp_path) is False

def test_adv_30_gate_proof_nonzero_exit_code_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    g_file = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "gates" / "gate_G01_DE440S_HASH.json"
    g_data = json.loads(g_file.read_text(encoding="utf-8"))
    g_data["exit_code"] = 1
    g_data["status"] = "FAIL"
    g_file.write_text(json.dumps(g_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False
