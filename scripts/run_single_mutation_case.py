"""
Single Mutation Case Validator Subprocess for Phase 2E-R4.1-R7-R8.
Executed in a fresh, isolated Python process for each mutation on a specific fixture.
CLI Usage:
  python run_single_mutation_case.py <mode> <fixture_id> <planet> <cat_or_contrib> <subcomp> [module_override]

Output Statuses:
  - ORACLE_PASS (Exit 0): Production calculation succeeded and matched independent oracle.
  - ORACLE_MISMATCH (Exit 1): Production calculation succeeded normally, but value differed from independent oracle.
  - PRODUCTION_EXCEPTION (Exit 2): Production engine crashed or raised an exception/syntax error.
  - FIXTURE_NOT_FOUND / VALIDATOR_ERROR (Exit 3): Requested fixture does not exist or missing arguments.
"""
import json
import importlib
import sys
import traceback
from pathlib import Path
from unittest.mock import MagicMock

# Disable Python bytecode caching to prevent stale .pyc import cache collisions
sys.dont_write_bytecode = True

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Block Skyfield JPL DE440s BSP kernel disk load to achieve ultra-fast process startup time
sys.modules["skyfield"] = MagicMock()
sys.modules["skyfield.api"] = MagicMock()
sys.modules["apps.api.engines.astronomy.provider"] = MagicMock()

from apps.api.tests.fixtures.phase_2d_r3.synthetic import get_base_chart, set_planet, set_ascendant
from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart

def extract_subcomponent_num(planet_obj, bala_cat, sub_comp):
    obj = getattr(planet_obj, bala_cat)
    if hasattr(obj, 'sub_components') and sub_comp in obj.sub_components:
        return obj.sub_components[sub_comp]
    return obj.value_shashtiamsas

def evaluate_fixture(fixture_path: Path, mode: str, planet: str, cat_or_contrib: str, subcomp: str, module_override: str = None) -> dict:
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fid = data.get("fixture_id", fixture_path.stem)

    # Build fast production chart
    chart = get_base_chart()
    chart.calculation_hash = f"HASH_{fid}"
    chart.input_data.year = data["local_year"]
    chart.input_data.month = data["local_month"]
    chart.input_data.day = data["local_day"]
    chart.input_data.hour = data["local_hour"]
    chart.input_data.minute = data["local_minute"]
    chart.time_normalization.julian_day_tt = data["julian_day"]

    set_ascendant(chart, data["ascendant_sidereal_longitude"])
    chart.mc.absolute_longitude = data["mc_sidereal_longitude"]
    chart.ayanamsha_value_deg = data["ayanamsha"]

    for p_name, p_info in data["planets"].items():
        set_planet(chart, p_name, p_info["longitude"])
        chart.placements[p_name].velocity_deg_day = p_info["velocity_deg_day"]
        chart.placements[p_name].retrograde = p_info["retrograde"]

    # Build independent oracle chart
    dt_str = data["birth_datetime_utc"]
    ind_chart = IndependentChart(
        data["ascendant_sidereal_longitude"],
        data["mc_sidereal_longitude"],
        data["ayanamsha"],
        data.get("julian_day", 2446702.145833),
        data.get("local_year", int(dt_str[:4])),
        data.get("local_month", int(dt_str[5:7])),
        data.get("local_day", int(dt_str[8:10])),
        data.get("local_hour", int(dt_str[11:13]))
    )
    for p_name, p_info in data["planets"].items():
        ind_chart.add_planet(p_name, p_info["longitude"], p_info["velocity_deg_day"], p_info["retrograde"])

    if mode == "shadbala":
        from apps.api.engines.varga.engine import VargaEngine
        from apps.api.tests.oracles.phase_2e_r4_1.independent_shadbala import r4_calculate_shadbala_for_planet

        if module_override:
            shad_mod = importlib.import_module(module_override)
            importlib.reload(shad_mod)
            ShadbalaEngine = shad_mod.ShadbalaEngine
        else:
            from apps.api.engines.strength.shadbala import ShadbalaEngine

        varga_suite = VargaEngine.calculate_all_16_vargas(chart)
        prod_shad = ShadbalaEngine.calculate_shadbala_suite(chart, varga_suite)
        prod_val = extract_subcomponent_num(prod_shad.planets[planet], cat_or_contrib, subcomp)

        oracle_shad = r4_calculate_shadbala_for_planet(ind_chart, planet)
        oracle_val = oracle_shad[subcomp]

        delta = abs(prod_val - oracle_val)
        status = "ORACLE_PASS" if delta <= 0.03 else "ORACLE_MISMATCH"

        return {
            "fixture_id": fid,
            "mode": mode,
            "planet": planet,
            "subcomponent": subcomp,
            "production_value": round(prod_val, 4),
            "oracle_value": round(oracle_val, 4),
            "delta": round(delta, 4),
            "status": status
        }

    elif mode == "bav":
        from apps.api.tests.oracles.phase_2e_r4_1.independent_ashtakavarga import r4_independent_bav

        if module_override:
            asht_mod = importlib.import_module(module_override)
            importlib.reload(asht_mod)
            AshtakavargaEngine = asht_mod.AshtakavargaEngine
        else:
            from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine

        prod_asht = AshtakavargaEngine.calculate_ashtakavarga(chart)
        prod_bav = prod_asht.bav[planet].bindus

        oracle_bav = r4_independent_bav(ind_chart, planet)

        status = "ORACLE_PASS" if prod_bav == oracle_bav else "ORACLE_MISMATCH"

        return {
            "fixture_id": fid,
            "mode": mode,
            "planet": planet,
            "contributor": cat_or_contrib,
            "production_value": prod_bav,
            "oracle_value": oracle_bav,
            "delta": 0 if prod_bav == oracle_bav else 1,
            "status": status
        }

    else:
        return {
            "fixture_id": fid,
            "mode": mode,
            "status": "VALIDATOR_ERROR",
            "message": f"Unknown mode {mode}"
        }

def main():
    if len(sys.argv) < 6:
        print(json.dumps({"status": "VALIDATOR_ERROR", "message": "Missing command-line arguments. Usage: python run_single_mutation_case.py <mode> <fixture_id> <planet> <cat_or_contrib> <subcomp> [module_override]"}))
        sys.exit(3)

    mode = sys.argv[1]
    fixture_id = sys.argv[2]
    planet = sys.argv[3]
    cat_or_contrib = sys.argv[4]
    subcomp = sys.argv[5]
    module_override = sys.argv[6] if len(sys.argv) > 6 else None

    # Locate exact requested fixture file
    ref_dir = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected")
    fixture_path = ref_dir / f"{fixture_id}.json"

    if not fixture_path.exists():
        print(json.dumps({"status": "FIXTURE_NOT_FOUND", "message": f"Requested fixture {fixture_id} not found at {fixture_path}"}))
        sys.exit(3)

    try:
        res = evaluate_fixture(fixture_path, mode, planet, cat_or_contrib, subcomp, module_override)
        print(json.dumps(res))

        if res["status"] == "ORACLE_PASS":
            sys.exit(0)
        elif res["status"] == "ORACLE_MISMATCH":
            sys.exit(1)
        else:
            sys.exit(3)

    except Exception as e:
        err_str = "".join(traceback.format_exception(e))
        res = {
            "fixture_id": fixture_id,
            "mode": mode,
            "planet": planet,
            "status": "PRODUCTION_EXCEPTION",
            "exception": str(e),
            "traceback": err_str
        }
        print(json.dumps(res))
        sys.exit(2)

if __name__ == "__main__":
    main()
