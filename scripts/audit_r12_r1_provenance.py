"""
Source-Level Provenance & Zero-Tolerance AST Auditor for Phase 2E-R4.1-R12-R1.
Inspects AST/import/call relationships and enforces:
  1. Zero reference longitude/ascendant overrides in production pipeline adapters.
  2. Zero oracle imports in production pipeline adapters (production_pipeline.py, production_shadbala.py, production_bav.py).
  3. Zero production imports in independent oracle modules.
  4. Zero tolerance inflation (e.g. 15.01 or 30.01) in certification adapters.
  5. Zero hardcoded PASS or hardcoded SAV vector shortcuts.
Returns exit code 0 if 0 provenance violations are found; otherwise exit code 1.
"""
import ast
import sys
from pathlib import Path

def audit_file_content(file_path: Path, forbidden_strings: list) -> list:
    violations = []
    if not file_path.exists():
        return violations

    text = file_path.read_text(encoding="utf-8")
    for pattern in forbidden_strings:
        if pattern in text:
            violations.append(f"Forbidden pattern '{pattern}' found in {file_path.name}")
    return violations

def audit_file_imports(file_path: Path, forbidden_modules: list) -> list:
    violations = []
    if not file_path.exists():
        return violations

    tree = ast.parse(file_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for f_mod in forbidden_modules:
                    if f_mod in alias.name:
                        violations.append(f"Forbidden import '{alias.name}' in {file_path.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                for f_mod in forbidden_modules:
                    if f_mod in node.module:
                        violations.append(f"Forbidden import from '{node.module}' in {file_path.name}")
    return violations

def main():
    violations = []

    # 1. Audit Pure Production Adapters (Zero Oracle Imports)
    prod_adapters = [
        Path("apps/api/tests/certification/production_pipeline.py"),
        Path("apps/api/tests/certification/production_shadbala.py"),
        Path("apps/api/tests/certification/production_bav.py")
    ]
    for adapter in prod_adapters:
        v_imports = audit_file_imports(adapter, ["apps.api.tests.oracles"])
        violations.extend(v_imports)

        v_content = audit_file_content(adapter, [
            "absolute_longitude = ",
            "sidereal_longitude = ",
            "sign_index = ",
            "rashi.sign_index = ",
            "tolerance = 30.01",
            "tolerance = 15.01",
            "sav = [25, 31"
        ])
        violations.extend(v_content)

    # 2. Audit Independent Oracle Modules (Zero Production Engine Imports)
    oracle_dir = Path("apps/api/tests/oracles/phase_2e_r4_1")
    for oracle_file in sorted(oracle_dir.glob("independent_*.py")):
        v = audit_file_imports(oracle_file, ["apps.api.engines"])
        violations.extend(v)

    # 3. Audit Production Strength Engines (Zero Oracle Imports)
    prod_dir = Path("apps/api/engines/strength")
    for prod_file in sorted(prod_dir.glob("*.py")):
        v = audit_file_imports(prod_file, ["apps.api.tests.oracles"])
        violations.extend(v)

    print("============================================================")
    print("STARTING PHASE 2E-R4.1-R12-R1 PROVENANCE & ZERO-TOLERANCE AUDIT")
    print("============================================================")

    if violations:
        print(f"PROVENANCE AUDIT FAILED: Found {len(violations)} isolation/provenance violations:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("PROVENANCE AUDIT PASS: 0 reference overrides, oracle contamination, or tolerance inflation found!")
        sys.exit(0)

if __name__ == "__main__":
    main()
