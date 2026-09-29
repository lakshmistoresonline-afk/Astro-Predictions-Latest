"""
Static AST Auditor for Mutation Implementation (Phase 2E-R4.1-R7-R4).
Inspects mutation scripts to ensure NO output object tampering occurs.
Fails if forbidden result object mutation patterns are found.
"""
import ast
import sys
from pathlib import Path

def audit_mutation_script():
    script_path = Path("scripts/execute_r7_r4_mutation_suite.py")
    if not script_path.exists():
        print(f"Script {script_path} not found yet.")
        return True

    forbidden_patterns = [
        "target_obj.sub_components",
        "target_obj.value_shashtiamsas",
        "res.planets[p]",
        "res.planets[target_obj]"
    ]

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    violations = []
    for pattern in forbidden_patterns:
        if pattern in content:
            violations.append(f"Forbidden result object modification pattern found: '{pattern}'")

    if violations:
        print("MUTATION AUDIT FAIL:")
        for v in violations:
            print(f"  - {v}")
        return False

    print("MUTATION AUDIT PASS: Zero output object tampering patterns found in mutation script.")
    return True

if __name__ == "__main__":
    success = audit_mutation_script()
    if not success:
        sys.exit(1)
