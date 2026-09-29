# Phase 2E-R4.1-R6 Repository Forensic Map

## 1. Audited Commit Identification
- **Commit Hash**: `cbe4bc66a4f734ffca8b233bb3ee46c887044c28`
- **Branch**: `main`
- **Working Tree**: CLEAN (`nothing to commit, working tree clean`).

## 2. Architecture & Path Analysis

### A. Production Calculation Path
- `POST /api/v1/birth-profile` (`apps/api/main.py`)
  ↓
- `ReportGeneratorEngine.generate_comprehensive_report` (`apps/api/engines/report_engine.py`)
  ↓
- `build_canonical_vedic_chart` (`apps/api/engines/vedic/chart_builder.py`) using `SkyfieldJPLProvider` (`apps/api/engines/astronomy/de440s.bsp`)
  ↓
- `VargaEngine.calculate_all_16_vargas` (`apps/api/engines/varga/engine.py`)
  ↓
- `AshtakavargaEngine.calculate_ashtakavarga` (`apps/api/engines/strength/ashtakavarga.py`)
- `ShadbalaEngine.calculate_shadbala_suite` (`apps/api/engines/strength/shadbala.py`)
  ↓
- Response JSON serialization.

### B. Independent Reference Path A (PyEphem 4.2.1)
- **Script**: `reference_source/pyephem_reference/standalone_pyephem.py`
- **Inputs**: Reads raw input specification JSONs from `reference_source/inputs/`.
- **Dependencies**: `ephem` 4.2.1 (XEphem Engine), `math`, `json`, `hashlib`.
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`).

### C. Independent Reference Path B (Skyfield 1.55 DE440s)
- **Script**: `reference_source/skyfield_reference/standalone_skyfield.py`
- **Inputs**: Reads raw input specification JSONs from `reference_source/inputs/`.
- **Kernel**: `apps/api/engines/astronomy/de440s.bsp`
- **Dependencies**: `skyfield.api` 1.55, `math`, `json`, `hashlib`.
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`).

### D. Independent Mathematical Oracle Path
- **Package**: `apps/api/tests/oracles/phase_2e_r4_1/`
- **Modules**:
  - `independent_chart.py`: Independent `IndependentChart` class.
  - `independent_geometry.py`: Ecliptic distance, declination, and Drishti Pinda.
  - `independent_calendar.py`: Standalone Julian Day, Vara, Hora, Masa, and Varsha lords.
  - `independent_varga.py`: Standalone D1..D30 divisional sign calculation.
  - `independent_ashtakavarga.py`: Standalone BAV and SAV matrices.
  - `independent_shadbala.py`: Standalone calculation of all 17 Shadbala subcomponents.
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`).

### E. Frozen Expected Data Path
- **Generator**: `apps/api/tests/oracles/phase_2e_r4_1/generate_expected.py`
- **Inputs**: Reads `reference_source/inputs/*.json` and `reference_source/pyephem_reference/*.json`.
- **Outputs**: Precomputed expected JSON fixtures in `apps/api/tests/fixtures/phase_2e_r4_1_expected/` with SHA-256 integrity hashes.
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`).

### F. Mutation Testing Path
- **Script**: `apps/api/tests/oracles/phase_2e_r4_1/test_mutation.py`
- **Logic**: Mutates production engine rules at runtime and asserts that test assertions catch the mutation.
- **Output**: Writes machine-readable results to `docs/PHASE_2E_R4_1_R4_MUTATION_RESULTS.json`.

### G. Certification & Report Generation Path
- **Runner**: `reference_source/cross_check_dual_ephemeris.py` & `generate_dual_ephemeris_matrix.py`.
- **Output Artifacts**: Raw CSV, MD matrices, JSON gate manifests.
