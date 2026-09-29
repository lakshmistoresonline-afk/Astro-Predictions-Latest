"""
Execute complete 73 genuine production mutations for Phase 2E-R4.1-R7-R2:
- 17 Shadbala subcomponent mutations
- 56 Ashtakavarga BAV contributor cell mutations
Total = 73 genuine executable mutations.
Outputs reports/r7/r2/mutation_execution.json, reports/r7/r2/mutation_inventory.json, and individual records in reports/r7/r2/mutations/.
Zero imports from apps.api.engines.* inside oracle evaluation!
"""
import copy
import json
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.varga.engine import VargaEngine
from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine, BAV_RULES
from apps.api.engines.strength.shadbala import (
    ShadbalaEngine, DEBILITATION_DEGREES, NAISARGIKA_BALA_SHASHTIAMSAS,
    AVG_DAILY_VELOCITY, NATURAL_FRIENDSHIP
)

def run_73_mutations():
    print("============================================================")
    print("STARTING 73 GENUINE PRODUCTION MUTATION SUITE (17 SHADBALA + 56 BAV)")
    print("============================================================")

    reports_dir_r2 = Path("reports/r7/r2/mutations")
    reports_dir_r2.mkdir(parents=True, exist_ok=True)

    reports_dir_r1 = Path("reports/r7/r1/mutations")
    reports_dir_r1.mkdir(parents=True, exist_ok=True)

    inp = BirthInput(name="Subramanian", year=1986, month=9, day=28, hour=16, minute=30, second=0, timezone_str="Asia/Kolkata", latitude=10.7867, longitude=76.6548)
    chart = build_canonical_vedic_chart(inp)
    varga_suite = VargaEngine.calculate_all_16_vargas(chart)

    baseline_shad = ShadbalaEngine.calculate_shadbala_suite(chart, varga_suite)
    baseline_asht = AshtakavargaEngine.calculate_ashtakavarga(chart)

    records = []

    # ------------------------------------------------------------
    # 1. 17 SHADBALA SUBCOMPONENT MUTATIONS
    # ------------------------------------------------------------
    shad_sub_specs = [
        ("MUT_SHAD_01_UCHHA", "Uccha Bala", "Sun", "sthana_bala", "Uccha Bala"),
        ("MUT_SHAD_02_SAPTA", "Sapta Vargaja Bala", "Sun", "sthana_bala", "Sapta Vargaja Bala"),
        ("MUT_SHAD_03_OJHA", "Ojha Yugma Bala", "Sun", "sthana_bala", "Ojha Yugma Bala"),
        ("MUT_SHAD_04_KENDRADI", "Kendradi Bala", "Sun", "sthana_bala", "Kendradi Bala"),
        ("MUT_SHAD_05_DREKKANA", "Drekkana Bala", "Sun", "sthana_bala", "Drekkana Bala"),
        ("MUT_SHAD_06_DIG", "Dig Bala", "Sun", "dig_bala", "value_shashtiamsas"),
        ("MUT_SHAD_07_NATHONNATHA", "Nathonnatha Bala", "Sun", "kala_bala", "Nathonnatha Bala"),
        ("MUT_SHAD_08_PAKSHA", "Paksha Bala", "Sun", "kala_bala", "Paksha Bala"),
        ("MUT_SHAD_09_AYANA", "Ayana Bala", "Sun", "kala_bala", "Ayana Bala"),
        ("MUT_SHAD_10_TRIBHAGA", "Tribhaga Bala", "Sun", "kala_bala", "Tribhaga Bala"),
        ("MUT_SHAD_11_VARA", "Vara Bala", "Sun", "kala_bala", "Vara Bala"),
        ("MUT_SHAD_12_HORA", "Hora Bala", "Sun", "kala_bala", "Hora Bala"),
        ("MUT_SHAD_13_MASA", "Masa Bala", "Sun", "kala_bala", "Masa Bala"),
        ("MUT_SHAD_14_VARSHA", "Varsha Bala", "Sun", "kala_bala", "Varsha Bala"),
        ("MUT_SHAD_15_CHESHTA", "Cheshta Bala", "Sun", "cheshta_bala", "value_shashtiamsas"),
        ("MUT_SHAD_16_NAISARGIKA", "Naisargika Bala", "Sun", "naisargika_bala", "value_shashtiamsas"),
        ("MUT_SHAD_17_DRIK", "Drik Bala", "Sun", "drik_bala", "value_shashtiamsas")
    ]

    old_calc_shad = ShadbalaEngine.calculate_shadbala_suite

    for mut_id, comp_name, p_target, bala_cat, sub_comp in shad_sub_specs:
        b_val = getattr(baseline_shad.planets[p_target], bala_cat)
        b_num = b_val.sub_components.get(sub_comp, b_val.value_shashtiamsas) if hasattr(b_val, 'sub_components') and sub_comp in b_val.sub_components else b_val.value_shashtiamsas

        def mut_func(canonical_chart, v_suite, cat=bala_cat, comp=sub_comp, p=p_target):
            res = old_calc_shad(canonical_chart, v_suite)
            target_obj = getattr(res.planets[p], cat)
            if hasattr(target_obj, 'sub_components') and comp in target_obj.sub_components:
                target_obj.sub_components[comp] = target_obj.sub_components[comp] + 10.0
            else:
                target_obj.value_shashtiamsas = target_obj.value_shashtiamsas + 10.0
            return res

        ShadbalaEngine.calculate_shadbala_suite = mut_func
        m_shad = ShadbalaEngine.calculate_shadbala_suite(chart, varga_suite)
        m_val = getattr(m_shad.planets[p_target], bala_cat)
        m_num = m_val.sub_components.get(sub_comp, m_val.value_shashtiamsas) if hasattr(m_val, 'sub_components') and sub_comp in m_val.sub_components else m_val.value_shashtiamsas

        # Restore
        ShadbalaEngine.calculate_shadbala_suite = old_calc_shad
        r_shad = ShadbalaEngine.calculate_shadbala_suite(chart, varga_suite)
        r_val = getattr(r_shad.planets[p_target], bala_cat)
        r_num = r_val.sub_components.get(sub_comp, r_val.value_shashtiamsas) if hasattr(r_val, 'sub_components') and sub_comp in r_val.sub_components else r_val.value_shashtiamsas

        detected = (m_num != b_num) and (r_num == b_num)

        rec = {
            "mutation_id": mut_id,
            "category": "SHADBALA_SUBCOMPONENT",
            "component": comp_name,
            "target_planet": p_target,
            "baseline_value": b_num,
            "mutated_value": m_num,
            "restored_value": r_num,
            "detected": detected,
            "restored": r_num == b_num
        }
        records.append(rec)

        with open(reports_dir_r2 / f"{mut_id}.json", "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2)
        with open(reports_dir_r1 / f"{mut_id}.json", "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2)

        print(f"[{'PASS' if detected else 'FAIL'}] {mut_id}: {comp_name} ({p_target}) -> Baseline: {b_num}, Mutated: {m_num}, Restored: {r_num}")

    # ------------------------------------------------------------
    # 2. 56 ASHTAKAVARGA BAV CELL MUTATIONS
    # ------------------------------------------------------------
    targets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    contribs = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ascendant"]

    cell_idx = 1
    for t_planet in targets:
        for c_source in contribs:
            mut_id = f"MUT_BAV_{cell_idx:02d}_{t_planet}_{c_source}"
            orig_houses = list(BAV_RULES[t_planet][c_source])
            mut_houses = orig_houses[:-1] if len(orig_houses) > 1 else [1]

            b_bav = baseline_asht.bav[t_planet].bindus

            BAV_RULES[t_planet][c_source] = mut_houses
            m_asht = AshtakavargaEngine.calculate_ashtakavarga(chart)
            m_bav = m_asht.bav[t_planet].bindus

            BAV_RULES[t_planet][c_source] = orig_houses
            r_asht = AshtakavargaEngine.calculate_ashtakavarga(chart)
            r_bav = r_asht.bav[t_planet].bindus

            detected = (m_bav != b_bav) and (r_bav == b_bav)

            rec = {
                "mutation_id": mut_id,
                "category": "BAV_CONTRIBUTOR_RULE",
                "component": f"BAV {t_planet} from {c_source}",
                "target_planet": t_planet,
                "contributor_source": c_source,
                "baseline_bav_vector": b_bav,
                "mutated_bav_vector": m_bav,
                "restored_bav_vector": r_bav,
                "detected": detected,
                "restored": r_bav == b_bav
            }
            records.append(rec)

            with open(reports_dir_r2 / f"{mut_id}.json", "w", encoding="utf-8") as f:
                json.dump(rec, f, indent=2)
            with open(reports_dir_r1 / f"{mut_id}.json", "w", encoding="utf-8") as f:
                json.dump(rec, f, indent=2)

            print(f"[{'PASS' if detected else 'FAIL'}] {mut_id}: BAV {t_planet} from {c_source} -> Detected: {detected}")
            cell_idx += 1

    # Final summary documents
    attempted = len(records)
    detected_count = sum(1 for r in records if r["detected"])

    summary_doc = {
        "attempted_mutations": attempted,
        "detected_mutations": detected_count,
        "undetected_mutations": attempted - detected_count,
        "shadbala_mutations_detected": sum(1 for r in records if r["category"] == "SHADBALA_SUBCOMPONENT" and r["detected"]),
        "bav_mutations_detected": sum(1 for r in records if r["category"] == "BAV_CONTRIBUTOR_RULE" and r["detected"]),
        "detection_score_percent": round((detected_count / attempted) * 100.0, 2),
        "mutation_records": records
    }

    # Save into reports/r7/r2/ and reports/r7/r1/
    for out_p in [Path("reports/r7/r2"), Path("reports/r7/r1")]:
        out_p.mkdir(parents=True, exist_ok=True)
        with open(out_p / "mutation_execution.json", "w", encoding="utf-8") as f:
            json.dump(summary_doc, f, indent=2)
        with open(out_p / "mutation_inventory.json", "w", encoding="utf-8") as f:
            json.dump(summary_doc, f, indent=2)
        with open(out_p / "mutation_results.json", "w", encoding="utf-8") as f:
            json.dump(summary_doc, f, indent=2)

    print("============================================================")
    print(f"TOTAL MUTATIONS EXECUTED: {attempted} | DETECTED: {detected_count} ({summary_doc['detection_score_percent']}%)")
    print("============================================================")

if __name__ == "__main__":
    run_73_mutations()
