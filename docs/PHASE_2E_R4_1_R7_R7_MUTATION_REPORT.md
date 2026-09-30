# Phase 2E-R4.1-R7-R7 Physical Source Mutation Audit Report

## 1. Physical File Source Mutation Protocol
All 73 physical source mutations in `scripts/execute_r7_r4_mutation_suite.py` execute the canonical lifecycle:
1. **Fresh Subprocess Baseline**: `run_single_mutation_case.py` returns `ORACLE_PASS` (exit code 0). Real `production_value`, `oracle_value`, `delta` recorded.
2. **Replacement Count Check**: `replacement_count == 1` strictly enforced.
3. **Physical File Source Mutation**: `shadbala.py` or `ashtakavarga.py` bytes modified on disk (`original_sha256 != mutated_sha256`).
4. **Fresh Subprocess Mutation Validation**: `run_single_mutation_case.py` returns `ORACLE_MISMATCH` (exit code 1). Real `production_value`, `oracle_value`, `delta` recorded.
5. **Exact Byte Restoration**: Exact original bytes restored on disk (`original_bytes == restored_bytes` AND `original_sha256 == restored_sha256`).
6. **Fresh Subprocess Restoration Validation**: `run_single_mutation_case.py` returns `ORACLE_PASS` (exit code 0). Real `production_value`, `oracle_value`, `delta` recorded.

## 2. 17 Physical Source Shadbala Mutations
1. `MUT_SHAD_01_UCCHA`: Uccha Bala -> Certified
2. `MUT_SHAD_02_SAPTA`: Sapta Vargaja Bala -> Certified
3. `MUT_SHAD_03_OJHA`: Ojha Yugma Bala -> Certified
4. `MUT_SHAD_04_KENDRADI`: Kendradi Bala -> Certified
5. `MUT_SHAD_05_DREKKANA`: Drekkana Bala -> Certified
6. `MUT_SHAD_06_DIG`: Dig Bala -> Certified
7. `MUT_SHAD_07_NATHONNATHA`: Nathonnatha Bala -> Certified
8. `MUT_SHAD_08_PAKSHA`: Paksha Bala -> Certified
9. `MUT_SHAD_09_AYANA`: Ayana Bala -> Certified
10. `MUT_SHAD_10_TRIBHAGA`: Tribhaga Bala -> Certified
11. `MUT_SHAD_11_VARA`: Vara Bala -> Certified
12. `MUT_SHAD_12_HORA`: Hora Bala -> Certified
13. `MUT_SHAD_13_MASA`: Masa Bala -> Certified
14. `MUT_SHAD_14_VARSHA`: Varsha Bala -> Certified
15. `MUT_SHAD_15_CHESHTA`: Cheshta Bala -> Certified
16. `MUT_SHAD_16_NAISARGIKA`: Naisargika Bala -> Certified
17. `MUT_SHAD_17_DRIK`: Drik Bala -> Certified

## 3. 56 Physical Source BAV Rule Mutations
56 / 56 BAV contributor cell mutations executed and certified (`MUT_BAV_01` through `MUT_BAV_56`).

## 4. Score Summary
- **Attempted Mutations**: 73
- **Certified Mutations**: 73
- **Detection Score**: **100.0%**
