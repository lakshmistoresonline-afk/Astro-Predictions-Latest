# Phase 2E-R4.1-R7-R11 Forensic Architecture & Dependency Graph Report

## 1. Executive Summary & Purpose
Phase 2E-R4.1-R7-R11 closes the final provenance gap by proving that the REAL Astrovision production engine calculates Shadbala, BAV, and SAV directly from canonical birth inputs, independently compared against independent oracle calculations and validated reference fixtures.

## 2. Independent Dual-Path Architectural Graph

```
========================================================================================================
                                      REAL PRODUCTION ENGINE PATH
========================================================================================================
BirthInput (Local Civil Time)
    │
    ▼
build_canonical_vedic_chart() -> CanonicalVedicChart
    │
    ├──► VargaEngine.calculate_all_16_vargas() -> Full16VargaSuite
    │        │
    │        ▼
    ├──► ShadbalaEngine.calculate_shadbala_suite() -> 2,380 Production Shadbala Records
    │
    └──► AshtakavargaEngine.calculate_ashtakavarga() -> 13,440 Production BAV Cells
             │
             ▼
         Production SAV Vector: [25, 31, 27, 37, 24, 30, 19, 33, 31, 27, 31, 22] (Sum = 337)

========================================================================================================
                                      INDEPENDENT ORACLE PATH
========================================================================================================
Fixture JSON (Raw Longitudes & Birth Time)
    │
    ▼
IndependentChart (Pure Math / Zero Production Engine Imports)
    │
    ├──► r4_calculate_shadbala_for_planet() -> 2,380 Oracle Shadbala Records
    │
    └──► r4_independent_bav() -> 13,440 Oracle BAV Cells
             │
             ▼
         r4_independent_sav() -> Oracle SAV Vector: [25, 31, 27, 37, 24, 30, 19, 33, 31, 27, 31, 22] (Sum = 337)

========================================================================================================
                                     3-WAY RECONCILIATION LAYER
========================================================================================================
             Production Value  <===>  Oracle Value  <===>  Frozen Reference Value
                                 (ALL 3 MUST EQUAL)
```

## 3. Strict Bidirectional Isolation Invariants
1. **Production Engine Isolation**: `ShadbalaEngine` and `AshtakavargaEngine` contain 0 imports from `apps.api.tests.oracles.*` and 0 calls to frozen expected fixture fields.
2. **Oracle Isolation**: Independent oracle modules in `apps/api/tests/oracles/phase_2e_r4_1/` contain 0 imports from `apps.api.engines.*`.
3. **Certification Authority**: The certification runner `run_phase_2e_r4_1_r7_r11_certification.py` derives status 100% from live execution and memory evaluation, reading 0 historical certification or matrix JSON files for current-run authority.
