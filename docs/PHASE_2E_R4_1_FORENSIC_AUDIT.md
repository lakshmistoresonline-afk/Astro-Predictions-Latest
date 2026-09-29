# Phase 2E-R4.1 Forensic Audit & Rejection of Circular Astronomy

## 1. Forensic Audit Findings
A forensic review of Phase 2E-R4 fixture generation (`apps/api/tests/fixtures/phase_2e_r4_expected/`) confirmed that the inputs and longitudes were extracted by executing the production astronomy engine `build_canonical_vedic_chart()`.

While the Shadbala and Ashtakavarga math inside `independent_shadbala.py` and `independent_ashtakavarga.py` was structurally independent, feeding production astronomical positions into the oracle created a circular dependency:
```
Production Astronomy (build_canonical_vedic_chart)
       ↓
Oracle Evaluation
       ↓
Frozen Expected Values
       ↓
Production Strength Engine Validation
```

## 2. R4.1 Remediation Architecture
To establish absolute, zero-trust numerical independence, Phase 2E-R4.1 replaces this pipeline with a three-layer decoupled architecture:

1. **Independent Reference Dataset** (`apps/api/tests/fixtures/phase_2e_r4_1_reference/`): Contains frozen astronomical reference data (sidereal longitudes, daily velocities, Ascendant, MC, ayanamsha) compiled independently without calling `build_canonical_vedic_chart()` or Skyfield.
2. **Pure Mathematical Oracle** (`apps/api/tests/oracles/phase_2e_r4_1/`): Contains self-contained, pure Python implementations for geometry, calendar, vargas (D1 to D30), BAV/SAV matrices, and Shadbala components with 0 imports from `apps.api.engines.*`.
3. **Frozen Expected Values** (`apps/api/tests/fixtures/phase_2e_r4_1_expected/`): Precomputed and frozen expected JSON files containing SHA-256 integrity hashes.
4. **Three-Way Comparison**: `Frozen Expected == R4 Independent Oracle == Production Engine Result`.
