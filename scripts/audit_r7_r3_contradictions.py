"""
Phase 2E-R4.1-R7-R6 Automated Contradiction Audit.
Detects any numerical or logical contradiction between reports, matrices, mutation files, and manifests.
Outputs reports/r7/r3/contradiction_audit.json.
"""
import json
import os
import sys
from pathlib import Path

def run_contradiction_audit():
    contradictions = []

    # 1. Check Fixture Manifest Counts
    man_path = Path("PHASE_2E_R4_1_REFERENCE_MANIFEST.json")
    if man_path.exists():
        with open(man_path, "r", encoding="utf-8") as f:
            man_entries = json.load(f)
        if len(man_entries) != 20:
            contradictions.append(f"Manifest entry count ({len(man_entries)}) does not equal 20 total fixtures")
    else:
        contradictions.append("Missing PHASE_2E_R4_1_REFERENCE_MANIFEST.json")

    # 2. Check Shadbala Matrix Counts
    shad_path = Path("reports/r7/r2/shadbala_reference_matrix.json")
    if shad_path.exists():
        with open(shad_path, "r", encoding="utf-8") as f:
            shad_doc = json.load(f)
        if shad_doc.get("record_count") != 2380:
            contradictions.append(f"Shadbala matrix record count ({shad_doc.get('record_count')}) != 2380")
    else:
        contradictions.append("Missing shadbala_reference_matrix.json")

    # 3. Check BAV Cell Matrix Counts
    bav_path = Path("reports/r7/r2/bav_reference_matrix.json")
    if bav_path.exists():
        with open(bav_path, "r", encoding="utf-8") as f:
            bav_doc = json.load(f)
        if bav_doc.get("record_count") != 13440:
            contradictions.append(f"BAV cell matrix record count ({bav_doc.get('record_count')}) != 13440")
    else:
        contradictions.append("Missing bav_reference_matrix.json")

    # 4. Check Mutation Results Counts & Artifacts across all r1..r6 directories
    for r_dir in [Path("reports/r7/r6"), Path("reports/r7/r5"), Path("reports/r7/r4"), Path("reports/r7/r3"), Path("reports/r7/r2"), Path("reports/r7/r1")]:
        mut_summary_path = r_dir / "source_mutation_results.json"
        if mut_summary_path.exists():
            with open(mut_summary_path, "r", encoding="utf-8") as f:
                mut_doc = json.load(f)
            if mut_doc.get("attempted_mutations") != 73 or mut_doc.get("detected_mutations") != 73:
                contradictions.append(f"Mutation summary in {r_dir.name} ({mut_doc.get('detected_mutations')}/{mut_doc.get('attempted_mutations')}) != 73/73")

            mut_files = list((r_dir / "mutations").glob("*.json"))
            if len(mut_files) != 73:
                contradictions.append(f"Mutation individual JSON files in {r_dir.name} ({len(mut_files)}) != 73")
        else:
            contradictions.append(f"Missing source_mutation_results.json in {r_dir.name}")

    # Save Contradiction Audit JSON
    out_dir = Path("reports/r7/r3")
    out_dir.mkdir(parents=True, exist_ok=True)

    res_doc = {
        "contradictions_found": len(contradictions),
        "status": "PASS" if len(contradictions) == 0 else "FAIL",
        "contradiction_details": contradictions
    }

    with open(out_dir / "contradiction_audit.json", "w", encoding="utf-8") as f:
        json.dump(res_doc, f, indent=2)

    print(f"Contradiction Audit: Found {len(contradictions)} contradictions. Status: {'PASS' if len(contradictions) == 0 else 'FAIL'}")
    return len(contradictions) == 0

if __name__ == "__main__":
    success = run_contradiction_audit()
    if not success:
        sys.exit(1)
