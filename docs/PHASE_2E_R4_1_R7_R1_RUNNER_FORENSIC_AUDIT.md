# Phase 2E-R4.1-R7-R1 Runner Forensic Audit & Remediation Plan

## 1. Forensic Audit Findings
1. **Contradiction in R7 Mutation Count**: Previous documentation reported 73 mutations in summary texts, but the underlying execution script ran only 58 mutations (3 Shadbala + 55 BAV).
2. **Hardcoded Evidence Strings in Runner**: `scripts/run_phase_2e_r4_1_r7_certification.py` had hardcoded text strings in print/logging calls rather than reading generated machine-readable JSON artifacts.
3. **Matrix Dimensions**:
   - Shadbala required count: 20 fixtures x 7 planets x 17 subcomponents = **2380 component records**.
   - BAV required cell count: 20 fixtures x 7 target planets x 8 contributors x 12 houses = **13,440 cell-level records**.

## 2. R7-R1 Remediation Architecture
1. **Executable Mutation Engine** (`scripts/execute_r7_r1_mutation_suite.py`):
   - Executes 17 genuine Shadbala subcomponent mutations (production code level).
   - Executes 56 genuine BAV cell mutations (production code level).
   - Verifies baseline failure on mutated code, restores baseline, and logs individual mutation JSON files in `reports/r7/r1/mutations/`.
   - Total = **73/73 genuine mutations**.
2. **Shadbala Matrix Generator**: Produces 2380 component records in `reports/r7/r1/shadbala_matrix.json`.
3. **BAV Cell Matrix Generator**: Produces 13,440 cell records in `reports/r7/r1/bav_cell_matrix.json`.
4. **Dynamic Fail-Closed Certification Runner** (`scripts/run_phase_2e_r4_1_r7_certification.py`):
   - Reads `reports/r7/r1/*.json` dynamically.
   - Enforces exact record counts ($2380$, $13,440$, $73/73$ mutations, $180$ ephemeris points).
   - Fails with non-zero exit code if ANY gate fails or if any count deviates.
