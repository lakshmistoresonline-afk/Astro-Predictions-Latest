"""
Zero-Trust Oracle Import Test.
Ensures that the independent rule oracles do not secretly import production rule engines.
"""
import ast
import os
from pathlib import Path

def test_oracle_independence():
    """
    Parses the AST of all Python files in the oracles directory to ensure
    no forbidden imports from production Yoga/Dosha engines exist.
    """
    forbidden_modules = [
        "apps.api.engines.yogas",
        "apps.api.engines.doshas",
        "YogaEvaluator",
        "DoshaEvaluator"
    ]

    oracle_dir = Path(__file__).parent

    for py_file in oracle_dir.rglob("*.py"):
        if py_file.name == "test_independence.py":
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

