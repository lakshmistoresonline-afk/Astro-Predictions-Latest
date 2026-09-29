"""
Phase 2E-R4.1 Three-Way Oracle Validation Test Suite.
Verifies: Frozen Expected == R4.1 Independent Oracle == Production Engine Result.
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
from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4_1.independent_shadbala import r4_calculate_shadbala_for_planet
from apps.api.tests.oracles.phase_2e_r4_1.independent_ashtakavarga import r4_independent_bav, r4_independent_sav

def get_r4_1_fixture_files():
    fixture_dir = Path(__file__).parent.parent.parent / "fixtures" / "phase_2e_r4_1_expected"
    files = sorted(list(fixture_dir.glob("*.json")))
    return files

FIXTURES = get_r4_1_fixture_files()
FIXTURE_IDS = [f.stem for f in FIXTURES]

@pytest.mark.parametrize("fixture_path", FIXTURES, ids=FIXTURE_IDS)
def test_r4_1_three_way_validation(fixture_path):
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fid = data["fixture_id"]
    frozen_exp = data["expected"]

    synthetic_fids = ["REF_016", "REF_017", "REF_018", "REF_019", "REF_020"]

    # 1. Build Production Chart & Varga Suite
    if fid in synthetic_fids: # Synthetic boundary cases
        prod_chart = get_base_chart()
        asc_lon = data["ascendant_sidereal_longitude"]
        set_ascendant(prod_chart, asc_lon)
        prod_chart.mc.absolute_longitude = data["mc_sidereal_longitude"]

        for p_name, p_info in data["planets"].items():
            set_planet(prod_chart, p_name, p_info["longitude"])
            prod_chart.placements[p_name].velocity_deg_day = p_info["velocity_deg_day"]
            prod_chart.placements[p_name].retrograde = p_info["retrograde"]
    else: # Birth Profiles
        inp = BirthInput(
            name=data["name"],
            year=data["local_year"],
            month=data["local_month"],
            day=data["local_day"],
            hour=data["local_hour"],
            minute=data["local_minute"],
            second=0,
            timezone_str=data["timezone_str"],
            latitude=data["latitude"],
            longitude=data["longitude"]
        )
        prod_chart = build_canonical_vedic_chart(inp)

    varga_suite = VargaEngine.calculate_all_16_vargas(prod_chart)

    # 2. Build Independent Oracle Chart
    dt_str = data["birth_datetime_utc"]
    ind_chart = IndependentChart(
        data["ascendant_sidereal_longitude"],
        data["mc_sidereal_longitude"],
        data["ayanamsha"],
        data.get("julian_day", prod_chart.time_normalization.julian_day_tt),
        data.get("local_year", int(dt_str[:4])),
        data.get("local_month", int(dt_str[5:7])),
        data.get("local_day", int(dt_str[8:10])),
        data.get("local_hour", int(dt_str[11:13])),
        data.get("local_minute", int(dt_str[14:16]))
    )
    for p_name, p_info in data["planets"].items():
        ind_chart.add_planet(p_name, p_info["longitude"], p_info["velocity_deg_day"], p_info["retrograde"])

    # Execute Production Engines
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
        oracle_p = r4_calculate_shadbala_for_planet(ind_chart, p)
        prod_p = prod_shad_res.planets[p]

        # Sthana / Uccha
        assert abs(frozen_p["uccha"] - oracle_p["uccha"]) <= 0.03

        # Dig Bala
        assert abs(frozen_p["dig"] - oracle_p["dig"]) <= 0.03

        # Kala Bala
        assert abs(frozen_p["kala"] - oracle_p["kala"]) <= 0.03

        # Cheshta Bala
        assert abs(frozen_p["cheshta"] - oracle_p["cheshta"]) <= 0.03

        # Naisargika Bala
        assert abs(frozen_p["naisargika"] - oracle_p["naisargika"]) <= 0.03

        # Drik Bala
        assert abs(frozen_p["drik"] - oracle_p["drik"]) <= 0.03
