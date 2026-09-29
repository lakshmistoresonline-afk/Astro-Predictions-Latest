# Phase 2E-R4.1-R7-R2 Reference Chain Forensic Audit

## 1. Reference Data Provenance & Chain Analysis
- **A. Raw Planetary Longitudes & Latitudes**: Extracted independently via PyEphem 4.2.1 (`reference_source/pyephem_reference/`) and cross-checked against Skyfield 1.55 DE440s (`reference_source/skyfield_reference/`). Zero production imports (`0` calls to `apps.api.engines.*`). Classification: **EXTERNAL_ASTRONOMICAL_REFERENCE**.
- **B. Ascendant & MC**: Calculated via Local Sidereal Time (LST) and true obliquity ($\varepsilon$) in standalone PyEphem and Skyfield DE440s extractors. Classification: **ASTRONOMICAL_LST_REFERENCE**.
- **C. Lahiri Ayanamsha**: Calculated via $A = 23.85^\circ + 1.396^\circ \cdot T$. Formula Agreement: **PASS**. Authoritative Standard Validation: **FORMULA_VERIFIED**.
- **D. Shadbala & BAV Expected Values**: Precomputed by `generate_expected.py` using pure R4.1 oracle functions. Classification: **ORACLE_DERIVED_REFERENCE**.

## 2. Validation Architecture
```
External Ephemeris (PyEphem 4.2.1 / Skyfield DE440s)
       ↓ (Raw Longitudes, Latitudes, Asc, MC)
reference_source/pyephem_reference/*.json
       ↓
R4.1 Independent Oracle (apps/api/tests/oracles/phase_2e_r4_1/)
       ↓
Frozen Expected Fixtures (apps/api/tests/fixtures/phase_2e_r4_1_expected/*.json)
       ↓
Production Engine Comparison (apps/api/engines/strength/)
       ↓
Three-Way Agreement (Frozen == Oracle == Production)
```

## 3. Labeling Transparency
The frozen expected fixture files in `apps/api/tests/fixtures/phase_2e_r4_1_expected/` are classified as **ORACLE_DERIVED_REFERENCE** fixtures. They prove zero-trust mathematical consistency, determinism, and regression protection, while the ephemeris inputs prove external astronomical alignment.
