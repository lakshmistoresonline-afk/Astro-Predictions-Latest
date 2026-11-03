"""
Hardened Zero-Trust Release Evidence Validator (Phase 2BB Detached Publication Attestation & Non-Circular Provenance Model).
Independently parses actual JUnit XML reports across batches and per-file gate XMLs,
enforces exact expected per-file XML inventory for every canonical gate,
recomputes physical source_artifact_sha256 and execution_artifact_sha256 digests directly from disk files,
validates strict 64-char hex formatting for all SHA digests,
validates Git commit IDs against detected repository object format (sha1=40 hex chars, sha256=64 hex chars),
validates non-circular provenance via detached publication_attestation.json or DAG ancestry (--is-ancestor),
cross-checks certificate digests against proof JSONs, physical disk files, and checked-out Git HEAD SHA fail-closed,
checks Git status, validates all 26 canonical release gates, execution proof, source SHAs, timestamps,
and build evidence against strict zero-trust invariants before certifying production readiness.
Strictly enforces occurrence-level accounting, exact per-file XML inventory, the canonical 10-batch plan, and zero-tolerance exit code rules.
"""
import json
import sys
import os
import hashlib
import functools
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

CANONICAL_GATE_FILE_COUNTS = {
    "G01_DE440S_HASH": 0,
    "G02_ASTRONOMY": 2,
    "G03_TIMEZONE_DST": 2,
    "G04_RASHI_NAKSHATRA": 1,
    "G05_ASCENDANT_HOUSES": 1,
    "G06_VARGAS_D1_D60": 1,
    "G07_VIMSHOTTARI_DASHA": 1,
    "G08_CLASSICAL_YOGAS": 1,
    "G09_CLASSICAL_DOSHAS": 1,
    "G10_SHADBALA": 1,
    "G11_ASHTAKAVARGA": 1,
    "G12_JAIMINI_SUTRAS": 1,
    "G13_TRANSITS": 1,
    "G14_PANCHANGA": 1,
    "G15_MUHURTA": 1,
    "G16_PREDICTIVE_TIMING": 2,
    "G17_RECTIFICATION": 1,
    "G18_COMPATIBILITY": 1,
    "G19_PREDICTION_EVIDENCE": 1,
    "G20_AI_TRUST_BOUNDARY": 1,
    "G21_AI_VALIDATION": 1,
    "G22_PERSISTENCE": 1,
    "G23_IDOR_CONTROLS": 1,
    "G24_API_CONTRACTS": 1,
    "G25_PDF_EXPORT": 2,
    "G26_ADMIN_SECURITY": 1,
}

CANONICAL_10_BATCH_IDS = [f"BATCH_{i}" for i in range(1, 11)]

@functools.lru_cache(maxsize=512)
def _run_git_cmd(project_root_str: str, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    return subprocess.run(["git"] + list(args), cwd=project_root_str, capture_output=True, text=True, env=env)

def check_git_status_clean(project_root: Path, ignore_detached_attestation: bool = True) -> bool:
    try:
        env = dict(os.environ)
        res = subprocess.run(["git", "status", "--porcelain=v1", "-z"], cwd=str(project_root), capture_output=True, env=env)
        if res.returncode != 0:
            return False

        raw_stdout = res.stdout
        if not raw_stdout:
            return True

        entries = raw_stdout.split(b"\x00")
        i = 0
        n = len(entries)

        target_bytes = b"reports/publication_attestation.json"

        while i < n:
            entry = entries[i]
            if not entry:
                i += 1
                continue

            if len(entry) < 3:
                return False  # Malformed status line

            x_byte = entry[0]
            y_byte = entry[1]

            path_bytes = entry[3:] if entry[2:3] == b" " else entry[2:]

            # Rename or copy records output two NUL-delimited paths: <target_path>\0<orig_path>\0
            is_rename_or_copy = (x_byte in [ord('R'), ord('C')]) or (y_byte in [ord('R'), ord('C')])
            if is_rename_or_copy:
                i += 1  # Consume original path
                if i >= n:
                    return False
                return False  # Renames and copies are modified tracked changes -> DIRTY

            # Exact byte-level untracked attestation exemption check (ONLY target_bytes)
            is_exact_untracked_attestation = (
                x_byte == ord('?') and y_byte == ord('?') and path_bytes == target_bytes
            )

            if ignore_detached_attestation and is_exact_untracked_attestation:
                i += 1
                continue

            # Any other byte entry means working tree is dirty
            return False

        return True
    except Exception:
        pass
    return False

def get_git_commit_sha(project_root: Path) -> str:
    try:
        res = _run_git_cmd(str(project_root), "rev-parse", "HEAD")
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return ""

def get_git_parent_sha(project_root: Path) -> str:
    try:
        res = _run_git_cmd(str(project_root), "rev-parse", "HEAD~1")
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return ""

def get_git_object_format(project_root: Path) -> Optional[str]:
    try:
        res = _run_git_cmd(str(project_root), "rev-parse", "--show-object-format")
        if res.returncode == 0:
            fmt = res.stdout.strip().lower()
            if fmt in ["sha1", "sha256"]:
                return fmt
    except Exception:
        pass
    return None

def is_git_ancestor(project_root: Path, ancestor_sha: str, descendant_sha: str) -> bool:
    try:
        res = _run_git_cmd(str(project_root), "merge-base", "--is-ancestor", ancestor_sha, descendant_sha)
        return res.returncode == 0
    except Exception:
        return False

def is_git_commit_in_repo(project_root: Path, commit_sha: str) -> bool:
    try:
        res = _run_git_cmd(str(project_root), "cat-file", "-e", f"{commit_sha}^{{commit}}")
        return res.returncode == 0
    except Exception:
        return False

def is_valid_sha256_hex(val: Any) -> bool:
    if not isinstance(val, str) or len(val) != 64:
        return False
    try:
        int(val, 16)
        return True
    except ValueError:
        return False

def is_valid_git_commit_sha(val: Any, object_format: str = "sha1") -> bool:
    expected_len = 64 if object_format == "sha256" else 40
    if not isinstance(val, str) or len(val) != expected_len:
        return False
    try:
        int(val, 16)
        return True
    except ValueError:
        return False

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
    attestation_data: Optional[Dict[str, Any]] = None

    try:
        inventory_data = json.loads((reports_dir / "test_node_inventory.json").read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"Failed to parse test_node_inventory.json: {e}")

    try:
        reconciliation_data = json.loads((reports_dir / "test_execution_reconciliation.json").read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"Failed to parse test_execution_reconciliation.json: {e}")

    try:
        certificate_raw_bytes = (reports_dir / "release_certificate.json").read_bytes()
        certificate_data = json.loads(certificate_raw_bytes.decode("utf-8"))
    except Exception as e:
        errors.append(f"Failed to parse release_certificate.json: {e}")

    attestation_file = reports_dir / "publication_attestation.json"
    if attestation_file.exists() and attestation_file.stat().st_size > 0:
        try:
            attestation_data = json.loads(attestation_file.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"Failed to parse publication_attestation.json: {e}")

    if errors:
        print("ZERO-TRUST EVIDENCE VALIDATION FAILED (JSON Parse Failure):")
        for err in errors:
            print(f" - {err}")
        return False

    # Live Checked-Out Git HEAD & Tested Source Revision Verification
    obj_fmt = get_git_object_format(project_root)
    if not obj_fmt or obj_fmt not in ["sha1", "sha256"]:
        errors.append(f"Unsupported or failed Git repository object format detection: '{obj_fmt}' (expected sha1 or sha256)")
        obj_fmt = "sha1"

    live_head_sha = get_git_commit_sha(project_root)
    pub_commit_sha = certificate_data.get("publication_commit_sha")

    # 3. Validate Inventory Format and SHA-256 Hash
    inv_nodes = inventory_data.get("node_ids", [])
    if not isinstance(inv_nodes, list) or len(inv_nodes) == 0:
        errors.append("test_node_inventory.json has empty or invalid node_ids list")

    inv_set = set(inv_nodes)
    if len(inv_nodes) != len(inv_set):
        errors.append("test_node_inventory.json contains duplicate node IDs")

    computed_inv_sha = compute_inventory_hash(inv_nodes)
    inv_sha_field = inventory_data.get("inventory_sha256", "")
    if not inv_sha_field or not is_valid_sha256_hex(inv_sha_field):
        errors.append(f"Inventory inventory_sha256 is missing, empty, or non-hex: '{inv_sha_field}'")
    elif inv_sha_field != computed_inv_sha:
        errors.append(f"Inventory inventory_sha256 field ({inv_sha_field}) disagrees with computed hash ({computed_inv_sha})")

    inv_count = inventory_data.get("total_unique_node_ids", 0)
    if inv_count != len(inv_set):
        errors.append(f"Inventory total_unique_node_ids ({inv_count}) does not match actual node count ({len(inv_set)})")

    # 4. Validate Run Manifest & Mandatory 10-Batch Plan
    rec_run_id = reconciliation_data.get("run_id", "")
    if not rec_run_id:
        errors.append("Reconciliation ledger missing run_id")

    rec_sha = reconciliation_data.get("source_sha", "")
    if not rec_sha or not is_valid_git_commit_sha(rec_sha, obj_fmt):
        errors.append(f"Reconciliation ledger source_sha is missing, empty, or malformed for object format '{obj_fmt}': '{rec_sha}'")

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

    # 8. Validate Release Certificate Integrity & Individual Gate Evidence JSON & Log & Per-File XML Files
    cert_sha = certificate_data.get("commit_sha", "")
    if not cert_sha or not is_valid_git_commit_sha(cert_sha, obj_fmt):
        errors.append(f"Certificate commit_sha is missing, empty, or malformed for object format '{obj_fmt}': '{cert_sha}'")

    if cert_sha != rec_sha:
        errors.append(f"Certificate SHA ({cert_sha}) does not match reconciliation ledger SHA ({rec_sha})")

    cert_verdict = certificate_data.get("verdict", "")

    if cert_verdict == "PASS - PRODUCTION READY" and not pub_commit_sha and not attestation_data:
        errors.append("Certificate claiming 'PASS - PRODUCTION READY' requires an explicit publication_commit_sha or publication_attestation.json")

    # Detached Publication Attestation Evaluation (Non-Circular Model)
    if attestation_data:
        att_pub_sha = attestation_data.get("publication_commit_sha")
        att_src_sha = attestation_data.get("source_commit_sha")
        att_cert_hash = attestation_data.get("certificate_sha256")

        if not att_pub_sha or not is_valid_git_commit_sha(att_pub_sha, obj_fmt):
            errors.append(f"Publication attestation contains missing or malformed publication_commit_sha: '{att_pub_sha}'")
        elif not is_git_commit_in_repo(project_root, att_pub_sha):
            errors.append(f"Publication attestation publication_commit_sha ({att_pub_sha}) does not exist in Git object database")
        elif live_head_sha and att_pub_sha != live_head_sha:
            errors.append(f"Publication attestation publication_commit_sha ({att_pub_sha}) does not match checked-out Git HEAD ({live_head_sha})")

        if not att_cert_hash or not is_valid_sha256_hex(att_cert_hash):
            errors.append(f"Publication attestation contains missing or malformed certificate_sha256: '{att_cert_hash}'")
        else:
            recomputed_cert_hash = hashlib.sha256(certificate_raw_bytes).hexdigest()
            if att_cert_hash != recomputed_cert_hash:
                errors.append(f"Publication attestation certificate_sha256 mismatch! Attestation recorded {att_cert_hash}, computed {recomputed_cert_hash}")

        if att_src_sha != cert_sha:
            errors.append(f"Publication attestation source_commit_sha ({att_src_sha}) disagrees with certificate commit_sha ({cert_sha})")

    # Strict Provenance Identity Model Verification
    if pub_commit_sha:
        if not is_valid_git_commit_sha(pub_commit_sha, obj_fmt):
            errors.append(f"Certificate publication_commit_sha is malformed for object format '{obj_fmt}': '{pub_commit_sha}'")
        elif not is_git_commit_in_repo(project_root, pub_commit_sha):
            errors.append(f"Certificate publication_commit_sha ({pub_commit_sha}) does not exist in Git repository object database")
        elif live_head_sha and pub_commit_sha != live_head_sha and not is_git_ancestor(project_root, pub_commit_sha, live_head_sha):
            errors.append(f"Certificate publication_commit_sha ({pub_commit_sha}) does not match current checked-out Git HEAD ({live_head_sha})")

        if cert_sha and pub_commit_sha and is_valid_git_commit_sha(cert_sha, obj_fmt) and is_valid_git_commit_sha(pub_commit_sha, obj_fmt):
            if not is_git_commit_in_repo(project_root, cert_sha):
                errors.append(f"Certificate source_commit_sha ({cert_sha}) does not exist in Git repository object database")
            elif not is_git_ancestor(project_root, cert_sha, pub_commit_sha):
                errors.append(f"Certificate source_commit_sha ({cert_sha}) is not a verified Git ancestor of publication_commit_sha ({pub_commit_sha}) in Git DAG history")
    else:
        # Non-circular provenance model: cert_sha is tested source_commit_sha, verified against Git repo and live_head_sha ancestry
        if cert_sha and live_head_sha and is_valid_git_commit_sha(cert_sha, obj_fmt):
            if not is_git_commit_in_repo(project_root, cert_sha):
                errors.append(f"Certificate source commit SHA ({cert_sha}) does not exist in Git repository object database")
            elif cert_sha != live_head_sha and not is_git_ancestor(project_root, cert_sha, live_head_sha):
                errors.append(f"Certificate source commit SHA ({cert_sha}) does not match or exist in Git ancestor lineage of checked-out HEAD ({live_head_sha})")

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
        xmls_proof_dir = gates_proof_dir / "xmls"

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

            # FAIL-CLOSED SHA-256 Digest Validation on Certificate Entry
            cert_src_sha = g_item.get("source_artifact_sha256")
            cert_exec_sha = g_item.get("execution_artifact_sha256")

            if not cert_src_sha or not is_valid_sha256_hex(cert_src_sha):
                errors.append(f"Gate {g_id} in certificate missing, empty, or non-hex source_artifact_sha256: '{cert_src_sha}'")

            if not cert_exec_sha or not is_valid_sha256_hex(cert_exec_sha):
                errors.append(f"Gate {g_id} in certificate missing, empty, or non-hex execution_artifact_sha256: '{cert_exec_sha}'")

            # Physical Source Artifact Hash Recomputation & Verification
            if g_id == "G01_DE440S_HASH":
                de440s_file = project_root / g_cmd
                if not de440s_file.exists():
                    de440s_file = project_root / "apps" / "api" / "engines" / "astronomy" / "de440s.bsp"
                if not de440s_file.exists() or de440s_file.stat().st_size == 0:
                    errors.append(f"Gate G01_DE440S_HASH missing physical ephemeris kernel file: {de440s_file}")
                else:
                    recomputed_kernel_sha = hashlib.sha256(de440s_file.read_bytes()).hexdigest()
                    if cert_src_sha and cert_src_sha != recomputed_kernel_sha:
                        errors.append(f"Gate G01_DE440S_HASH physical kernel SHA-256 mismatch! Certificate recorded {cert_src_sha}, computed {recomputed_kernel_sha}")
            else:
                cmd_file_paths = [p.strip() for p in g_cmd.split(",") if p.strip()]
                src_bytes = b""
                for tf_path_str in cmd_file_paths:
                    tf_file = project_root / tf_path_str
                    try:
                        res_tf = tf_file.resolve()
                        if not res_tf.is_relative_to(project_root.resolve()):
                            errors.append(f"Gate {g_id} test source path ({tf_path_str}) escapes project root")
                    except Exception:
                        errors.append(f"Gate {g_id} test source path resolution error: {tf_path_str}")

                    if not tf_file.exists() or tf_file.stat().st_size == 0:
                        errors.append(f"Gate {g_id} missing or empty physical test source file: {tf_path_str}")
                    else:
                        src_bytes += tf_file.read_bytes()

                if src_bytes:
                    recomputed_src_sha = hashlib.sha256(src_bytes).hexdigest()
                    if cert_src_sha and cert_src_sha != recomputed_src_sha:
                        errors.append(f"Source artifact hash mismatch for {g_id}! Certificate recorded {cert_src_sha}, computed {recomputed_src_sha}")

            # Cross-check against individual gate evidence JSON file
            proof_src_sha = None
            proof_exec_sha = None
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

                        proof_src_sha = g_file_data.get("source_artifact_sha256")
                        proof_exec_sha = g_file_data.get("execution_artifact_sha256")

                        if not proof_src_sha or not is_valid_sha256_hex(proof_src_sha):
                            errors.append(f"Gate proof file for {g_id} missing, empty, or non-hex source_artifact_sha256: '{proof_src_sha}'")

                        if not proof_exec_sha or not is_valid_sha256_hex(proof_exec_sha):
                            errors.append(f"Gate proof file for {g_id} missing, empty, or non-hex execution_artifact_sha256: '{proof_exec_sha}'")

                        if cert_src_sha and proof_src_sha and cert_src_sha != proof_src_sha:
                            errors.append(f"Gate {g_id} source SHA mismatch between certificate ({cert_src_sha}) and proof JSON ({proof_src_sha})")

                        if cert_exec_sha and proof_exec_sha and cert_exec_sha != proof_exec_sha:
                            errors.append(f"Gate {g_id} execution SHA mismatch between certificate ({cert_exec_sha}) and proof JSON ({proof_exec_sha})")

                    except Exception as g_exc:
                        errors.append(f"Failed to parse gate proof file for {g_id}: {g_exc}")

            # Verify retained output log file against physical file bytes on disk
            if logs_proof_dir.exists():
                log_f = logs_proof_dir / f"gate_{g_id}.log"
                if not log_f.exists() or log_f.stat().st_size == 0:
                    errors.append(f"Missing retained gate output log file: {log_f.relative_to(project_root)}")
                else:
                    recomputed_exec_hash = hashlib.sha256(log_f.read_bytes()).hexdigest()
                    if cert_exec_sha and cert_exec_sha != recomputed_exec_hash:
                        errors.append(f"Execution artifact hash mismatch for {g_id}! Certificate recorded {cert_exec_sha}, computed {recomputed_exec_hash}")
                    if proof_exec_sha and proof_exec_sha != recomputed_exec_hash:
                        errors.append(f"Execution artifact hash mismatch for {g_id}! Proof JSON recorded {proof_exec_sha}, computed {recomputed_exec_hash}")

            # Strict Per-File XML Inventory Validation
            if xmls_proof_dir.exists() and g_id != "G01_DE440S_HASH":
                expected_files_count = CANONICAL_GATE_FILE_COUNTS.get(g_id, 1)
                expected_xml_set = set()

                for file_idx in range(1, expected_files_count + 1):
                    expected_xml_file = xmls_proof_dir / f"gate_{g_id}_file_{file_idx}.xml"
                    if not expected_xml_file.exists() or expected_xml_file.stat().st_size == 0:
                        fallback_xml = xmls_proof_dir / f"gate_{g_id}.xml"
                        if fallback_xml.exists() and fallback_xml.stat().st_size > 0 and expected_files_count == 1:
                            expected_xml_set.add(fallback_xml)
                        else:
                            errors.append(f"Missing expected per-file XML report for gate {g_id} file index {file_idx}: gate_{g_id}_file_{file_idx}.xml")
                    else:
                        expected_xml_set.add(expected_xml_file)

                # Find ALL matching XML files for this gate in xmls_proof_dir
                actual_matching_xmls = set(xmls_proof_dir.glob(f"gate_{g_id}*.xml"))

                # Reject any unexpected extra XML file, non-canonical index, or legacy aggregate XML coexisting with per-file XMLs
                unexpected_xmls = actual_matching_xmls - expected_xml_set
                if len(unexpected_xmls) > 0:
                    for unexp_f in unexpected_xmls:
                        errors.append(f"Gate {g_id} contains unexpected extra or non-canonical XML report: {unexp_f.name}")

                g_xml_passed = 0
                g_xml_failed = 0
                g_xml_skipped = 0
                g_xml_errors = 0
                for g_xml in expected_xml_set:
                    if not g_xml.exists() or g_xml.stat().st_size == 0:
                        continue
                    try:
                        gtree = ET.parse(g_xml)
                        groot = gtree.getroot()
                        for tc in groot.iter("testcase"):
                            if tc.find("failure") is not None:
                                g_xml_failed += 1
                            elif tc.find("error") is not None:
                                g_xml_errors += 1
                            elif tc.find("skipped") is not None:
                                g_xml_skipped += 1
                            else:
                                g_xml_passed += 1
                    except Exception as g_xml_exc:
                        errors.append(f"Failed to parse gate XML report {g_xml}: {g_xml_exc}")

                if g_xml_failed > 0 or g_xml_skipped > 0 or g_xml_errors > 0:
                    errors.append(f"Gate {g_id} per-file XML report contains non-passing tests (Failed: {g_xml_failed}, Skipped: {g_xml_skipped}, Errors: {g_xml_errors})")
                if g_xml_passed != g_tests:
                    errors.append(f"Gate {g_id} proof test count ({g_tests}) disagrees with parsed per-file XML test count ({g_xml_passed})")

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
