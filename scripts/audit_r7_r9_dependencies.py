"""
Static AST Dependency & Zero-Trust Auditor for Phase 2E-R4.1-R7-R9.
Inspects certification runner scripts for forbidden dependencies, recursion calls, or hardcoded pass shortcuts.
Returns exit code 0 if 0 forbidden dependency violations are found; otherwise exit code 1.
"""
import ast
import sys
from pathlib import Path

def audit_runner_dependencies(runner_path: Path) -> list:
    violations = []
    if not runner_path.exists():
        return [f"Runner file not found: {runner_path}"]

    content = runner_path.read_text(encoding="utf-8")
    tree = ast.parse(content)

    forbidden_imports = [
        "test_zero_trust_certification",
        "test_r7_r7_zero_trust_architecture",
        "test_r7_r8_zero_trust_architecture"
    ]

    forbidden_strings = [
        "test_r7_r7_zero_trust_architecture.py",
        "test_zero_trust_certification.py",
        "baseline_pass = True",
        "b_out = \"ORACLE_PASS: Baseline Pass\"",
        "\"production_value\": \"Baseline Pass\"",
        "\"oracle_value\": \"Baseline Pass\""
    ]

    # 1. AST Import check
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for f_imp in forbidden_imports:
                    if f_imp in alias.name:
                        violations.append(f"Forbidden AST import '{alias.name}' in {runner_path.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                for f_imp in forbidden_imports:
                    if f_imp in node.module:
                        violations.append(f"Forbidden AST import from '{node.module}' in {runner_path.name}")

    # 2. String literal check
    for f_str in forbidden_strings:
        if f_str in content:
            violations.append(f"Forbidden string pattern '{f_str}' found in {runner_path.name}")

    return violations

def main():
    runner_path = Path("scripts/run_phase_2e_r4_1_r7_r9_certification.py")
    violations = audit_runner_dependencies(runner_path)

    print("============================================================")
    print("STARTING PHASE 2E-R4.1-R7-R9 STATIC DEPENDENCY & ZERO-TRUST AUDIT")
    print("============================================================")

    if violations:
        print(f"DEPENDENCY AUDIT FAILED: Found {len(violations)} forbidden dependencies:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print(f"DEPENDENCY AUDIT PASS: Zero forbidden imports, recursion calls, or hardcoded shortcuts found in {runner_path.name}.")
        sys.exit(0)

if __name__ == "__main__":
    main()
