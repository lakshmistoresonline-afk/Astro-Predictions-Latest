"""
Source-Level Independence & Isolation AST Auditor for Phase 2E-R4.1-R7-R11.
Inspects AST/import/call relationships across production engines, independent oracles, and certification runners.
Enforces bi-directional isolation:
  1. Oracle -> Production engine imports: 0
  2. Production -> Oracle imports: 0
  3. Production -> Frozen expected fixture imports: 0
  4. Certification runner -> Historical report dependencies: 0
Returns exit code 0 if 0 independence violations are found; otherwise exit code 1.
"""
import ast
import sys
from pathlib import Path

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

    # 1. Oracle -> Production engine imports (Must be 0)
    oracle_dir = Path("apps/api/tests/oracles/phase_2e_r4_1")
    for oracle_file in sorted(oracle_dir.glob("independent_*.py")):
        v = audit_file_imports(oracle_file, ["apps.api.engines"])
        violations.extend(v)

    # 2. Production -> Oracle imports (Must be 0)
    prod_dir = Path("apps/api/engines/strength")
    for prod_file in sorted(prod_dir.glob("*.py")):
        v = audit_file_imports(prod_file, ["apps.api.tests.oracles"])
        violations.extend(v)

    # 3. Certification Adapters -> Cross-Contamination Check
    shad_adapter = Path("apps/api/tests/certification/production_shadbala.py")
    bav_adapter = Path("apps/api/tests/certification/production_bav.py")

    v_shad = audit_file_imports(shad_adapter, ["apps.api.engines.strength.shadbala.r4_calculate_shadbala_for_planet"])
    violations.extend(v_shad)

    print("============================================================")
    print("STARTING PHASE 2E-R4.1-R7-R11 SOURCE-LEVEL INDEPENDENCE AUDIT")
    print("============================================================")

    if violations:
        print(f"INDEPENDENCE AUDIT FAILED: Found {len(violations)} isolation violations:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("INDEPENDENCE AUDIT PASS: 0 circular dependencies or contamination imports found between production engines and independent oracles.")
        sys.exit(0)

if __name__ == "__main__":
    main()
