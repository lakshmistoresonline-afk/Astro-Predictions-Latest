"""
Independent Oracle Integration Tests for Phase 2E Shadbala.
"""
import pytest
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.varga.engine import VargaEngine
from apps.api.engines.strength import ShadbalaEngine

from apps.api.tests.fixtures.phase_2d_r3.synthetic import get_base_chart, set_planet, set_ascendant
from apps.api.tests.oracles.phase_2e_shadbala.chart_state import IndependentChart
from apps.api.tests.oracles.phase_2e_shadbala.rules import (
    independent_uccha_bala, independent_dig_bala, independent_kala_bala,
    independent_cheshta_bala, independent_naisargika_bala, independent_drik_bala,
    independent_total_shadbala
)

def sync_charts(asc_lon, planets):
    ind_chart = IndependentChart(asc_lon, (asc_lon - 90) % 360.0, 23.85)
    prod_chart = get_base_chart()
    set_ascendant(prod_chart, asc_lon)
    prod_chart.mc.absolute_longitude = (asc_lon - 90) % 360.0

    for name, data in planets.items():
        lon = data["lon"]
        retro = data.get("retro", False)
        vel = data.get("vel", 1.0)
        ind_chart.add_planet(name, lon, retro, vel)
        set_planet(prod_chart, name, lon)
        prod_chart.placements[name].retrograde = retro
        prod_chart.placements[name].velocity_deg_day = vel

    return ind_chart, prod_chart

def test_shadbala_oracle_subramanian():
    """Verify Canonical Subramanian Shadbala against independent oracle."""
    inp = BirthInput(
        name="Subramanian T S", year=1986, month=9, day=28,
        hour=16, minute=30, second=0, timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )
    prod_chart = build_canonical_vedic_chart(inp)
    varga_suite = VargaEngine.calculate_all_16_vargas(prod_chart)

    ind_chart = IndependentChart(
        prod_chart.ascendant.absolute_longitude,
        prod_chart.mc.absolute_longitude,
        prod_chart.ayanamsha_value_deg,
        prod_chart.time_normalization.julian_day_tt,
        1986, 9, 16
    )
    for p_name, placement in prod_chart.placements.items():
        if p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            ind_chart.add_planet(p_name, placement.sidereal_longitude, placement.retrograde, placement.velocity_deg_day)

    res = ShadbalaEngine.calculate_shadbala_suite(prod_chart, varga_suite)

    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        prod_p = res.planets[p]

        # Sthana (Uccha)
        exp_uccha = independent_uccha_bala(ind_chart, p)
        assert abs(prod_p.sthana_bala.sub_components["Uccha Bala"] - round(exp_uccha, 2)) < 0.02

        # Dig
        exp_dig = independent_dig_bala(ind_chart, p)
        assert abs(prod_p.dig_bala.value_shashtiamsas - round(exp_dig, 2)) < 0.02

        # Kala
        exp_kala = independent_kala_bala(ind_chart, p)
        assert abs(prod_p.kala_bala.value_shashtiamsas - round(exp_kala, 2)) < 0.02

        # Cheshta
        exp_cheshta = independent_cheshta_bala(ind_chart, p)
        assert abs(prod_p.cheshta_bala.value_shashtiamsas - round(exp_cheshta, 2)) < 0.02

        # Naisargika
        exp_naisargika = independent_naisargika_bala(ind_chart, p)
        assert abs(prod_p.naisargika_bala.value_shashtiamsas - round(exp_naisargika, 2)) < 0.02

        # Total
        exp_total = independent_total_shadbala(ind_chart, p, varga_suite)
        assert abs(prod_p.total_shashtiamsas - round(exp_total, 2)) < 0.02

def test_shadbala_oracle_exaltation_boundary():
    """Verify Uccha Bala strictly at exact debilitation point."""
    ind, prod = sync_charts(0.0, {
        "Sun": {"lon": 190.0}, # Libra 10 = exact debilitation
        "Moon": {"lon": 0.0},
        "Mars": {"lon": 0.0},
        "Mercury": {"lon": 0.0},
        "Jupiter": {"lon": 0.0},
        "Venus": {"lon": 0.0},
        "Saturn": {"lon": 0.0}
    })

    varga_suite = VargaEngine.calculate_all_16_vargas(prod)
    res = ShadbalaEngine.calculate_shadbala_suite(prod, varga_suite)

    # Sun should have 0 Uccha Bala
    assert res.planets["Sun"].sthana_bala.sub_components["Uccha Bala"] == 0.0

def test_shadbala_oracle_dig_bala_boundary():
    """Verify Dig Bala at exact power house and opposite house."""
    ind, prod = sync_charts(0.0, { # Aries Ascendant
        "Sun": {"lon": 270.0}, # Capricorn = 10th House = Full Dig Bala for Sun
        "Mars": {"lon": 90.0}, # Cancer = 4th House = Zero Dig Bala for Mars
        "Moon": {"lon": 0.0},
        "Mercury": {"lon": 0.0},
        "Jupiter": {"lon": 0.0},
        "Venus": {"lon": 0.0},
        "Saturn": {"lon": 0.0}
    })

    varga_suite = VargaEngine.calculate_all_16_vargas(prod)
    res = ShadbalaEngine.calculate_shadbala_suite(prod, varga_suite)

    assert res.planets["Sun"].dig_bala.value_shashtiamsas == 60.0
    assert res.planets["Mars"].dig_bala.value_shashtiamsas == 0.0
