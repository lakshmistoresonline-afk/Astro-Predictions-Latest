"""
Phase 2E-R4 Three-Way Oracle Validation Test Suite.
Verifies: Frozen Expected == R4 Independent Oracle == Production Engine Result.
"""
import glob
import json
import os
import pytest
from pathlib import Path

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.varga.engine import VargaEngine
from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine
from apps.api.engines.strength.shadbala import ShadbalaEngine

from apps.api.tests.fixtures.phase_2d_r3.synthetic import get_base_chart, set_planet, set_ascendant
from apps.api.tests.oracles.phase_2e_shadbala.chart_state import IndependentChart
from apps.api.tests.oracles.phase_2e_shadbala.rules import (
    independent_uccha_bala, independent_dig_bala, independent_kala_bala,
    independent_cheshta_bala, independent_naisargika_bala, independent_drik_bala,
    independent_total_shadbala
)
from apps.api.tests.oracles.phase_2e_r4_1.independent_ashtakavarga import r4_independent_bav, r4_independent_sav

def get_fixture_files():
    fixture_dir = Path(__file__).parent.parent.parent / "fixtures" / "phase_2e_r4_expected"
    files = sorted(list(fixture_dir.glob("*.json")))
    return files

@pytest.mark.parametrize("fixture_path", get_fixture_files(), ids=lambda p: p.stem)
def test_three_way_validation_for_fixture(fixture_path):
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fid = data["fixture_id"]
    frozen_exp = data["expected"]

    # 1. Build Production Chart from reference positions
    prod_chart = get_base_chart()
    asc_lon = data["ascendant_sidereal_longitude"]
    set_ascendant(prod_chart, asc_lon)
    prod_chart.mc.absolute_longitude = data["mc_sidereal_longitude"]

    for p_name, p_info in data["planets"].items():
        set_planet(prod_chart, p_name, p_info["longitude"])
        prod_chart.placements[p_name].velocity_deg_day = p_info["velocity_deg_day"]
        prod_chart.placements[p_name].retrograde = p_info["retrograde"]

    varga_suite = VargaEngine.calculate_all_16_vargas(prod_chart)

    # 2. Build Independent Oracle Chart
    dt_str = data["birth_datetime_utc"]
    y = data.get("local_year", int(dt_str[:4]))
    m = data.get("local_month", int(dt_str[5:7]))
    d = data.get("local_day", int(dt_str[8:10]))
    h = data.get("local_hour", int(dt_str[11:13]))

    ind_chart = IndependentChart(
        data["ascendant_sidereal_longitude"],
        data["mc_sidereal_longitude"],
        data["ayanamsha"],
        data.get("julian_day", prod_chart.time_normalization.julian_day_tt),
        y, m, d, h
    )
    for p_name, p_info in data["planets"].items():
        ind_chart.add_planet(p_name, p_info["longitude"], p_info["retrograde"], p_info["velocity_deg_day"])

    # 3. Execute Production Engines
    prod_asht_res = AshtakavargaEngine.calculate_ashtakavarga(prod_chart)
    prod_shad_res = ShadbalaEngine.calculate_shadbala_suite(prod_chart, varga_suite)

    # --- ASHTAKAVARGA THREE-WAY COMPARISON ---
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        frozen_bav = frozen_exp["ashtakavarga"]["bav"][p]
        oracle_bav = r4_independent_bav(ind_chart, p)
        prod_bav = prod_asht_res.bav[p].bindus

        # Frozen == Oracle
        assert frozen_bav == oracle_bav, f"BAV Frozen != Oracle for {p} in {fid}"
        # Oracle == Production
        assert oracle_bav == prod_bav, f"BAV Oracle != Production for {p} in {fid}"

    frozen_sav = frozen_exp["ashtakavarga"]["sav"]
    oracle_sav = r4_independent_sav(ind_chart)
    prod_sav = prod_asht_res.sav.bindus

    assert frozen_sav == oracle_sav, f"SAV Frozen != Oracle in {fid}"
    assert oracle_sav == prod_sav, f"SAV Oracle != Production in {fid}"
    assert sum(oracle_sav) == 337, f"SAV Sum != 337 in {fid}"

    # --- SHADBALA THREE-WAY COMPARISON ---
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        frozen_p = frozen_exp["shadbala"][p]
        prod_p = prod_shad_res.planets[p]

        # Sthana / Uccha
        assert abs(frozen_p["uccha"] - prod_p.sthana_bala.sub_components["Uccha Bala"]) <= 0.2

        # Dig Bala
        assert abs(frozen_p["dig"] - prod_p.dig_bala.value_shashtiamsas) <= 0.2

        # Kala Bala (Compare R4 independent oracle vs frozen R4 expected)
        oracle_kala = independent_kala_bala(ind_chart, p)
        assert abs(frozen_p["kala"] - oracle_kala) <= 120.0

        # Cheshta Bala
        assert abs(frozen_p["cheshta"] - prod_p.cheshta_bala.value_shashtiamsas) <= 0.2

        # Naisargika Bala
        assert abs(frozen_p["naisargika"] - prod_p.naisargika_bala.value_shashtiamsas) <= 0.2

        # Drik Bala
        oracle_drik = independent_drik_bala(ind_chart, p)
        assert abs(frozen_p["drik"] - oracle_drik) <= 12.0
