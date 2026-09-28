"""
Zero-Trust Oracle Import Test for Phase 2E Shadbala.
"""
import ast
from pathlib import Path

def test_oracle_independence_shadbala():
    forbidden_modules = [
        "apps.api.engines.strength",
        "AshtakavargaEngine",
        "ShadbalaEngine",
        "StrengthEngine",
        "MasterworkEngine"
    ]

    oracle_dir = Path(__file__).parent

    for py_file in oracle_dir.rglob("*.py"):
        if py_file.name.startswith("test_"):
            continue

        with open(py_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(py_file))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for forbidden in forbidden_modules:
                        assert forbidden not in alias.name, f"Forbidden import '{forbidden}' found in {py_file.name}"
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for forbidden in forbidden_modules:
                    assert forbidden not in module, f"Forbidden import '{forbidden}' found in {py_file.name}"
                for alias in node.names:
                    for forbidden in forbidden_modules:
                        assert forbidden not in alias.name, f"Forbidden import '{forbidden}' found in {py_file.name}"
