"""
Independent Oracle Integration Tests for Phase 2E Ashtakavarga.
Executes the production AshtakavargaEngine and compares against independent expected BAV/SAV matrices.
"""
import pytest
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.strength import AshtakavargaEngine

from apps.api.tests.fixtures.phase_2d_r3.synthetic import get_base_chart, set_planet, set_ascendant
from apps.api.tests.oracles.phase_2e_ashtakavarga.chart_state import IndependentChart
from apps.api.tests.oracles.phase_2e_ashtakavarga.rules import independent_bav, independent_sav

def sync_charts(asc_lon, planets):
    ind_chart = IndependentChart(asc_lon)
    prod_chart = get_base_chart()
    set_ascendant(prod_chart, asc_lon)

    for name, lon in planets.items():
        ind_chart.add_planet(name, lon)
        set_planet(prod_chart, name, lon)

    return ind_chart, prod_chart

def test_ashtakavarga_oracle_subramanian():
    """Verify Canonical Subramanian BAV and SAV matrices against independent oracle."""
    # Build chart strictly from canonical birth input
    inp = BirthInput(
        name="Subramanian T S", year=1986, month=9, day=28,
        hour=16, minute=30, second=0, timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    prod_chart = build_canonical_vedic_chart(inp)

    ind_chart = IndependentChart(prod_chart.ascendant.absolute_longitude)
    for p_name, placement in prod_chart.placements.items():
        if p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            ind_chart.add_planet(p_name, placement.sidereal_longitude)

    res = AshtakavargaEngine.calculate_ashtakavarga(prod_chart)

    # 1. Total SAV is exactly 337
    assert res.sav.total == 337

    # 2. BAV match
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        ind_bav = independent_bav(ind_chart, p)
        prod_bav = res.bav[p].bindus
        assert ind_bav == prod_bav

    # 3. SAV match
    ind_sav = independent_sav(ind_chart)
    assert ind_sav == res.sav.bindus
    assert sum(ind_sav) == 337

def test_ashtakavarga_oracle_boundary_crossing():
    """Verify sign counting exactly at a 30° boundary."""
    # Ascendant at exactly 0.0°
    # Sun at exactly 30.0° (Taurus)
    # Moon at exactly 59.9999° (Taurus)
    ind, prod = sync_charts(0.0, {
        "Sun": 30.0, "Moon": 59.9999, "Mars": 0.0, "Mercury": 0.0,
        "Jupiter": 0.0, "Venus": 0.0, "Saturn": 0.0
    })

    res = AshtakavargaEngine.calculate_ashtakavarga(prod)
    ind_sav = independent_sav(ind)

    assert ind_sav == res.sav.bindus
    assert sum(ind_sav) == 337
