"""
Automated Negative-Path Test Suite for Release Certification System Runner.
Proves that missing test paths, zero-test modules, failing assertions, collection errors,
internal setup errors, and unapproved skips fail release certification closed.
Includes positive control proving valid gates pass cleanly.
"""
import pytest
import shutil
from pathlib import Path
from scripts.run_release_certification import run_release_certification

@pytest.fixture
def temp_runner_environment(tmp_path):
    """Creates an isolated project structure for runner testing."""
    test_dir = Path("apps/api/tests/_temp_runner_tests")
    test_dir.mkdir(parents=True, exist_ok=True)
    yield test_dir
    if test_dir.exists():
        shutil.rmtree(test_dir, ignore_errors=True)

def test_missing_test_path_fails_gate(temp_runner_environment):
    """1. Proves that a nonexistent test file path causes certification gate failure."""
    nonexistent = "apps/api/tests/_temp_runner_tests/nonexistent_file.py"
    custom_gates = [("G_TEST_MISSING", "Missing File Gate", nonexistent)]
    res = run_release_certification(custom_gates=custom_gates)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["failed_gates"] == 1
    assert res["gate_results"][0]["status"] == "FAIL"

def test_zero_collected_tests_fails_gate(temp_runner_environment):
    """2. Proves that a test file with zero test cases fails certification gate."""
    empty_file = temp_runner_environment / "test_empty.py"
    empty_file.write_text("# Empty test file\n")
    rel_path = str(empty_file).replace("\\", "/")
    custom_gates = [("G_TEST_EMPTY", "Empty File Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_failing_assertion_fails_gate(temp_runner_environment):
    """3. Proves that a failing assertion in a gate module causes certification gate failure."""
    fail_file = temp_runner_environment / "test_failing.py"
    fail_file.write_text("def test_will_fail():\n    assert 1 == 2\n")
    rel_path = str(fail_file).replace("\\", "/")
    custom_gates = [("G_TEST_FAIL", "Failing Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_collection_syntax_error_fails_gate(temp_runner_environment):
    """4. Proves that a syntax error during pytest collection causes certification gate failure."""
    syntax_file = temp_runner_environment / "test_syntax.py"
    syntax_file.write_text("def test_broken_syntax(\n    assert True\n")
    rel_path = str(syntax_file).replace("\\", "/")
    custom_gates = [("G_TEST_SYNTAX", "Syntax Error Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_fixture_setup_error_fails_gate(temp_runner_environment):
    """5. Proves that a fixture setup error in a gate module causes certification gate failure."""
    fixture_file = temp_runner_environment / "test_fixture_err.py"
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
    res = run_release_certification(custom_gates=custom_gates)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_unapproved_skip_fails_gate(temp_runner_environment):
    """6. Proves that skipped tests are flagged and fail-closed for certification gate integrity."""
    skip_file = temp_runner_environment / "test_skipped.py"
    skip_file.write_text(
        "import pytest\n"
        "@pytest.mark.skip(reason='Unapproved Skip')\n"
        "def test_skipped():\n"
        "    assert True\n"
    )
    rel_path = str(skip_file).replace("\\", "/")
    custom_gates = [("G_TEST_SKIP", "Skipped Gate", rel_path)]
    res = run_release_certification(custom_gates=custom_gates)
    assert res["verdict"] == "FAIL - GATE FAILURE"
    assert res["gate_results"][0]["status"] == "FAIL"

def test_positive_control_valid_gate_passes(temp_runner_environment):
    """7. Positive Control: Proves that a valid test case passes certification gate cleanly."""
    valid_file = temp_runner_environment / "test_valid.py"
    valid_file.write_text("def test_valid_pass():\n    assert True\n")
    rel_path = str(valid_file).replace("\\", "/")
    custom_gates = [("G_TEST_PASS", "Valid Gate Positive Control", rel_path)]
    res = run_release_certification(custom_gates=custom_gates)
    assert res["verdict"] == "PASS - PRODUCTION READY"
    assert res["passed_gates"] == 1
    assert res["failed_gates"] == 0
    assert res["gate_results"][0]["status"] == "PASS"
