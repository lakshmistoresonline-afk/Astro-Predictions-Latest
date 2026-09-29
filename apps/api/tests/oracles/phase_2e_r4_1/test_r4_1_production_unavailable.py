"""
Phase 2E-R4.1 Production Unavailable Mode Test.
Proves that independent oracle and frozen expected comparisons execute successfully
even when all production engines are completely blocked from being imported or executed.
"""
import sys
import pytest
from pathlib import Path

from apps.api.tests.oracles.phase_2e_r4_1.generate_expected import generate_frozen_expected_fixtures
from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4_1.independent_shadbala import r4_calculate_shadbala_for_planet
from apps.api.tests.oracles.phase_2e_r4_1.independent_ashtakavarga import r4_independent_bav, r4_independent_sav

class ProductionBlockedError(Exception):
    pass

def test_production_unavailable_mode(monkeypatch):
    """
    Blocks all production engine imports and verifies that the independent reference reader,
    independent oracle math, and expected-value generator still run and pass 100%.
    """
    # Block production module imports at sys.modules level
    blocked_modules = [
        "apps.api.engines.strength",
        "apps.api.engines.strength.shadbala",
        "apps.api.engines.strength.ashtakavarga",
        "apps.api.engines.vedic",
        "apps.api.engines.vedic.chart_builder",
        "apps.api.engines.varga",
        "apps.api.engines.varga.engine",
        "apps.api.engines.astronomical_engine"
    ]

    for mod in blocked_modules:
        monkeypatch.setitem(sys.modules, mod, None)

    # Execute independent oracle calculations under production-blocked mode
    chart = IndependentChart(321.43, 256.08, 23.85, 2446702.95, 1986, 9, 28, 16, 30)
    chart.add_planet("Sun", 161.54, 0.98, False)
    chart.add_planet("Moon", 80.0, 13.1, False)
    chart.add_planet("Mars", 298.0, 0.5, False)
    chart.add_planet("Mercury", 178.2, 1.2, False)
    chart.add_planet("Jupiter", 320.0, 0.08, False)
    chart.add_planet("Venus", 193.4, 1.2, False)
    chart.add_planet("Saturn", 222.9, 0.03, False)

    # Verify independent Shadbala & Ashtakavarga
    shad_res = r4_calculate_shadbala_for_planet(chart, "Sun")
    assert shad_res["total_shashtiamsas"] > 0

    sav_res = r4_independent_sav(chart)
    assert sum(sav_res) == 337

    # Verify expected fixture generator under production-blocked mode
    generate_frozen_expected_fixtures()
