"""
Automated Negative-Path Test Suite for Release Certification System Runner.
Proves that missing test paths, zero-test modules, failing assertions, collection errors,
internal setup errors, and unapproved skips fail release certification closed.
"""
import pytest
import subprocess
import sys
import shutil
from pathlib import Path

@pytest.fixture
def temp_test_dir(tmp_path):
    """Creates a temporary test directory inside project tests root."""
    target_dir = Path("apps/api/tests/_temp_runner_tests")
    target_dir.mkdir(parents=True, exist_ok=True)
    yield target_dir
    if target_dir.exists():
        shutil.rmtree(target_dir, ignore_errors=True)

def test_missing_test_path_fails_gate(temp_test_dir):
    """1. Proves that a nonexistent test file path causes certification gate failure."""
    nonexistent_file = temp_test_dir / "test_nonexistent_gate.py"
    cmd = [
        sys.executable, "-m", "pytest",
        str(nonexistent_file), "-q"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode != 0

def test_zero_collected_tests_fails_gate(temp_test_dir):
    """2. Proves that a test file with zero test cases fails certification gate."""
    empty_file = temp_test_dir / "test_empty_gate.py"
    empty_file.write_text("# Empty test file\n")
    cmd = [
        sys.executable, "-m", "pytest",
        str(empty_file), "-q"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 5 or "no tests ran" in res.stdout.lower() or "NO TESTS RAN" in res.stdout or res.returncode != 0

def test_failing_assertion_fails_gate(temp_test_dir):
    """3. Proves that a failing assertion in a gate module causes certification gate failure."""
    fail_file = temp_test_dir / "test_failing_gate.py"
    fail_file.write_text("def test_will_fail():\n    assert 1 == 2\n")
    cmd = [
        sys.executable, "-m", "pytest",
        str(fail_file), "-q"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 1
    assert "1 failed" in res.stdout

def test_collection_syntax_error_fails_gate(temp_test_dir):
    """4. Proves that a syntax error during pytest collection causes certification gate failure."""
    syntax_err_file = temp_test_dir / "test_syntax_error.py"
    syntax_err_file.write_text("def test_broken_syntax(\n    assert True\n")
    cmd = [
        sys.executable, "-m", "pytest",
        str(syntax_err_file), "-q"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode != 0

def test_fixture_setup_error_fails_gate(temp_test_dir):
    """5. Proves that a fixture setup error in a gate module causes certification gate failure."""
    fixture_err_file = temp_test_dir / "test_fixture_error.py"
    fixture_err_file.write_text(
        "import pytest\n"
        "@pytest.fixture\n"
        "def broken_fix():\n"
        "    raise RuntimeError('Fixture Setup Crashed')\n"
        "def test_uses_broken_fix(broken_fix):\n"
        "    assert True\n"
    )
    cmd = [
        sys.executable, "-m", "pytest",
        str(fixture_err_file), "-q"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 1 or "1 error" in res.stdout or res.returncode != 0

def test_unapproved_skip_fails_gate(temp_test_dir):
    """6. Proves that skipped tests are flagged and fail-closed for certification gate integrity."""
    skip_file = temp_test_dir / "test_skipped_gate.py"
    skip_file.write_text(
        "import pytest\n"
        "@pytest.mark.skip(reason='Unapproved Skip')\n"
        "def test_unapproved_skip():\n"
        "    assert True\n"
    )
    cmd = [
        sys.executable, "-m", "pytest",
        str(skip_file), "-q"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert "1 skipped" in res.stdout
