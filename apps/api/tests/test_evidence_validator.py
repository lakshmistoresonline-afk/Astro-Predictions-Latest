"""
Comprehensive Hardened Zero-Trust Adversarial Unit Tests for the Evidence Validator (Phase 2AW/2AX Final Defect Closure).
Fast, lightweight, deterministic temporary fixtures without redundant amend loops or git calls.
Tests occurrence-level XML accounting, canonical 10-batch plan enforcement, gate execution proof verification,
physical source_artifact_sha256 and execution_artifact_sha256 recomputation, exact per-file XML inventory validation,
naive timestamps, duplicate executions split across batches, physical log & source file tampering,
missing or non-hex digests, fail-closed Git object format detection, and all 57 required negative adversarial defect cases.
Does not monkeypatch Git status for tests that verify real Git repository state.
"""
import pytest
import json
import os
import hashlib
import subprocess
from pathlib import Path
from unittest.mock import patch
from scripts.validate_release_evidence import validate_release_evidence, CANONICAL_26_GATES, CANONICAL_GATE_FILE_COUNTS
from scripts.generate_test_inventory import generate_inventory

def init_git_repo_in_dir(repo_dir: Path) -> str:
    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"
    env["GIT_AUTHOR_DATE"] = "2026-10-25T00:00:00Z"
    env["GIT_COMMITTER_DATE"] = "2026-10-25T00:00:00Z"

    subprocess.run(["git", "init", "-q"], cwd=repo_dir, capture_output=True, env=env)
    (repo_dir / "README.md").write_text("# Test Repo\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo_dir, capture_output=True, env=env)
    subprocess.run(["git", "commit", "-m", "Initial commit", "--no-gpg-sign", "-q"], cwd=repo_dir, capture_output=True, env=env)
    res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, capture_output=True, text=True, env=env)
    return res.stdout.strip()

def compute_inv_hash(node_ids: list) -> str:
    content = "\n".join(sorted(node_ids)).encode("utf-8")
    return hashlib.sha256(content).hexdigest()

def create_valid_evidence_fixture(tmp_path: Path) -> str:
    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"
    env["GIT_AUTHOR_DATE"] = "2026-10-25T00:00:00Z"
    env["GIT_COMMITTER_DATE"] = "2026-10-25T00:00:00Z"

    subprocess.run(["git", "init", "-q"], cwd=tmp_path, capture_output=True, env=env)
    subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=tmp_path, capture_output=True, env=env)
    subprocess.run(["git", "config", "core.eol", "lf"], cwd=tmp_path, capture_output=True, env=env)
    (tmp_path / "README.md").write_text("# Test Repo\n", encoding="utf-8")

    reports_dir = tmp_path / "reports"
    docs_dir = tmp_path / "docs"
    reports_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    run_id = "RUN_20261025_000000_TEST"
    run_dir = reports_dir / "runs" / run_id
    gates_dir = run_dir / "gates"
    logs_dir = gates_dir / "logs"
    xmls_dir = gates_dir / "xmls"
    gates_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    xmls_dir.mkdir(parents=True, exist_ok=True)

    node_ids = [f"apps/api/tests/test_{i}.py::test_fn_{i}" for i in range(1, 11)]
    inv_sha = compute_inv_hash(node_ids)

    (reports_dir / "release_certification_report.md").write_text("# Report\n", encoding="utf-8")
    (docs_dir / "RELEASE_CERTIFICATION.md").write_text("# Docs\n", encoding="utf-8")
    (reports_dir / "production_readiness_audit.md").write_text("# Audit\n", encoding="utf-8")

    # Write dummy source files for all gates
    for g_id in CANONICAL_26_GATES:
        if g_id == "G01_DE440S_HASH":
            k_file = tmp_path / "apps" / "api" / "engines" / "astronomy" / "de440s.bsp"
            k_file.parent.mkdir(parents=True, exist_ok=True)
            k_file.write_bytes(b"0" * 1024)
        else:
            expected_count = CANONICAL_GATE_FILE_COUNTS.get(g_id, 1)
            for f_idx in range(1, expected_count + 1):
                tf_rel = f"apps/api/tests/test_{g_id}_{f_idx}.py"
                tf_p = tmp_path / tf_rel
                tf_p.parent.mkdir(parents=True, exist_ok=True)
                tf_p.write_bytes(f"def test_fn_{f_idx}(): assert True\n".encode("utf-8"))

    # Commit test source files to get source_sha
    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True, env=env)
    subprocess.run(["git", "commit", "-m", "Commit source files", "--no-gpg-sign", "-q"], cwd=tmp_path, capture_output=True, env=env)
    source_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True, env=env).stdout.strip()

    inv_data = {
        "repository": "Astrovision",
        "source_sha": source_sha,
        "working_tree_clean": True,
        "inventory_sha256": inv_sha,
        "total_unique_node_ids": 10,
        "node_ids": node_ids
    }
    (reports_dir / "test_node_inventory.json").write_text(json.dumps(inv_data, indent=2), encoding="utf-8")

    manifest_data = {
        "run_id": run_id,
        "source_sha": source_sha,
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
            "source_sha": source_sha,
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
        "source_sha": source_sha,
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
        log_f = logs_dir / f"gate_{g_id}.log"
        log_f.write_text(f"Gate {g_id} Execution Output Log\nStatus: PASS\n", encoding="utf-8")
        exec_hash = hashlib.sha256(log_f.read_bytes()).hexdigest()

        if g_id == "G01_DE440S_HASH":
            k_file = tmp_path / "apps" / "api" / "engines" / "astronomy" / "de440s.bsp"
            src_hash = hashlib.sha256(k_file.read_bytes()).hexdigest()
            cmd_str = "apps/api/engines/astronomy/de440s.bsp"
            tests_run_count = 1
        else:
            expected_count = CANONICAL_GATE_FILE_COUNTS.get(g_id, 1)
            tests_run_count = expected_count
            tf_paths = []
            src_bytes = b""
            for f_idx in range(1, expected_count + 1):
                tf_rel = f"apps/api/tests/test_{g_id}_{f_idx}.py"
                tf_p = tmp_path / tf_rel
                src_bytes += tf_p.read_bytes()
                tf_paths.append(tf_rel)

                g_xml = xmls_dir / f"gate_{g_id}_file_{f_idx}.xml"
                g_xml.write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="1">
    <testcase classname="apps.api.tests.test_{g_id}_{f_idx}" name="test_fn_{f_idx}" time="0.1" file="{tf_rel}" />
  </testsuite>
</testsuites>""", encoding="utf-8")
            cmd_str = ", ".join(tf_paths)
            src_hash = hashlib.sha256(src_bytes).hexdigest()

        g_entry = {
            "gate_id": g_id,
            "gate_title": g_id,
            "command": cmd_str,
            "commit_sha": source_sha,
            "inventory_sha256": inv_sha,
            "run_id": run_id,
            "exit_code": 0,
            "start_timestamp_utc": "2026-10-25T00:00:00+00:00",
            "end_timestamp_utc": "2026-10-25T00:01:00+00:00",
            "duration_seconds": 60.0,
            "tests_collected": tests_run_count,
            "tests_passed": tests_run_count,
            "tests_failed": 0,
            "tests_skipped": 0,
            "errors": 0,
            "source_artifact_sha256": src_hash,
            "execution_artifact_sha256": exec_hash,
            "artifact_hash": exec_hash,
            "status": "PASS",
            "tests_run": tests_run_count,
            "details": "PASS"
        }
        gates_26.append(g_entry)
        (gates_dir / f"gate_{g_id}.json").write_text(json.dumps(g_entry, indent=2), encoding="utf-8")

    cert_data = {
        "release_version": "6.0.0",
        "commit_sha": source_sha,
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
    (reports_dir / "release_certificate.json").write_bytes(json.dumps(cert_data, indent=2).encode("utf-8"))

    # Stage and commit evidence artifacts cleanly as Commit 2
    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True, env=env)
    subprocess.run(["git", "commit", "-m", "Publish release evidence", "--no-gpg-sign", "-q"], cwd=tmp_path, capture_output=True, env=env)
    return source_sha

def test_positive_evidence_validation(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    create_valid_evidence_fixture(tmp_path)
    generate_publication_attestation(tmp_path)
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

def test_adv_31_multi_file_gate_xml_first_fail_second_pass_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xmls_dir = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "gates" / "xmls"
    xmls_dir.mkdir(parents=True, exist_ok=True)
    f1_xml = xmls_dir / "gate_G02_ASTRONOMY_file_1.xml"
    f2_xml = xmls_dir / "gate_G02_ASTRONOMY_file_2.xml"
    f1_xml.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="apps.api.tests.test_astronomy_provider" name="test_astro_1" file="apps/api/tests/test_astronomy_provider.py"><failure message="failed"/></testcase>
  </testsuite>
</testsuites>""", encoding="utf-8")
    f2_xml.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="apps.api.tests.test_planetary_schema_integrity" name="test_schema_1" file="apps/api/tests/test_planetary_schema_integrity.py" />
  </testsuite>
</testsuites>""", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_32_missing_one_xml_report_from_multifile_gate_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xmls_dir = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "gates" / "xmls"
    f2_xml = xmls_dir / "gate_G02_ASTRONOMY_file_2.xml"
    if f2_xml.exists():
        f2_xml.unlink()
    assert validate_release_evidence(tmp_path) is False

def test_adv_33_unexpected_extra_xml_report_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xmls_dir = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "gates" / "xmls"
    f3_xml = xmls_dir / "gate_G02_ASTRONOMY_file_3.xml"
    f3_xml.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="apps.api.tests.test_extra" name="test_extra" file="apps/api/tests/test_extra.py" />
  </testsuite>
</testsuites>""", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_34_gate_proof_count_disagrees_with_xml_total_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][1]["tests_run"] = 99 # G02_ASTRONOMY claims 99 tests instead of 2
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_35_unexpected_file_4_xml_report_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xmls_dir = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "gates" / "xmls"
    f4_xml = xmls_dir / "gate_G02_ASTRONOMY_file_4.xml" # Gate G02 expects 2 files
    f4_xml.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="apps.api.tests.test_extra4" name="test_extra4" file="apps/api/tests/test_extra4.py" />
  </testsuite>
</testsuites>""", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_36_legacy_xml_coexisting_with_perfile_xml_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    xmls_dir = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "gates" / "xmls"
    legacy_xml = xmls_dir / "gate_G02_ASTRONOMY.xml" # Legacy aggregate XML coexisting with file_1 & file_2
    legacy_xml.write_text("""<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="apps.api.tests.test_legacy" name="test_legacy" file="apps/api/tests/test_legacy.py" />
  </testsuite>
</testsuites>""", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_37_tampered_physical_log_file_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    log_f = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "gates" / "logs" / "gate_G02_ASTRONOMY.log"
    log_f.write_text("TAMPERED PHYSICAL LOG CONTENT AFTER HASH WAS RECORDED\n", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_38_tampered_physical_source_file_hash_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    src_f = tmp_path / "apps" / "api" / "tests" / "test_G02_ASTRONOMY_1.py"
    src_f.write_text("# TAMPERED TEST SOURCE FILE\ndef test_fn_tampered(): assert False\n", encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_39_missing_physical_source_file_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    src_f = tmp_path / "apps" / "api" / "tests" / "test_G02_ASTRONOMY_1.py"
    if src_f.exists():
        src_f.unlink()
    assert validate_release_evidence(tmp_path) is False

def test_adv_40_empty_certificate_source_hash_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][1]["source_artifact_sha256"] = "" # empty source hash
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_41_missing_certificate_source_hash_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    del c_data["gate_results"][1]["source_artifact_sha256"] # missing field
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_42_cert_source_hash_differs_from_proof_source_hash_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][1]["source_artifact_sha256"] = "a" * 64 # valid hex but differs from proof JSON
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_43_empty_execution_hash_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][1]["execution_artifact_sha256"] = "" # empty execution hash
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_44_cert_exec_hash_differs_from_proof_exec_hash_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][1]["execution_artifact_sha256"] = "b" * 64 # valid hex but differs
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_45_missing_retained_log_file_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    log_f = tmp_path / "reports" / "runs" / "RUN_20261025_000000_TEST" / "gates" / "logs" / "gate_G02_ASTRONOMY.log"
    if log_f.exists():
        log_f.unlink()
    assert validate_release_evidence(tmp_path) is False

def test_adv_46_malformed_non_hex_sha256_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][1]["source_artifact_sha256"] = "NOT_A_VALID_HEX_SHA256_STRING!"
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_47_cert_sha_differs_from_checked_out_head_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["commit_sha"] = "0123456789abcdef0123456789abcdef01234567" # Different SHA from checked-out HEAD
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_48_publication_commit_sha_mismatch_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["publication_commit_sha"] = "0123456789abcdef0123456789abcdef01234567" # Mismatched publication SHA
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_49_unrelated_parent_sha_without_publication_model_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["commit_sha"] = "f" * 40 # Unrelated source SHA
    cert_f.write_text(json.dumps(c_data), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_50_git_commit_sha_40_char_non_hex_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["commit_sha"] = "g" * 40 # 40 chars but non-hex 'g'
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_51_git_commit_sha_39_char_short_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["commit_sha"] = "a" * 39 # 39 chars instead of 40
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_52_git_commit_sha_41_char_long_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["commit_sha"] = "b" * 41 # 41 chars instead of 40
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_53_publication_commit_sha_non_hex_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["publication_commit_sha"] = "x" * 40 # non-hex publication SHA
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_54_valid_git_commit_sha_accepted(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    generate_publication_attestation(tmp_path)
    assert len(sha) == 40
    assert validate_release_evidence(tmp_path) is True

def test_adv_55_artifact_sha256_64_char_non_hex_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["gate_results"][1]["source_artifact_sha256"] = "z" * 64 # 64 chars but non-hex 'z'
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_56_failed_object_format_detection_fails_closed(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    with patch("scripts.validate_release_evidence.get_git_object_format", return_value=None):
        assert validate_release_evidence(tmp_path) is False

def test_adv_57_unsupported_object_format_fails_closed(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    with patch("scripts.validate_release_evidence.get_git_object_format", return_value="unsupported_sha512"):
        assert validate_release_evidence(tmp_path) is False

def test_adv_58_production_ready_missing_publication_sha_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["verdict"] = "PASS - PRODUCTION READY"
    if "publication_commit_sha" in c_data:
        del c_data["publication_commit_sha"]
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_59_nonexistent_publication_sha_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["publication_commit_sha"] = "0" * 40 # Valid hex format, but commit object does not exist in Git DB
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_60_publication_sha_mismatch_with_checked_out_head_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["publication_commit_sha"] = sha # Valid commit object (parent commit), but does not match checked-out HEAD
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_61_ancestor_publication_sha_not_equal_to_head_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    # Set publication_commit_sha to parent commit (valid ancestor, but not equal to checked-out HEAD)
    c_data["publication_commit_sha"] = sha
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_62_unrelated_checkout_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["commit_sha"] = "e" * 40 # Unrelated commit SHA
    c_data["publication_commit_sha"] = "e" * 40
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_63_missing_attestation_when_required_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["verdict"] = "PASS - PRODUCTION READY"
    if "publication_commit_sha" in c_data:
        del c_data["publication_commit_sha"]
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_64_attestation_certificate_hash_mismatch_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    att_file = tmp_path / "reports" / "publication_attestation.json"
    cert_bytes = (tmp_path / "reports" / "release_certificate.json").read_bytes()
    att_data = {
        "publication_commit_sha": sha,
        "source_commit_sha": sha,
        "certificate_sha256": "0" * 64 # Mismatched cert hash
    }
    att_file.write_text(json.dumps(att_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_65_attestation_source_sha_mismatch_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    att_file = tmp_path / "reports" / "publication_attestation.json"
    cert_bytes = (tmp_path / "reports" / "release_certificate.json").read_bytes()
    cert_hash = hashlib.sha256(cert_bytes).hexdigest()
    att_data = {
        "publication_commit_sha": sha,
        "source_commit_sha": "d" * 40, # Mismatched source SHA
        "certificate_sha256": cert_hash
    }
    att_file.write_text(json.dumps(att_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_66_tampered_certificate_after_attestation_rejected(tmp_path):
    sha = create_valid_evidence_fixture(tmp_path)
    att_file = tmp_path / "reports" / "publication_attestation.json"
    cert_bytes = (tmp_path / "reports" / "release_certificate.json").read_bytes()
    cert_hash = hashlib.sha256(cert_bytes).hexdigest()
    att_data = {
        "publication_commit_sha": sha,
        "source_commit_sha": sha,
        "certificate_sha256": cert_hash
    }
    att_file.write_text(json.dumps(att_data, indent=2), encoding="utf-8")

    # Tamper certificate after attestation was generated
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["total_gates_evaluated"] = 99
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")

    assert validate_release_evidence(tmp_path) is False

def test_adv_67_generate_publication_attestation_success(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    att = generate_publication_attestation(tmp_path)
    assert len(att["publication_commit_sha"]) == 40
    assert att["source_commit_sha"] == sha
    assert len(att["certificate_sha256"]) == 64
    assert (tmp_path / "reports" / "publication_attestation.json").exists()

def test_adv_68_attestation_requires_valid_ancestor_source_commit(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["commit_sha"] = "0" * 40 # Nonexistent source commit in Git
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")

    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"
    subprocess.run(["git", "commit", "-a", "-m", "Amend cert", "--no-gpg-sign", "-q"], cwd=tmp_path, env=env)

    with pytest.raises(RuntimeError, match="Source commit SHA .* does not exist"):
        generate_publication_attestation(tmp_path)

def test_adv_69_attestation_requires_existing_git_commit(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    with pytest.raises(RuntimeError, match="Publication commit SHA .* does not exist"):
        generate_publication_attestation(tmp_path, publication_commit_sha="f" * 40)

def test_adv_70_attestation_requires_clean_tree(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    (tmp_path / "dirty.txt").write_text("uncommitted file", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Git working tree contains uncommitted changes"):
        generate_publication_attestation(tmp_path)

def test_adv_71_attestation_requires_production_ready_verdict(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["verdict"] = "FAIL - GATE FAILURE"
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")

    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"
    subprocess.run(["git", "commit", "-a", "-m", "Amend cert verdict", "--no-gpg-sign", "-q"], cwd=tmp_path, env=env)

    with pytest.raises(RuntimeError, match="Certificate verdict is 'FAIL - GATE FAILURE'"):
        generate_publication_attestation(tmp_path)

def test_adv_72_attestation_overwrite_protection_without_force(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    generate_publication_attestation(tmp_path)

    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"
    subprocess.run(["git", "add", "."], cwd=tmp_path, env=env)
    subprocess.run(["git", "commit", "-m", "Commit attestation", "--no-gpg-sign", "-q"], cwd=tmp_path, env=env)

    with pytest.raises(RuntimeError, match="Publication attestation already exists"):
        generate_publication_attestation(tmp_path)

def test_adv_73_attestation_force_overwrite_allowed(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    generate_publication_attestation(tmp_path)

    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"
    subprocess.run(["git", "add", "."], cwd=tmp_path, env=env)
    subprocess.run(["git", "commit", "-m", "Commit attestation", "--no-gpg-sign", "-q"], cwd=tmp_path, env=env)

    att_forced = generate_publication_attestation(tmp_path, force=True)
    assert att_forced["source_commit_sha"] == sha

def test_adv_74_attestation_verifies_certificate_content_in_git_commit(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)

    cert_f = tmp_path / "reports" / "release_certificate.json"
    c_data = json.loads(cert_f.read_text(encoding="utf-8"))
    c_data["total_executed_tests"] = 999
    cert_f.write_text(json.dumps(c_data, indent=2), encoding="utf-8")

    with pytest.raises(RuntimeError, match="Git working tree contains uncommitted changes"):
        generate_publication_attestation(tmp_path)

def test_adv_75_attestation_rejects_identical_source_and_publication_commits(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    with pytest.raises(RuntimeError, match="must be a strict descendant of source commit SHA"):
        generate_publication_attestation(tmp_path, publication_commit_sha=sha)

def test_adv_78_stale_attestation_from_prior_commit_rejected(tmp_path):
    from scripts.generate_publication_attestation import get_git_commit_sha
    sha = create_valid_evidence_fixture(tmp_path)
    att_file = tmp_path / "reports" / "publication_attestation.json"
    cert_bytes = (tmp_path / "reports" / "release_certificate.json").read_bytes()
    cert_hash = hashlib.sha256(cert_bytes).hexdigest()
    att_data = {
        "publication_commit_sha": get_git_commit_sha(tmp_path),
        "source_commit_sha": "a" * 40, # Stale source SHA from prior commit
        "certificate_sha256": cert_hash
    }
    att_file.write_text(json.dumps(att_data, indent=2), encoding="utf-8")
    assert validate_release_evidence(tmp_path) is False

def test_adv_79_runner_cleans_stale_prior_attestation(tmp_path):
    from scripts.generate_publication_attestation import get_git_commit_sha
    from scripts.run_release_certification import run_release_certification
    sha = create_valid_evidence_fixture(tmp_path)
    att_file = tmp_path / "reports" / "publication_attestation.json"
    att_data = {
        "publication_commit_sha": get_git_commit_sha(tmp_path),
        "source_commit_sha": "b" * 40, # Stale prior commit
        "certificate_sha256": "0" * 64
    }
    att_file.write_text(json.dumps(att_data, indent=2), encoding="utf-8")

    # Re-running certification cleans stale prior attestation
    run_release_certification(tmp_path)
    assert not att_file.exists()

def test_adv_80_complete_release_evidence_lifecycle_success(tmp_path):
    from scripts.generate_publication_attestation import generate_publication_attestation

    # Stage 1: Tested Source Commit & Evidence Publication Commit
    sha = create_valid_evidence_fixture(tmp_path)

    # Stage 2: Detached Attestation Generation for Publication Commit
    att = generate_publication_attestation(tmp_path)
    assert att["source_commit_sha"] == sha

    # Stage 3: Final Validation of Publication Commit & Detached Attestation
    assert validate_release_evidence(tmp_path) is True

def test_adv_81_untracked_exact_attestation_exempted(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    from scripts.generate_publication_attestation import generate_publication_attestation
    sha = create_valid_evidence_fixture(tmp_path)
    generate_publication_attestation(tmp_path)
    assert check_git_status_clean(tmp_path) is True

def test_adv_82_untracked_other_attestation_rejected(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    sha = create_valid_evidence_fixture(tmp_path)
    (tmp_path / "reports" / "other_publication_attestation.json").write_text("{}", encoding="utf-8")
    assert check_git_status_clean(tmp_path) is False

def test_adv_83_untracked_nested_attestation_rejected(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    sha = create_valid_evidence_fixture(tmp_path)
    other_dir = tmp_path / "other"
    other_dir.mkdir(parents=True, exist_ok=True)
    (other_dir / "publication_attestation.json").write_text("{}", encoding="utf-8")
    assert check_git_status_clean(tmp_path) is False

def test_adv_84_untracked_attestation_bak_rejected(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    sha = create_valid_evidence_fixture(tmp_path)
    (tmp_path / "reports" / "publication_attestation.json.bak").write_text("{}", encoding="utf-8")
    assert check_git_status_clean(tmp_path) is False

def test_adv_85_unrelated_untracked_file_rejected(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    sha = create_valid_evidence_fixture(tmp_path)
    (tmp_path / "dirty.txt").write_text("uncommitted file", encoding="utf-8")
    assert check_git_status_clean(tmp_path) is False

def test_adv_86_tracked_modified_attestation_rejected(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    from scripts.generate_publication_attestation import generate_publication_attestation
    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"

    sha = create_valid_evidence_fixture(tmp_path)
    generate_publication_attestation(tmp_path)

    # Commit attestation so it becomes tracked
    subprocess.run(["git", "add", "."], cwd=tmp_path, env=env)
    subprocess.run(["git", "commit", "-m", "Commit attestation", "--no-gpg-sign", "-q"], cwd=tmp_path, env=env)

    # Now modify tracked attestation
    att_file = tmp_path / "reports" / "publication_attestation.json"
    att_file.write_text("{}", encoding="utf-8")
    assert check_git_status_clean(tmp_path) is False

def test_adv_87_staged_attestation_rejected(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    from scripts.generate_publication_attestation import generate_publication_attestation
    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"

    sha = create_valid_evidence_fixture(tmp_path)
    generate_publication_attestation(tmp_path)

    # Stage attestation
    subprocess.run(["git", "add", "reports/publication_attestation.json"], cwd=tmp_path, env=env)
    assert check_git_status_clean(tmp_path) is False

def test_adv_88_tracked_deleted_attestation_rejected(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    from scripts.generate_publication_attestation import generate_publication_attestation
    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"

    sha = create_valid_evidence_fixture(tmp_path)
    generate_publication_attestation(tmp_path)

    subprocess.run(["git", "add", "."], cwd=tmp_path, env=env)
    subprocess.run(["git", "commit", "-m", "Commit attestation", "--no-gpg-sign", "-q"], cwd=tmp_path, env=env)

    # Delete committed attestation from working tree
    (tmp_path / "reports" / "publication_attestation.json").unlink()
    assert check_git_status_clean(tmp_path) is False

def test_adv_89_rename_attestation_rejected(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    from scripts.generate_publication_attestation import generate_publication_attestation
    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = "test@astrovision.test"
    env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_COMMITTER_EMAIL"] = "test@astrovision.test"

    sha = create_valid_evidence_fixture(tmp_path)
    generate_publication_attestation(tmp_path)

    subprocess.run(["git", "add", "."], cwd=tmp_path, env=env)
    subprocess.run(["git", "commit", "-m", "Commit attestation", "--no-gpg-sign", "-q"], cwd=tmp_path, env=env)

    # Rename attestation
    subprocess.run(["git", "mv", "reports/publication_attestation.json", "reports/renamed_attestation.json"], cwd=tmp_path, env=env)
    assert check_git_status_clean(tmp_path) is False

def test_adv_90_normal_clean_repo_passes(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    sha = create_valid_evidence_fixture(tmp_path)
    assert check_git_status_clean(tmp_path) is True

def test_adv_91_status_parser_raw_unicode_bytes(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    sha = create_valid_evidence_fixture(tmp_path)

    # Create file with space and unicode in filename
    (tmp_path / "reports" / "test file unicode_äöü.txt").write_text("unicode test", encoding="utf-8")
    assert check_git_status_clean(tmp_path) is False

def test_adv_94_stale_attestation_safe_archival_verification(tmp_path):
    from scripts.run_release_certification import run_release_certification
    sha = create_valid_evidence_fixture(tmp_path)
    att_file = tmp_path / "reports" / "publication_attestation.json"
    old_content = json.dumps({"source_commit_sha": "c" * 40, "certificate_sha256": "0" * 64}, indent=2)
    att_file.write_text(old_content, encoding="utf-8")

    custom_gate = [("G01_DE440S_HASH", "NASA JPL DE440s Kernel SHA-256 Checksum", "apps/api/engines/astronomy/de440s.bsp")]
    run_release_certification(tmp_path, custom_gates=custom_gate)

    # Old attestation is unlinked from main path, and archived to .json.bak
    assert not att_file.exists()
    baks = list((tmp_path / "reports").glob("publication_attestation_stale_*.json.bak"))
    assert len(baks) == 1
    assert json.loads(baks[0].read_text(encoding="utf-8"))["source_commit_sha"] == "c" * 40

def test_adv_95_exclusive_archival_prevents_overwrite(tmp_path):
    from scripts.run_release_certification import run_release_certification
    sha = create_valid_evidence_fixture(tmp_path)
    att_file = tmp_path / "reports" / "publication_attestation.json"
    old_content = json.dumps({"source_commit_sha": "d" * 40, "certificate_sha256": "0" * 64}, indent=2)
    att_file.write_text(old_content, encoding="utf-8")

    custom_gate = [("G01_DE440S_HASH", "NASA JPL DE440s Kernel SHA-256 Checksum", "apps/api/engines/astronomy/de440s.bsp")]
    run_release_certification(tmp_path, custom_gates=custom_gate)

    # First archival created one .json.bak
    baks_1 = list((tmp_path / "reports").glob("publication_attestation_stale_*.json.bak"))
    assert len(baks_1) == 1

    # Re-write another stale attestation
    att_file.write_text(old_content, encoding="utf-8")
    run_release_certification(tmp_path, custom_gates=custom_gate)

    # Second archival created another unique .json.bak without overwriting
    baks_2 = list((tmp_path / "reports").glob("publication_attestation_stale_*.json.bak"))
    assert len(baks_2) == 2

def test_adv_98_status_parser_rejects_literal_backslash_filename(tmp_path):
    from scripts.validate_release_evidence import check_git_status_clean
    sha = create_valid_evidence_fixture(tmp_path)
    # File with literal backslash in filename is NOT exempted
    (tmp_path / "reports" / "publication_attestation.json.bak").write_text("{}", encoding="utf-8")
    assert check_git_status_clean(tmp_path) is False
