"""
Single Mutation Case Validator Subprocess for Phase 2E-R4.1-R7-R6.
Executed in a fresh, isolated Python process for each mutation.
Evaluates production engine vs independent oracle.
Fast synthetic chart construction (under 0.005s per process).
Output Statuses:
  - ORACLE_PASS (Exit 0): Production calculation succeeded and matched independent oracle.
  - ORACLE_MISMATCH (Exit 1): Production calculation succeeded normally, but value differed from independent oracle.
  - PRODUCTION_EXCEPTION (Exit 2): Production engine crashed or raised an exception/syntax error during calculation.
  - VALIDATOR_ERROR (Exit 3): Command-line argument or test runner invocation error.
"""
import json
import sys
import traceback
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.api.tests.fixtures.phase_2d_r3.synthetic import get_base_chart, set_planet, set_ascendant
from apps.api.engines.varga.engine import VargaEngine

from apps.api.tests.oracles.phase_2e_r4_1.independent_chart import IndependentChart
from apps.api.tests.oracles.phase_2e_r4_1.independent_shadbala import r4_calculate_shadbala_for_planet
from apps.api.tests.oracles.phase_2e_r4_1.independent_ashtakavarga import r4_independent_bav

def extract_subcomponent_num(planet_obj, bala_cat, sub_comp):
    obj = getattr(planet_obj, bala_cat)
    if hasattr(obj, 'sub_components') and sub_comp in obj.sub_components:
        return obj.sub_components[sub_comp]
    return obj.value_shashtiamsas

def evaluate_single_fixture(fixture_path: Path, mode: str, planet: str, cat_or_contrib: str, subcomp: str) -> str:
    # Deferred imports to catch syntax errors during mutated file imports
    from apps.api.engines.strength.shadbala import ShadbalaEngine
    from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Build fast production chart
    chart = get_base_chart()
    chart.calculation_hash = f"HASH_{data['fixture_id']}"
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

    varga_suite = VargaEngine.calculate_all_16_vargas(chart)

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
        prod_shad = ShadbalaEngine.calculate_shadbala_suite(chart, varga_suite)
        prod_val = extract_subcomponent_num(prod_shad.planets[planet], cat_or_contrib, subcomp)

        oracle_shad = r4_calculate_shadbala_for_planet(ind_chart, planet)
        oracle_val = oracle_shad[subcomp]

        delta = abs(prod_val - oracle_val)
        if delta <= 0.03:
            return f"ORACLE_PASS: Prod {prod_val:.2f} == Oracle {oracle_val:.2f}"
        else:
            return f"ORACLE_MISMATCH: Prod {prod_val:.2f} != Oracle {oracle_val:.2f} (Delta: {delta:.4f})"

    elif mode == "bav":
        prod_asht = AshtakavargaEngine.calculate_ashtakavarga(chart)
        prod_bav = prod_asht.bav[planet].bindus

        oracle_bav = r4_independent_bav(ind_chart, planet)

        if prod_bav == oracle_bav:
            return f"ORACLE_PASS: BAV {planet} Prod {prod_bav} == Oracle {oracle_bav}"
        else:
            return f"ORACLE_MISMATCH: BAV {planet} Prod {prod_bav} != Oracle {oracle_bav}"

    else:
        return f"VALIDATOR_ERROR: Unknown mode {mode}"

def main():
    if len(sys.argv) < 5:
        print("VALIDATOR_ERROR: Missing command-line arguments")
        sys.exit(3)

    mode = sys.argv[1]
    planet = sys.argv[2]
    cat_or_contrib = sys.argv[3]
    subcomp = sys.argv[4]

    ref_path = Path("apps/api/tests/fixtures/phase_2e_r4_1_expected/REF_001.json")

    try:
        res_msg = evaluate_single_fixture(ref_path, mode, planet, cat_or_contrib, subcomp)
        if "ORACLE_MISMATCH" in res_msg:
            print(f"ORACLE_MISMATCH: {res_msg}")
            sys.exit(1)
        elif "ORACLE_PASS" in res_msg:
            print(f"ORACLE_PASS: {res_msg}")
            sys.exit(0)
        else:
            print(res_msg)
            sys.exit(3)

    except Exception as e:
        err_str = "".join(traceback.format_exception(e))
        print(f"PRODUCTION_EXCEPTION: {e}\n{err_str}")
        sys.exit(2)

if __name__ == "__main__":
    main()
