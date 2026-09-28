"""
Phase 2E-R4 Zero-Trust Oracle Independence & Runtime Isolation Test.
"""
import ast
from pathlib import Path
import pytest

from apps.api.tests.oracles.phase_2e_r4.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4.independent_shadbala import r4_calculate_shadbala_for_planet
from apps.api.tests.oracles.phase_2e_r4.independent_ashtakavarga import r4_independent_bav, r4_independent_sav

class OracleContaminationError(Exception):
    pass

def test_r4_static_import_isolation():
    """
    Parses the AST of all Python files in phase_2e_r4 oracle directory to verify
    zero imports of production calculation modules.
    """
    forbidden_modules = [
        "apps.api.engines",
        "ShadbalaEngine",
        "AshtakavargaEngine",
        "StrengthEngine",
        "MasterworkEngine",
        "CanonicalVedicChart",
        "VargaEngine"
    ]

    oracle_dir = Path(__file__).parent

    for py_file in oracle_dir.rglob("*.py"):
        if py_file.name.startswith("test_"):
            continue # Skip test executor wrappers

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

def test_r4_runtime_zero_trust_isolation(monkeypatch):
    """
    Monkey-patches production engine classes with contamination stubs that throw hard errors.
    Executes the R4 independent oracle to prove 100% runtime execution independence.
    """
    import apps.api.engines.strength.shadbala as prod_shad
    import apps.api.engines.strength.ashtakavarga as prod_asht

    def raise_contamination(*args, **kwargs):
        raise OracleContaminationError("Production engine was illegally called during oracle execution!")

    monkeypatch.setattr(prod_shad.ShadbalaEngine, "calculate_shadbala_suite", raise_contamination)
    monkeypatch.setattr(prod_asht.AshtakavargaEngine, "calculate_ashtakavarga", raise_contamination)

    # Run independent oracle logic under monkeypatched environment
    chart = IndependentChart(321.43, 256.08, 23.85, 2451545.0, 1986, 9, 28, 16, 30)
    chart.add_planet("Sun", 161.54, 0.98, False)
    chart.add_planet("Moon", 80.0, 13.1, False)
    chart.add_planet("Mars", 298.0, 0.5, False)
    chart.add_planet("Mercury", 178.2, 1.2, False)
    chart.add_planet("Jupiter", 320.0, 0.08, False)
    chart.add_planet("Venus", 190.0, 1.2, False)
    chart.add_planet("Saturn", 230.0, 0.03, False)

    # These must complete successfully without triggering OracleContaminationError
    sun_shad = r4_calculate_shadbala_for_planet(chart, "Sun")
    assert sun_shad["total_shashtiamsas"] > 0

    sun_bav = r4_independent_bav(chart, "Sun")
    assert len(sun_bav) == 12

    sav = r4_independent_sav(chart)
    assert sum(sav) == 337
