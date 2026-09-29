"""
Phase 2E-R4.1 Zero-Trust Oracle Independence & Runtime Isolation Test Suite.
"""
import ast
from pathlib import Path
import pytest

from apps.api.tests.oracles.phase_2e_r4_1.generate_expected import generate_frozen_expected_fixtures

class OracleContaminationError(Exception):
    pass

def test_r4_1_static_import_isolation():
    """
    Parses the AST of all Python files in phase_2e_r4_1 oracle package to verify
    zero imports of production engines or chart builders.
    """
    forbidden_modules = [
        "apps.api.engines",
        "ShadbalaEngine",
        "AshtakavargaEngine",
        "StrengthEngine",
        "MasterworkEngine",
        "CanonicalVedicChart",
        "build_canonical_vedic_chart",
        "VargaEngine"
    ]

    oracle_dir = Path(__file__).parent

    for py_file in oracle_dir.rglob("*.py"):
        if py_file.name.startswith("test_"):
            continue # Skip test execution wrappers

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

def test_r4_1_runtime_zero_trust_isolation(monkeypatch):
    """
    Monkey-patches production engine modules and chart builders with error stubs.
    Executes expected-value fixture generation to prove 100% runtime execution independence from production code.
    """
    import apps.api.engines.strength.shadbala as prod_shad
    import apps.api.engines.strength.ashtakavarga as prod_asht
    import apps.api.engines.vedic.chart_builder as prod_chart_builder
    import apps.api.engines.varga.engine as prod_varga

    def raise_contamination(*args, **kwargs):
        raise OracleContaminationError("Production engine was illegally called during expected value generation!")

    monkeypatch.setattr(prod_shad.ShadbalaEngine, "calculate_shadbala_suite", raise_contamination)
    monkeypatch.setattr(prod_asht.AshtakavargaEngine, "calculate_ashtakavarga", raise_contamination)
    monkeypatch.setattr(prod_chart_builder, "build_canonical_vedic_chart", raise_contamination)
    monkeypatch.setattr(prod_varga.VargaEngine, "calculate_all_16_vargas", raise_contamination)

    # Run expected fixture generator - MUST complete without calling any monkeypatched production engine!
    generate_frozen_expected_fixtures()
