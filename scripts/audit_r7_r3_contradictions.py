"""
Automated Contradiction Auditor for Phase 2E-R4.1-R7-R8.
Audits reports and manifests across r1 through r8 for logical contradictions,
mismatched mutation counts, or file count discrepancies.
Returns exit code 0 if 0 contradictions found; otherwise non-zero exit code.
"""
import json
import sys
from pathlib import Path

def run_contradiction_audit():
    contradictions = []

    # Check raw reference manifest vs expected fixtures count
    manifest_path = Path("PHASE_2E_R4_1_REFERENCE_MANIFEST.json")
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            man_data = json.load(f)
        if len(man_data) != 20:
            contradictions.append(f"Reference manifest count ({len(man_data)}) != 20")
    else:
        contradictions.append("Reference manifest missing")

    # Audit individual mutation record counts across r1 through r8
    for r_level in ["r8", "r7", "r6", "r5", "r4", "r3", "r2", "r1"]:
        r_dir = Path(f"reports/r7/{r_level}")
        if r_dir.exists():
            mut_files = list((r_dir / "mutations").glob("*.json"))
            if len(mut_files) != 73:
                contradictions.append(f"Mutation individual JSON files in {r_level} ({len(mut_files)}) != 73")

            sum_file = r_dir / "source_mutation_results.json"
            if sum_file.exists():
                with open(sum_file, "r", encoding="utf-8") as f:
                    s_data = json.load(f)
                if s_data.get("attempted_mutations") != 73:
                    contradictions.append(f"Attempted mutations in {r_level} summary ({s_data.get('attempted_mutations')}) != 73")
                if s_data.get("detected_mutations") != 73:
                    contradictions.append(f"Detected mutations in {r_level} summary ({s_data.get('detected_mutations')}) != 73")
                if s_data.get("detection_score_percent") != 100.0:
                    contradictions.append(f"Detection score in {r_level} summary ({s_data.get('detection_score_percent')}) != 100.0")

    status = "PASS" if len(contradictions) == 0 else "FAIL"
    res_doc = {
        "contradictions_found": len(contradictions),
        "status": status,
        "contradiction_details": contradictions
    }

    out_p = Path("reports/r7/r3")
    out_p.mkdir(parents=True, exist_ok=True)
    with open(out_p / "contradiction_audit.json", "w", encoding="utf-8") as f:
        json.dump(res_doc, f, indent=2)

    print(f"Contradiction Audit: Found {len(contradictions)} contradictions. Status: {status}")
    if len(contradictions) > 0:
        for c in contradictions:
            print(f"  - {c}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(run_contradiction_audit())
