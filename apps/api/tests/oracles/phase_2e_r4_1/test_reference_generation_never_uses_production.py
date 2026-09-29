"""
Phase 2E-R4.1 Reference Generation Production-Free Audit Test.
Statically verifies that reference dataset generators contain zero production engine imports.
"""
import ast
from pathlib import Path

def test_reference_generation_never_uses_production():
    forbidden_modules = [
        "apps.api.engines",
        "build_canonical_vedic_chart",
        "CanonicalVedicChart",
        "SkyfieldJPLProvider",
        "AstronomicalEngine",
        "VargaEngine",
        "ShadbalaEngine",
        "AshtakavargaEngine",
        "StrengthEngine"
    ]

    oracle_dir = Path(__file__).parent
    ref_scripts = [
        oracle_dir / "build_reference_dataset.py",
        oracle_dir / "build_synthetic_reference.py",
        oracle_dir / "generate_expected.py"
    ]

    for script_file in ref_scripts:
        if not script_file.exists():
            continue

        with open(script_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(script_file))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for forbidden in forbidden_modules:
                        assert forbidden not in alias.name, f"Forbidden import '{forbidden}' found in {script_file.name}"
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for forbidden in forbidden_modules:
                    assert forbidden not in module, f"Forbidden import '{forbidden}' found in {script_file.name}"
                for alias in node.names:
                    for forbidden in forbidden_modules:
                        assert forbidden not in alias.name, f"Forbidden import '{forbidden}' found in {script_file.name}"
