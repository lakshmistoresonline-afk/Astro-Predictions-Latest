# Phase 2E-R4.1-R7-R3 Forensic Inventory & Repository Map

## 1. Audited Commit Identification
- **Current Head Commit**: `46d79efad04d293d42da0e2dbf24e8b3e25cea18`
- **Branch**: `main`
- **Working Tree**: CLEAN (`nothing to commit, working tree clean`).

## 2. Inventory of Current Artifacts

### A. Production Calculation Path
- `apps/api/main.py`: API endpoint `/api/v1/birth-profile`.
- `apps/api/engines/report_engine.py`: `ReportGeneratorEngine`.
- `apps/api/engines/vedic/chart_builder.py`: `build_canonical_vedic_chart` using Skyfield 1.55 + DE440s kernel.
- `apps/api/engines/varga/engine.py`: `VargaEngine`.
- `apps/api/engines/strength/ashtakavarga.py`: `AshtakavargaEngine`.
- `apps/api/engines/strength/shadbala.py`: `ShadbalaEngine`.

### B. Independent Astronomical Reference Layer
- `reference_source/inputs/*.json`: 20 raw input specification JSONs (15 real birth profiles + 5 synthetic boundary cases).
- `reference_source/pyephem_reference/standalone_pyephem.py`: PyEphem 4.2.1 standalone extractor (0 `apps.api.engines.*` imports).
- `reference_source/skyfield_reference/standalone_skyfield.py`: Skyfield 1.55 DE440s standalone extractor (0 `apps.api.engines.*` imports).
- `reference_source/cross_check_dual_ephemeris.py`: PyEphem vs Skyfield DE440s cross-check runner.
- `PHASE_2E_R4_1_REFERENCE_MANIFEST.json`: Cryptographic SHA-256 reference manifest.

### C. Independent Mathematical Oracle Layer
- `apps/api/tests/oracles/phase_2e_r4_1/`:
  - `independent_chart.py`: `IndependentChart`.
  - `independent_geometry.py`: Ecliptic geometry and Drishti Pinda.
  - `independent_calendar.py`: Vara, Hora, Masa, Varsha lords.
  - `independent_varga.py`: D1..D30 sign calculations.
  - `independent_ashtakavarga.py`: BAV/SAV matrices.
  - `independent_shadbala.py`: 17 Shadbala subcomponents.
  - `generate_expected.py`: Expected fixture generator (0 `apps.api.engines.*` imports).

### D. Frozen Expected Fixtures Layer
- `apps/api/tests/fixtures/phase_2e_r4_1_expected/*.json`: 20 precomputed frozen expected JSONs with SHA-256 integrity hashes. Classified as `ORACLE_DERIVED_REFERENCE`.

### E. Executable Mutation Testing Layer
- `scripts/execute_r7_r1_mutation_suite.py`: Harness for 17 Shadbala + 56 BAV mutations ($73/73$ total).
- `reports/r7/r3/mutations/`: Directory storing individual mutation lifecycle JSONs (`PASS -> FAIL -> PASS`).

### F. Reports & Certification Output Layer
- `reports/r7/r3/`: Output directory containing machine-readable JSON artifacts (`shadbala_reference_matrix.json`, `bav_reference_matrix.json`, `mutation_execution.json`, `contradiction_audit.json`, `final_gate_matrix.json`, `certification_results.json`).
- `scripts/run_phase_2e_r4_1_r7_certification.py`: Fail-closed dynamic certification runner.
