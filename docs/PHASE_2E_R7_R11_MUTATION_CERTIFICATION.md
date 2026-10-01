# Phase 2E-R4.1-R7-R11 Physical Source Mutation Certification Report

## 1. Physical File Source Mutation Protocol
All 73 physical source mutations in `scripts/execute_r7_r4_mutation_suite.py` execute the canonical 20-fixture lifecycle:
1. **Fresh Process Baseline**: `run_case` executed on ALL 20 reference fixtures (`REF_001`..`REF_020`) returning `ORACLE_PASS` (exit code 0). Real `production_value`, `oracle_value`, `delta` recorded for each fixture.
2. **Replacement Count Check**: `replacement_count == 1` strictly enforced.
3. **Physical File Source Mutation**: `shadbala.py` or `ashtakavarga.py` bytes modified on disk (`original_sha256 != mutated_sha256`).
4. **Fresh Process Mutation Validation**: `run_case` executed on ALL 20 reference fixtures (`REF_001`..`REF_020`) returning `ORACLE_MISMATCH` (exit code 1). Real `production_value`, `oracle_value`, `delta` recorded for each fixture. (`PRODUCTION_EXCEPTION` is a failure!).
5. **Exact Byte Restoration**: Exact original bytes restored on disk (`original_bytes == restored_bytes` AND `original_sha256 == restored_sha256`).
6. **Fresh Process Restoration Validation**: `run_case` executed on ALL 20 reference fixtures (`REF_001`..`REF_020`) returning `ORACLE_PASS` (exit code 0). Real `production_value`, `oracle_value`, `delta` recorded for each fixture.

## 2. 17 Physical Source Shadbala Mutations
- 17 / 17 physical source Shadbala mutations certified across ALL 20 reference fixtures ($1,020$ fixture evaluations).

## 3. 56 Physical Source BAV Rule Mutations
- 56 / 56 physical source BAV mutations certified across ALL 20 reference fixtures ($3,360$ fixture evaluations).

## 4. Score Summary
- **Attempted Mutations**: 73
- **Certified Mutations**: 73
- **Detection Score**: **100.0%**
- **Total Fixture Lifecycle Evaluations**: **4,380 / 4,380 (100%)**
- **Production Exceptions**: **0**
