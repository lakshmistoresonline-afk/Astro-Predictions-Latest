# Phase 2E-R4.1-R12 Forensic Architecture & Inventory Audit Report

## 1. Executive Summary
Phase 2E-R4.1-R12 establishes a pure end-to-end certification pipeline starting from raw `BirthInput` through `build_canonical_vedic_chart`, `VargaEngine`, `ShadbalaEngine`, and `AshtakavargaEngine`.
This audit inspects every component in the calculation chain and proves zero reference longitude overrides, zero oracle contamination, and zero tolerance inflation.

## 2. Complete Component Inventory

| Component ID | Component Name | Source File | Key Entry Point / Function | Inputs | Outputs | Reads Reference expected? | Oracle Contaminated? | Hardcoded Shortcuts? |
|---|---|---|---|---|---|---|---|---|
| A | Production Astronomy Provider | `apps/api/engines/astronomy/provider.py` | `AstronomyProvider.get_planetary_positions()` | Julian Day, Lat/Lon, Elevation | Sidereal Longitudes, Velocities, Retrograde flags | **NO** | **NO** | **NO** |
| B | Canonical Chart Builder | `apps/api/engines/vedic/chart_builder.py` | `build_canonical_vedic_chart()` | `BirthInput` | `CanonicalVedicChart` | **NO** | **NO** | **NO** |
| C | Production Varga Engine | `apps/api/engines/varga/engine.py` | `VargaEngine.calculate_all_16_vargas()` | `CanonicalVedicChart` | `Full16VargaSuite` | **NO** | **NO** | **NO** |
| D | Production Shadbala Engine | `apps/api/engines/strength/shadbala.py` | `ShadbalaEngine.calculate_shadbala_suite()` | `CanonicalVedicChart`, `Full16VargaSuite` | `ShadbalaSuiteResult` (17 subcomponents x 7 planets) | **NO** | **NO** | **NO** |
| E | Production Ashtakavarga Engine | `apps/api/engines/strength/ashtakavarga.py` | `AshtakavargaEngine.calculate_ashtakavarga()` | `CanonicalVedicChart` | `AshtakavargaSuiteResult` (BAV & SAV) | **NO** | **NO** | **NO** |
| F | Pure Production Pipeline Adapter | `apps/api/tests/certification/production_pipeline.py` | `get_pure_production_results()` | `BirthInput` | Production Chart, Shadbala, BAV & SAV | **NO** | **NO** | **NO** |
| G | Independent Chart Oracle | `apps/api/tests/oracles/phase_2e_r4_1/independent_chart.py` | `IndependentChart()` | Raw Longitudes, Ayanamsha | `IndependentChart` | **NO** | **NO** | **NO** |
| H | Independent Shadbala Oracle | `apps/api/tests/oracles/phase_2e_r4_1/independent_shadbala.py` | `r4_calculate_shadbala_for_planet()` | `IndependentChart`, Planet Name | Dict of 17 subcomponents | **NO** | **NO** | **NO** |
| I | Independent Ashtakavarga Oracle | `apps/api/tests/oracles/phase_2e_r4_1/independent_ashtakavarga.py` | `r4_independent_bav()`, `r4_independent_sav()` | `IndependentChart`, Target Planet | 12-house BAV & SAV vectors | **NO** | **NO** | **NO** |
| J | Provenance AST Auditor | `scripts/audit_r7_r12_provenance.py` | `main()` | Python Source Files | Terminal Output, Exit Code | **NO** | **NO** | **NO** |
| K | 42-Gate Certification Runner | `scripts/run_phase_2e_r4_1_r7_r12_certification.py` | `run_r7_r12_certification()` | Pure Adapters, Oracles, Fixtures | Certification JSON, Terminal Logs | Comparison Only | **NO** | **NO** |

## 3. Provenance Classification Principles
- `PRODUCTION`: Generated 100% by production application code starting from `BirthInput`.
- `INDEPENDENT_ORACLE`: Derived 100% by independent oracle modules without production imports.
- `FROZEN_REFERENCE`: Immutable expected fixture JSON fields used solely as comparison targets.
