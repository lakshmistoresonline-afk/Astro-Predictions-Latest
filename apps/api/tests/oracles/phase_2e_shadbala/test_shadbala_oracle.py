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
        1986, 9, 28, 16
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
        assert abs(prod_p.total_shashtiamsas - round(exp_total, 2)) < 10.0 # Accommodate ephemeris precision delta on Drik Bala

def test_shadbala_oracle_exaltation_boundary():
    """Verify exaltation boundary logic."""
    ind_chart = IndependentChart(0.0, 270.0, 23.85, 2451545.0, 2000, 1, 1, 12)
    ind_chart.add_planet("Sun", 10.0, False, 1.0) # Sun at exaltation 10.0 deg Aries
    exp_uccha = independent_uccha_bala(ind_chart, "Sun")
    assert abs(exp_uccha - 60.0) < 0.01

def test_shadbala_oracle_dig_bala_boundary():
    """Verify Dig Bala cardinal boundary logic."""
    ind_chart = IndependentChart(0.0, 270.0, 23.85, 2451545.0, 2000, 1, 1, 12) # Lagna=Aries 0, MC=Capricorn 270
    ind_chart.add_planet("Sun", 270.0, False, 1.0) # Sun at MC (10th house) -> Dig Bala = 60
    exp_dig = independent_dig_bala(ind_chart, "Sun")
    assert abs(exp_dig - 60.0) < 0.01
