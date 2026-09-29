# Phase 2E-R4.1-R7-R3 Reference Chain & Isolation Audit

## 1. Zero-Trust Architecture
```
External Ephemeris (PyEphem 4.2.1 / Skyfield 1.55 DE440s)
       ↓ (Raw Longitudes, Latitudes, Asc, MC)
reference_source/inputs/*.json -> reference_source/pyephem_reference/*.json
       ↓
R4.1 Independent Oracle (apps/api/tests/oracles/phase_2e_r4_1/)
       ↓
Frozen Expected Fixtures (apps/api/tests/fixtures/phase_2e_r4_1_expected/*.json)
       ↓
Production Engine Comparison (apps/api/engines/strength/)
       ↓
Three-Way Agreement (Frozen == Oracle == Production)
```

## 2. Import & Runtime Isolation Audit
- **Static AST Import Inspection**: `test_r4_1_static_import_isolation` verified 0 imports of `apps.api.engines.*` in `apps/api/tests/oracles/phase_2e_r4_1/` and `reference_source/`.
- **Runtime Zero-Trust Isolation**: `test_r4_1_runtime_zero_trust_isolation` monkeypatches all production engines with `OracleContaminationError` and proves that reference generation and oracle evaluation complete with 100% success.
- **Production Unavailable Mode**: `test_production_unavailable_mode` blocks production modules at `sys.modules` level during oracle execution.

## 3. Reference Layer Classifications
- `reference_source/pyephem_reference/*.json`: **EXTERNAL_ASTRONOMICAL_REFERENCE**
- `apps/api/tests/fixtures/phase_2e_r4_1_expected/*.json`: **ORACLE_DERIVED_REFERENCE**
- Lahiri, Ascendant, MC: **FORMULA_VERIFIED** (PyEphem vs Skyfield cross-check mean delta = 1.83", max delta = 19.81").
