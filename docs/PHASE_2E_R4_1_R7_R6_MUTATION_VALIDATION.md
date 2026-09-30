# Phase 2E-R4.1-R7-R6 Physical Source Mutation Validation Report

## 1. Physical File Source Mutation Protocol Verification
Every mutation in `scripts/execute_r7_r4_mutation_suite.py` satisfies the canonical lifecycle:
1. **Fresh Subprocess Baseline**: `run_single_mutation_case.py` returns `ORACLE_PASS` (exit code 0).
2. **Replacement Count Check**: `replacement_count == 1` strictly enforced.
3. **Physical File Mutation**: `shadbala.py` or `ashtakavarga.py` bytes modified on disk (`original_sha256 != mutated_sha256`).
4. **Fresh Subprocess Mutation Validation**: `run_single_mutation_case.py` returns `ORACLE_MISMATCH` (exit code 1).
5. **Exact Byte Restoration**: Exact original bytes restored on disk (`original_bytes == restored_bytes` AND `original_sha256 == restored_sha256`).
6. **Fresh Subprocess Restoration Validation**: `run_single_mutation_case.py` returns `ORACLE_PASS` (exit code 0).

## 2. 17 Physical Source Shadbala Mutations
1. `MUT_SHAD_01_UCCHA`: Uccha Bala -> Certified (`ORACLE_MISMATCH` detected)
2. `MUT_SHAD_02_SAPTA`: Sapta Vargaja Bala -> Certified (`ORACLE_MISMATCH` detected)
3. `MUT_SHAD_03_OJHA`: Ojha Yugma Bala -> Certified (`ORACLE_MISMATCH` detected)
4. `MUT_SHAD_04_KENDRADI`: Kendradi Bala -> Certified (`ORACLE_MISMATCH` detected)
5. `MUT_SHAD_05_DREKKANA`: Drekkana Bala -> Certified (`ORACLE_MISMATCH` detected)
6. `MUT_SHAD_06_DIG`: Dig Bala -> Certified (`ORACLE_MISMATCH` detected)
7. `MUT_SHAD_07_NATHONNATHA`: Nathonnatha Bala -> Certified (`ORACLE_MISMATCH` detected)
8. `MUT_SHAD_08_PAKSHA`: Paksha Bala -> Certified (`ORACLE_MISMATCH` detected)
9. `MUT_SHAD_09_AYANA`: Ayana Bala -> Certified (`ORACLE_MISMATCH` detected)
10. `MUT_SHAD_10_TRIBHAGA`: Tribhaga Bala -> Certified (`ORACLE_MISMATCH` detected)
11. `MUT_SHAD_11_VARA`: Vara Bala -> Certified (`ORACLE_MISMATCH` detected)
12. `MUT_SHAD_12_HORA`: Hora Bala -> Certified (`ORACLE_MISMATCH` detected)
13. `MUT_SHAD_13_MASA`: Masa Bala -> Certified (`ORACLE_MISMATCH` detected)
14. `MUT_SHAD_14_VARSHA`: Varsha Bala -> Certified (`ORACLE_MISMATCH` detected)
15. `MUT_SHAD_15_CHESHTA`: Cheshta Bala -> Certified (`ORACLE_MISMATCH` detected)
16. `MUT_SHAD_16_NAISARGIKA`: Naisargika Bala -> Certified (`ORACLE_MISMATCH` detected)
17. `MUT_SHAD_17_DRIK`: Drik Bala -> Certified (`ORACLE_MISMATCH` detected)

## 3. 56 Physical Source BAV Rule Mutations
56 / 56 BAV contributor cell mutations executed and certified (`MUT_BAV_01` through `MUT_BAV_56`).

## 4. Score Summary
- **Attempted Mutations**: 73
- **Certified Mutations**: 73
- **Detection Score**: **100.0%**
