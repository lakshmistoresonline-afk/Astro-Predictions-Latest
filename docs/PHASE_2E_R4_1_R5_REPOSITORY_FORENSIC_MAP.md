# Phase 2E-R4.1-R5 Repository Forensic Map

## 1. Audited Commit Identification
- **Commit Hash**: `461d440c706def9d9223a6f0bf506dada75f598c`
- **Branch**: `main`
- **Working Tree**: CLEAN (`nothing to commit, working tree clean`).

## 2. Architecture & Call-Graph Paths

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
- Output contract serialization.

### B. Independent Reference Path A (PyEphem 4.2.1)
- **Script**: `reference_source/pyephem_reference/standalone_pyephem.py`
- **Inputs**: Reads raw birth input specification JSONs from `reference_source/inputs/`.
- **Dependencies**: `ephem` 4.2.1 (XEphem C Ephemeris Core), `math`, `json`, `hashlib`.
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`).

### C. Independent Reference Path B (Skyfield 1.55 DE440s)
- **Script**: `reference_source/skyfield_reference/standalone_skyfield.py`
- **Inputs**: Reads raw birth input specification JSONs from `reference_source/inputs/`.
- **Dependencies**: `skyfield.api` 1.55, `apps/api/engines/astronomy/de440s.bsp`, `math`, `json`, `hashlib`.
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`).

### D. Independent Mathematical Oracle Path
- **Package**: `apps/api/tests/oracles/phase_2e_r4_1/`
- **Modules**:
  - `independent_chart.py`: Standalone `IndependentChart` data structure.
  - `independent_geometry.py`: Ecliptic distance, declination ($\delta$), and BPHS Drishti Pinda.
  - `independent_calendar.py`: Standalone Julian Day, Vara, Hora, Masa, and Varsha lords.
  - `independent_varga.py`: Standalone D1..D30 divisional sign calculation.
  - `independent_ashtakavarga.py`: Standalone BAV and SAV matrices.
  - `independent_shadbala.py`: Standalone calculation of all 17 Shadbala subcomponents.
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`).

### E. Frozen Expected Data Path
- **Generator**: `apps/api/tests/oracles/phase_2e_r4_1/generate_expected.py`
- **Inputs**: Reads `reference_source/inputs/*.json` and `reference_source/pyephem_reference/*.json`.
- **Outputs**: Stores immutable precomputed expected JSON fixtures in `apps/api/tests/fixtures/phase_2e_r4_1_expected/` with SHA-256 integrity hashes.
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`).

### F. Mutation Testing Path
- **Script**: `apps/api/tests/oracles/phase_2e_r4_1/test_mutation.py`
- **Logic**: Deliberately mutates production `DEBILITATION_DEGREES`, `BAV_RULES`, and `ShadbalaEngine` methods at runtime and asserts that test assertions detect the mutation.
- **Output**: Writes machine-readable results to `docs/PHASE_2E_R4_1_R4_MUTATION_RESULTS.json`.

### G. Three-Way Validation Path
- **Test File**: `apps/api/tests/oracles/phase_2e_r4_1/test_r4_1_oracle.py`
- **Assertion**: Enforces `Frozen Expected == R4.1 Independent Oracle == Production Engine Result` within $\le 0.03$ shashtiamsas for all 20 fixtures.
