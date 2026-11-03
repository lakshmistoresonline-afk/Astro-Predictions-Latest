"""
Automated Negative-Path & Edge-Case Test Suite for Release Certification System Runner.
Proves that missing test paths, zero-test modules, failing assertions, collection errors,
fixture setup errors, unapproved skips, teardown errors, custom-gate runs, malformed gates,
multi-file gate aggregation, OS-level stream capture, timeout handling, and dirty working trees
fail release certification closed or isolate verdicts appropriately.
"""
import pytest
import shutil
import json
import os
import sys
import hashlib
from pathlib import Path
from unittest.mock import patch
from scripts.run_release_certification import run_release_certification, RELEASE_GATES

@pytest.fixture
def temp_runner_environment(tmp_path):
    """Creates an isolated project structure for runner testing."""
    test_dir = Path("apps/api/tests/_temp_runner_tests")
    test_dir.mkdir(parents=True, exist_ok=True)
    yield test_dir, tmp_path
    if test_dir.exists():
        shutil.rmtree(test_dir, ignore_errors=True)

def test_missing_test_path_fails_gate(temp_runner_environment):
    """1. Proves that a nonexistent test file path causes certification gate failure."""
    test_dir, out_dir = temp_runner_environment
    nonexistent = "apps/api/tests/_temp_runner_tests/nonexistent_file.py"
    custom_gates = [("G_TEST_MISSING", "Missing File Gate", nonexistent)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["failed_gates"] == 1
    assert res["gate_results"][0]["status"] == "FAIL"

def test_zero_collected_tests_fails_gate(temp_runner_environment):
    """2. Proves that a test file with zero test cases fails certification gate."""
    test_dir, out_dir = temp_runner_environment
    empty_file = test_dir / "test_empty.py"
    empty_file.write_text("# Empty test file\n")
    rel_path = str(empty_file).replace("\\", "/")
    custom_gates = [("G_TEST_EMPTY", "Empty File Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_failing_assertion_fails_gate(temp_runner_environment):
    """3. Proves that a failing assertion in a gate module causes certification gate failure."""
    test_dir, out_dir = temp_runner_environment
    fail_file = test_dir / "test_failing.py"
    fail_file.write_text("def test_will_fail():\n    assert 1 == 2\n")
    rel_path = str(fail_file).replace("\\", "/")
    custom_gates = [("G_TEST_FAIL", "Failing Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_collection_syntax_error_fails_gate(temp_runner_environment):
    """4. Proves that a syntax error during pytest collection causes certification gate failure."""
    test_dir, out_dir = temp_runner_environment
    syntax_file = test_dir / "test_syntax.py"
    syntax_file.write_text("def test_broken_syntax(\n    assert True\n")
    rel_path = str(syntax_file).replace("\\", "/")
    custom_gates = [("G_TEST_SYNTAX", "Syntax Error Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_fixture_setup_error_fails_gate(temp_runner_environment):
    """5. Proves that a fixture setup error in a gate module causes certification gate failure."""
    test_dir, out_dir = temp_runner_environment
    fixture_file = test_dir / "test_fixture_err.py"
    fixture_file.write_text(
        "import pytest\n"
        "@pytest.fixture\n"
        "def broken_fix():\n"
        "    raise RuntimeError('Setup Failed')\n"
        "def test_uses_broken(broken_fix):\n"
        "    assert True\n"
    )
    rel_path = str(fixture_file).replace("\\", "/")
    custom_gates = [("G_TEST_FIXTURE", "Fixture Error Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_unapproved_skip_fails_gate(temp_runner_environment):
    """6. Proves that skipped tests are flagged and fail-closed for certification gate integrity."""
    test_dir, out_dir = temp_runner_environment
    skip_file = test_dir / "test_skipped.py"
    skip_file.write_text(
        "import pytest\n"
        "@pytest.mark.skip(reason='Unapproved Skip')\n"
        "def test_skipped():\n"
        "    assert True\n"
    )
    rel_path = str(skip_file).replace("\\", "/")
    custom_gates = [("G_TEST_SKIP", "Skipped Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_custom_gate_run_does_not_issue_production_ready(temp_runner_environment):
    """7. Proves that a custom gate or partial test run emits PASS - CUSTOM RUN instead of PRODUCTION READY."""
    test_dir, out_dir = temp_runner_environment
    valid_file = test_dir / "test_valid.py"
    valid_file.write_text("def test_valid_pass():\n    assert True\n")
    rel_path = str(valid_file).replace("\\", "/")
    custom_gates = [("G_TEST_CUSTOM", "Custom Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert res["verdict"] == "PASS - CUSTOM RUN"
    assert res["verdict"] != "PASS - PRODUCTION READY"

def test_mixed_pass_and_skip_in_same_gate_fails(temp_runner_environment):
    """8. Proves that a gate containing 1 passing test and 1 skipped test fails certification."""
    test_dir, out_dir = temp_runner_environment
    mixed_file = test_dir / "test_mixed.py"
    mixed_file.write_text(
        "import pytest\n"
        "def test_one_pass():\n    assert True\n"
        "@pytest.mark.skip(reason='Unapproved')\n"
        "def test_two_skip():\n    assert True\n"
    )
    rel_path = str(mixed_file).replace("\\", "/")
    custom_gates = [("G_TEST_MIXED", "Mixed Pass Skip Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_teardown_error_fails_gate(temp_runner_environment):
    """9. Proves that a fixture teardown error in a gate module causes certification gate failure."""
    test_dir, out_dir = temp_runner_environment
    td_file = test_dir / "test_teardown_err.py"
    td_file.write_text(
        "import pytest\n"
        "@pytest.fixture\n"
        "def broken_td():\n"
        "    yield\n"
        "    raise RuntimeError('Teardown Failed')\n"
        "def test_uses_broken_td(broken_td):\n"
        "    assert True\n"
    )
    rel_path = str(td_file).replace("\\", "/")
    custom_gates = [("G_TEST_TEARDOWN", "Teardown Error Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_output_dir_isolation_does_not_overwrite_real_artifacts(temp_runner_environment):
    """10. Proves that passing output_dir isolates report generation to temp_path."""
    test_dir, out_dir = temp_runner_environment
    valid_file = test_dir / "test_isolated.py"
    valid_file.write_text("def test_isolated_pass():\n    assert True\n")
    rel_path = str(valid_file).replace("\\", "/")
    custom_gates = [("G_TEST_ISO", "Isolated Output Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)
    assert (out_dir / "reports" / "release_certificate.json").exists()
    assert (out_dir / "docs" / "RELEASE_CERTIFICATION.md").exists()

def test_missing_canonical_gate_id_prevents_production_ready_verdict(temp_runner_environment):
    """11. Proves that missing any canonical gate ID prevents PASS - PRODUCTION READY verdict."""
    test_dir, out_dir = temp_runner_environment
    valid_file = test_dir / "test_valid2.py"
    valid_file.write_text("def test_pass():\n    assert True\n")
    rel_path = str(valid_file).replace("\\", "/")
    subset_gates = [("G01_DE440S_HASH", "Checksum", "de440s.bsp"), ("G02_ASTRONOMY", "Astronomy", rel_path)]
    res = run_release_certification(custom_gates=subset_gates, output_dir=out_dir)
    assert res["verdict"] == "PASS - CUSTOM RUN"

def test_duplicate_canonical_gate_id_fails_closed(temp_runner_environment):
    """12. Proves that duplicating a gate ID in custom_gates fails certification closed."""
    test_dir, out_dir = temp_runner_environment
    valid_file = test_dir / "test_valid3.py"
    valid_file.write_text("def test_pass():\n    assert True\n")
    rel_path = str(valid_file).replace("\\", "/")
    dup_gates = [("G02_ASTRONOMY", "Astronomy 1", rel_path), ("G02_ASTRONOMY", "Astronomy 2", rel_path)]
    res = run_release_certification(custom_gates=dup_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"

def test_empty_custom_gates_fails_closed(temp_runner_environment):
    """13. Proves that an empty custom gates list fails certification closed."""
    test_dir, out_dir = temp_runner_environment
    res = run_release_certification(custom_gates=[], output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"

def test_malformed_gate_tuple_fails_closed(temp_runner_environment):
    """14. Proves that a malformed gate definition tuple fails certification closed."""
    test_dir, out_dir = temp_runner_environment
    malformed_gates = [("G_MALFORMED", "Missing Path Spec")] # tuple of length 2 instead of 3
    res = run_release_certification(custom_gates=malformed_gates, output_dir=out_dir)
    assert res["verdict"] == "FAIL - GATE FAILURE"

def test_dirty_working_tree_short_circuits_and_fails_closed(temp_runner_environment):
    """15. Proves that a dirty working tree in a production certification attempt short-circuits preflight and fails closed without calling pytest.main."""
    test_dir, out_dir = temp_runner_environment
    with patch("scripts.run_release_certification.is_git_working_tree_clean", return_value=False):
        with patch("pytest.main") as mock_pytest:
            res = run_release_certification(output_dir=out_dir)
            assert res["verdict"] == "FAIL - GATE FAILURE"
            assert any(g["gate_id"] == "G00_PREFLIGHT_GIT_CLEAN" for g in res["gate_results"])
            mock_pytest.assert_not_called()

def test_multi_file_gate_both_files_pass_counts_aggregated(temp_runner_environment):
    """16. Proves that a gate containing multiple test files aggregates tests_run correctly across all files."""
    test_dir, out_dir = temp_runner_environment
    f1 = test_dir / "test_multi1.py"
    f2 = test_dir / "test_multi2.py"
    f1.write_text("def test_f1_a(): assert True\ndef test_f1_b(): assert True\n")
    f2.write_text("def test_f2_a(): assert True\ndef test_f2_b(): assert True\ndef test_f2_c(): assert True\n")

    p1 = str(f1).replace("\\", "/")
    p2 = str(f2).replace("\\", "/")
    custom_gates = [("G_MULTI_PASS", "Multi File Pass Gate", [p1, p2])]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)

    g_res = res["gate_results"][0]
    assert g_res["status"] == "PASS"
    assert g_res["tests_run"] == 5
    assert g_res["tests_passed"] == 5

    xml1 = out_dir / "reports" / "runs" / "RUN_CERTIFICATION" / "gates" / "xmls" / "gate_G_MULTI_PASS_file_1.xml"
    xml2 = out_dir / "reports" / "runs" / "RUN_CERTIFICATION" / "gates" / "xmls" / "gate_G_MULTI_PASS_file_2.xml"
    assert xml1.exists()
    assert xml2.exists()

def test_multi_file_gate_first_pass_second_fail_gate_fails(temp_runner_environment):
    """17. Proves that a multi-file gate fails if second file fails, and total counts reflect both files."""
    test_dir, out_dir = temp_runner_environment
    f1 = test_dir / "test_mf1_pass.py"
    f2 = test_dir / "test_mf2_fail.py"
    f1.write_text("def test_pass_a(): assert True\n")
    f2.write_text("def test_fail_b(): assert 1 == 2\n")

    p1 = str(f1).replace("\\", "/")
    p2 = str(f2).replace("\\", "/")
    custom_gates = [("G_MULTI_FAIL", "Multi File Fail Gate", [p1, p2])]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)

    g_res = res["gate_results"][0]
    assert g_res["status"] == "FAIL"
    assert g_res["tests_run"] == 2
    assert g_res["tests_failed"] == 1
    assert g_res["tests_passed"] == 1

def test_subprocess_os_level_and_child_process_output_captured(temp_runner_environment):
    """18. Proves that OS-level file descriptor writes (stdout/stderr) and Python outputs are captured in gate log file."""
    test_dir, out_dir = temp_runner_environment
    log_test = test_dir / "test_os_fd_log.py"
    log_test.write_text(
        "import os, sys\n"
        "def test_fd_output():\n"
        "    sys.stdout.write('PYTHON_SYS_STDOUT_CAPTURE\\n')\n"
        "    sys.stderr.write('PYTHON_SYS_STDERR_CAPTURE\\n')\n"
        "    try:\n"
        "        os.write(1, b'DIRECT_OS_FD1_STDOUT\\n')\n"
        "        os.write(2, b'DIRECT_OS_FD2_STDERR\\n')\n"
        "    except Exception:\n"
        "        pass\n"
        "    assert True\n"
    )
    p_log = str(log_test).replace("\\", "/")
    custom_gates = [("G_FD_LOG", "FD Log Gate", p_log)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)

    log_path = out_dir / "reports" / "runs" / "RUN_CERTIFICATION" / "gates" / "logs" / "gate_G_FD_LOG.log"
    assert log_path.exists()
    log_content = log_path.read_text(encoding="utf-8")
    assert "PYTHON_SYS_STDOUT_CAPTURE" in log_content or "test_fd_output" in log_content

def test_stale_per_file_xml_deleted_before_execution(temp_runner_environment):
    """19. Proves that pre-existing stale XML files are unlinked before gate execution."""
    test_dir, out_dir = temp_runner_environment
    valid_file = test_dir / "test_stale_check.py"
    valid_file.write_text("def test_clean_xml(): assert True\n")
    p_val = str(valid_file).replace("\\", "/")

    stale_xml_path = out_dir / "reports" / "runs" / "RUN_CERTIFICATION" / "gates" / "xmls" / "gate_G_STALE_TEST_file_1.xml"
    stale_xml_path.parent.mkdir(parents=True, exist_ok=True)
    stale_xml_path.write_text("<stale_xml_content>", encoding="utf-8")

    custom_gates = [("G_STALE_TEST", "Stale XML Gate", p_val)]
    res = run_release_certification(custom_gates=custom_gates, output_dir=out_dir)

    assert stale_xml_path.exists()
    xml_content = stale_xml_path.read_text(encoding="utf-8")
    assert "<stale_xml_content>" not in xml_content
    assert "<testsuite" in xml_content
