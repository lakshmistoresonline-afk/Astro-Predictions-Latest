"""
Astrovision Version 6.0.0 Release Certification System Runner (Phase 2BQ Hardened Implementation).
Executes and evaluates the 26 canonical release gates (G01 - G26), generating traceable,
independently verifiable gate execution evidence files in reports/runs/<run_id>/gates/gate_<G_ID>.json,
isolated per-file gate JUnit XMLs in reports/runs/<run_id>/gates/xmls/gate_<G_ID>_file_<N>.xml,
and genuine operating-system subprocess captured stdout/stderr output log files in
reports/runs/<run_id>/gates/logs/gate_<G_ID>.log with distinct source_artifact_sha256 and execution_artifact_sha256 digests.
"""
import os
import sys
import json
import time
import hashlib
import tempfile
import platform
import subprocess
import xml.etree.ElementTree as ET
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
            return len(res.stdout.strip()) == 0
    except Exception:
        pass
    return False

def compute_inventory_hash(node_ids: list) -> str:
    content = "\n".join(sorted(node_ids)).encode("utf-8")
    return hashlib.sha256(content).hexdigest()

def run_release_certification(
    project_root: Optional[Path] = None,
    custom_gates: Optional[List] = None,
    output_dir: Optional[Path] = None,
    run_id: str = "RUN_CERTIFICATION"
) -> Dict[str, Any]:
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent

    orig_cwd = os.getcwd()
    try:
        os.chdir(project_root)

        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        commit_sha = get_git_commit_sha(project_root)
        clean_tree = is_git_working_tree_clean(project_root)

        cert_dir = (output_dir or project_root) / "reports"
        cert_dir.mkdir(parents=True, exist_ok=True)

        # Exclusive Collision-Protected Archival of Stale Publication Attestation
        att_path = cert_dir / "publication_attestation.json"
        if att_path.exists() and att_path.stat().st_size > 0:
            try:
                old_bytes = att_path.read_bytes()
                old_att = json.loads(old_bytes.decode("utf-8"))
                if old_att.get("source_commit_sha") != commit_sha:
                    ts_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                    counter = 0
                    arch_path = None
                    while counter < 100:
                        rand_str = hashlib.md5(f"{time.time()}_{os.getpid()}_{counter}".encode()).hexdigest()[:6]
                        candidate_path = cert_dir / f"publication_attestation_stale_{ts_str}_{rand_str}.json.bak"
                        try:
                            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | (getattr(os, "O_BINARY", 0))
                            fd = os.open(str(candidate_path), flags, 0o644)
                            with os.fdopen(fd, "wb") as f:
                                f.write(old_bytes)
                                f.flush()
                                os.fsync(f.fileno())
                            arch_path = candidate_path
                            break
                        except FileExistsError:
                            counter += 1

                    if arch_path and arch_path.exists():
                        arch_bytes = arch_path.read_bytes()
                        if arch_bytes == old_bytes or arch_bytes.replace(b"\r\n", b"\n") == old_bytes.replace(b"\r\n", b"\n"):
                            att_path.unlink()
                            print(f"Safely archived stale publication attestation to {arch_path}")
                        else:
                            print(f"Warning: Archived file bytes differ from original attestation bytes. Retaining original {att_path}")
                    else:
                        print("Warning: Could not establish exclusive non-colliding archive filename after 100 attempts")
            except Exception as arch_exc:
                print(f"Warning: Failed to archive stale attestation safely: {arch_exc}")

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
        xmls_dir = gates_dir / "xmls"
        gates_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)
        xmls_dir.mkdir(parents=True, exist_ok=True)

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
                "source_artifact_sha256": "dirty_working_tree",
                "execution_artifact_sha256": exec_hash,
                "artifact_hash": exec_hash,
                "status": "FAIL",
                "tests_run": 0,
                "details": f"Working tree is dirty (clean={clean_tree})"
            }
            gate_results.append(pf_entry)
            (gates_dir / "gate_G00_PREFLIGHT_GIT_CLEAN.json").write_text(json.dumps(pf_entry, indent=2), encoding="utf-8")

        # Gate G01 Special Pre-compiled Ephemeris Kernel Integrity Check
        if any(g[0] == "G01_DE440S_HASH" for g in gates_to_run) and not is_malformed:
            t_start = datetime.now(timezone.utc)
            de440s_path = project_root / "apps" / "api" / "engines" / "astronomy" / "de440s.bsp"
            if de440s_path.exists() and de440s_path.stat().st_size > 0:
                k_bytes = de440s_path.read_bytes()
                kernel_hash = hashlib.sha256(k_bytes).hexdigest()
                t_end = datetime.now(timezone.utc)
                dur = (t_end - t_start).total_seconds()

                if kernel_hash == EXPECTED_DE440S_SHA256:
                    log_file = logs_dir / "gate_G01_DE440S_HASH.log"
                    log_text = f"DE440s Kernel Verification Log\nFile: {de440s_path}\nSize: {len(k_bytes)} bytes\nSHA-256: {kernel_hash}\nStatus: PASS\n"
                    log_file.write_text(log_text, encoding="utf-8")
                    exec_hash = hashlib.sha256(log_file.read_bytes()).hexdigest()

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
                        "details": f"DE440s kernel verified ({len(k_bytes):,} bytes, SHA-256: {kernel_hash[:16]}...)"
                    }
                    gate_results.append(g1_entry)
                    (gates_dir / "gate_G01_DE440S_HASH.json").write_text(json.dumps(g1_entry, indent=2), encoding="utf-8")
                    total_tests_executed += 1
                else:
                    all_passed = False
                    log_file = logs_dir / "gate_G01_DE440S_HASH.log"
                    log_text = f"DE440s Kernel Verification Log\nChecksum Mismatch! Got {kernel_hash}, Expected {EXPECTED_DE440S_SHA256}\n"
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

        # Remaining Gates: Operating-System Subprocess Pytest Execution with Per-File Unique XMLs
        pytest_gates = [g for g in gates_to_run if isinstance(g, (tuple, list)) and len(g) == 3 and g[0] != "G01_DE440S_HASH"] if not is_malformed else []
        for gate_id, title, test_files in pytest_gates:
            t_start = datetime.now(timezone.utc)
            file_list = test_files if isinstance(test_files, list) else [test_files]
            cmd_str = ", ".join(file_list)

            file_bytes = b""
            gate_failed = False
            last_exit_code = 0

            for tf in file_list:
                p = project_root / tf
                if p.exists():
                    file_bytes += p.read_bytes()
                else:
                    all_passed = False
                    gate_failed = True

            src_hash = hashlib.sha256(file_bytes).hexdigest() if file_bytes else "missing_test_files"

            # Clean stale XML files for this gate before execution
            for stale_xml in xmls_dir.glob(f"gate_{gate_id}*.xml"):
                try:
                    stale_xml.unlink()
                except Exception:
                    pass

            g_passed = 0
            g_failed = 0
            g_skipped = 0
            g_errors = 0
            sub_stdout = ""
            sub_stderr = ""

            for file_idx, tf in enumerate(file_list, 1):
                p = project_root / tf
                if not p.exists():
                    g_errors += 1
                    gate_failed = True
                    continue

                xml_out = xmls_dir / f"gate_{gate_id}_file_{file_idx}.xml"
                py_args = [
                    sys.executable, "-m", "pytest",
                    str(p),
                    "-s",
                    f"--junitxml={xml_out}",
                    "-o", "junit_family=xunit2"
                ]

                try:
                    proc = subprocess.run(
                        py_args,
                        cwd=project_root,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    sub_stdout += f"\n--- [{tf}] STDOUT ---\n" + proc.stdout
                    sub_stderr += f"\n--- [{tf}] STDERR ---\n" + proc.stderr
                    last_exit_code = proc.returncode

                    if proc.returncode != 0:
                        gate_failed = True

                except subprocess.TimeoutExpired as tex:
                    sub_stdout += f"\n--- [{tf}] TIMEOUT EXPIRED ---\n"
                    sub_stderr += f"\n--- [{tf}] TIMEOUT EXPIRED: {tex} ---\n"
                    last_exit_code = 124
                    gate_failed = True
                except Exception as p_exc:
                    sub_stderr += f"\n--- [{tf}] SUBPROCESS EXCEPTION: {p_exc} ---\n"
                    last_exit_code = 1
                    gate_failed = True

                if xml_out.exists() and xml_out.stat().st_size > 0:
                    try:
                        gtree = ET.parse(xml_out)
                        groot = gtree.getroot()
                        for tc in groot.iter("testcase"):
                            if tc.find("failure") is not None:
                                g_failed += 1
                            elif tc.find("error") is not None:
                                g_errors += 1
                            elif tc.find("skipped") is not None:
                                g_skipped += 1
                            else:
                                g_passed += 1
                    except Exception:
                        g_errors += 1
                        gate_failed = True
                else:
                    g_errors += 1
                    gate_failed = True

            t_end = datetime.now(timezone.utc)
            dur = (t_end - t_start).total_seconds()

            tests_run = g_passed + g_failed
            if g_skipped > 0 or g_errors > 0 or g_failed > 0:
                gate_failed = True

            log_file = logs_dir / f"gate_{gate_id}.log"
            log_text = f"=== GATE {gate_id} SUBPROCESS EXECUTED OUTPUT LOG ===\nCommand: {cmd_str}\nExit Code: {last_exit_code}\nCollected: {tests_run + g_skipped}\nPassed: {g_passed}\nFailed: {g_failed}\nSkipped: {g_skipped}\nErrors: {g_errors}\n=== PROCESS STDOUT ===\n{sub_stdout}\n=== PROCESS STDERR ===\n{sub_stderr}\n"
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
                    "tests_collected": tests_run + g_skipped,
                    "tests_passed": g_passed,
                    "tests_failed": g_failed,
                    "tests_skipped": g_skipped,
                    "errors": g_errors,
                    "source_artifact_sha256": src_hash,
                    "execution_artifact_sha256": exec_hash,
                    "artifact_hash": exec_hash,
                    "status": "FAIL",
                    "tests_run": tests_run,
                    "details": f"Pytest failed (Exit code {last_exit_code}, {g_failed} failed, {g_skipped} skipped)"
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
                    "tests_collected": g_passed,
                    "tests_passed": g_passed,
                    "tests_failed": 0,
                    "tests_skipped": 0,
                    "errors": 0,
                    "source_artifact_sha256": src_hash,
                    "execution_artifact_sha256": exec_hash,
                    "artifact_hash": exec_hash,
                    "status": "PASS",
                    "tests_run": g_passed,
                    "details": f"Pytest executed successfully ({g_passed} tests passed)"
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
        elif not clean_tree and is_production_run and all_passed:
            verdict = "INCOMPLETE - EVIDENCE NOT VERIFIED"
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

        cert_bytes = json.dumps(cert_data, indent=2).encode("utf-8")
        cert_json_path.write_bytes(cert_bytes)

        doc_md_path.write_text(f"# RELEASE CERTIFICATION REPORT\nVerdict: {verdict}\nCommit: {commit_sha}\n", encoding="utf-8")

        print(f"\nRelease certificate written to {cert_json_path}")
        print(f"Final Verdict: {verdict}")

        return cert_data
    finally:
        os.chdir(orig_cwd)

if __name__ == "__main__":
    res = run_release_certification()
    if res["verdict"] != "PASS - PRODUCTION READY":
        sys.exit(1)
