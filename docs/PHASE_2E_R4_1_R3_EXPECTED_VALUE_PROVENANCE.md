# Phase 2E-R4.1-R3 Expected Value Provenance & Pipeline

## 1. Generation Pipeline
Expected values in `apps/api/tests/fixtures/phase_2e_r4_1_expected/` are precomputed using `apps/api/tests/oracles/phase_2e_r4_1/generate_expected.py`.

Pipeline:
```
Raw PyEphem Reference JSONs (reference_source/raw_reference/*.json)
       ↓
Independent Chart State (IndependentChart)
       ↓
R4.1 Pure Independent Oracle (independent_shadbala.py & independent_ashtakavarga.py)
       ↓
Frozen Expected JSON Fixtures (apps/api/tests/fixtures/phase_2e_r4_1_expected/*.json)
```

## 2. Zero Production Imports
`generate_expected.py` contains 0 imports from `apps.api.engines.*`. Tested and verified by `test_r4_1_runtime_zero_trust_isolation` and `test_production_unavailable_mode`.

## 3. SHA-256 Hashes
Each expected JSON document contains a `sha256_manifest_hash` / `integrity_hash` payload.
