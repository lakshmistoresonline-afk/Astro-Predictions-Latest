# Phase 2E-R4.1-R3 Forensic Starting State Audit

## 1. Starting State Audit
- **Current Commit**: `3aa520adc73b451e9cafb1edd63a15901de8faab` (or working tree state following R4.1).
- **Audit Target**: Prove PyEphem 4.2.1 standalone execution, ephemeris cross-check vs Skyfield DE440s, zero production engine contamination in reference extraction, 17/17 Shadbala component validation, 56/56 Ashtakavarga cell validation, and complete test suite integrity.

## 2. Key Artifacts & Directories To Build / Audit
- `reference_source/standalone_ephemeris_extractor.py`: Independent PyEphem 4.2.1 standalone reference dataset generator.
- `reference_source/cross_check_pyephem_skyfield.py`: Standalone cross-check script comparing PyEphem 4.2.1 vs Skyfield JPL DE440s.
- `reference_source/raw_reference/`: Directory containing 20 raw JSON reference datasets (15 real charts + 5 synthetic boundary cases).
- `reference_source/cross_check_results.json`: Machine-readable numerical comparison dataset.
- `PHASE_2E_R4_1_R3_REFERENCE_MANIFEST.json`: Cryptographic SHA-256 manifest of all reference files.
- `apps/api/tests/oracles/phase_2e_r4_1/`: Pure R4.1 independent mathematical oracle package.
- `apps/api/tests/fixtures/phase_2e_r4_1_expected/`: Frozen expected JSON fixtures.
