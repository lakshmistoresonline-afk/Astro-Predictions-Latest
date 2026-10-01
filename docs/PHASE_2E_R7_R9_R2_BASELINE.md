# Phase 2E-R7-R9-R2 Baseline Status Report

## 1. Baseline State Identification
- **Current Commit**: `20c311feecfbed64193bba661f534ee397944685` (R7-R9-R1)
- **Current Certification Status**: CERTIFIED in R7-R9-R1.
- **Current Gate Total**: 29 / 29 Gates Passed.
- **Current Mutation Performance**:
  - 73 / 73 Physical Source File Mutations Certified (100% Score)
  - 20 / 20 Unique Reference Fixtures Evaluated Per Mutation (`REF_001` .. `REF_020`)
  - 1,460 / 1,460 Baseline Evaluations Passed
  - 1,460 / 1,460 Mutated Evaluations Produced ORACLE_MISMATCH
  - 1,460 / 1,460 Restored Evaluations Passed
  - 4,380 / 4,380 Total Fixture-Level Lifecycle Evaluations
  - 0 Production Exceptions / Crashes
  - Total Mutation Suite Execution Time: **under 2.0 seconds**

## 2. Identified Weaknesses to Fix in R7-R9-R2
1. **G06 / G07 Matrix File Dependency**:
   - In R7-R9-R1, `run_matrix_generation()` was called, which generated matrix files on disk (`reports/r7/r2/shadbala_reference_matrix.json` and `reports/r7/r2/bav_reference_matrix.json`).
   - The runner then read those JSON files from disk and verified `"record_count"` and `"match": true`.
   - **Remediation**: Refactor `generate_r7_r2_matrices.py` to expose `generate_shadbala_records()`, `generate_bav_records()`, and `derive_sav_from_bav()`. The certification runner will receive live Python data structures directly in memory and independently validate every key tuple and value against live calculations without reading disk JSONs as the authority.
2. **G08 SAV Derivation Dependency**:
   - In R7-R9-R1, the runner read `REF_001.json` to get `expected["ashtakavarga"]["sav"]`.
   - **Remediation**: Remove `REF_001.json` as the calculation source. Derive the SAV vector directly from the live in-memory BAV cell matrix by summing BAV bindus across the 7 target planets for each of the 12 houses. Verify mathematical consistency ($SAV[h] = \sum_{p=1}^7 BAV_p[h]$) and compare the live calculated vector against expected values.
3. **Adversarial Suite Expansion**:
   - Expand the 25 adversarial attacks to 34 attack tests (Attacks 26 to 34) specifically targeting live in-memory matrix generation, key-tuple uniqueness, SAV derivation independence, and historical report file deletion/corruption resilience.
