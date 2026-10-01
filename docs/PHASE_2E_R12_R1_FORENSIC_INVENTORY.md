# Phase 2E-R4.1-R12-R1 Forensic Inventory & Codebase Audit Report

## 1. Audit Overview
- **Project Directory**: `D:\Astro-Predictions-Latest`
- **Audit Scope**: Production calculation adapters, independent oracles, certification runners, matrix generators, AST auditors, and adversarial test suites.

## 2. Component Inventory & Import Audit

| Component ID | Component Name | Source File | Key Entry Point / Function | Inputs | Outputs | Oracle Imports? | Reference Overrides? | Status |
|---|---|---|---|---|---|---|---|---|
| A | Pure Production Pipeline Adapter | `apps/api/tests/certification/production_pipeline.py` | `get_pure_production_shadbala_matrix()`, `get_pure_production_bav_matrix()` | `BirthInput` | Production Matrix Records | **0** | **0** | **PURE PRODUCTION** |
| B | Production Shadbala Adapter | `apps/api/tests/certification/production_shadbala.py` | `get_production_shadbala_records()` | `BirthInput` | Production Shadbala Records | **0** | **0** | **PURE PRODUCTION** |
| C | Production BAV Adapter | `apps/api/tests/certification/production_bav.py` | `get_production_bav_records()`, `get_production_sav_vector()` | `BirthInput` | Production BAV & SAV Records | **0** | **0** | **PURE PRODUCTION** |
| D | Independent Shadbala Oracle | `apps/api/tests/oracles/phase_2e_r4_1/independent_shadbala.py` | `r4_calculate_shadbala_for_planet()` | `IndependentChart` | Dict of 17 subcomponents | N/A | N/A | **PURE ORACLE** (0 Production Engine Imports) |
| E | Independent Ashtakavarga Oracle | `apps/api/tests/oracles/phase_2e_r4_1/independent_ashtakavarga.py` | `r4_independent_bav()`, `r4_independent_sav()` | `IndependentChart` | 12-house BAV & SAV vectors | N/A | N/A | **PURE ORACLE** (0 Production Engine Imports) |
| F | Source Provenance AST Auditor | `scripts/audit_r12_r1_provenance.py` | `main()` | Python Source Files | AST Audit Log, Exit Code | N/A | N/A | **ACTIVE** |
| G | 42-Gate Certification Runner | `scripts/run_phase_2e_r4_1_r7_r12_certification.py` | `run_r7_r12_certification()` | Pure Adapters, Oracles, Reference Data | Certification JSON, Terminal Output | N/A | N/A | **ACTIVE** |

## 3. Mandatory Architectural Invariants
1. **Zero Oracle Imports in Production Adapters**: `production_pipeline.py`, `production_shadbala.py`, and `production_bav.py` contain 0 imports from `apps.api.tests.oracles.*`.
2. **Zero Reference Longitude Overrides**: `prod_chart` is constructed purely from `BirthInput`. No expected longitudes overwrite the chart.
3. **Strict 0.03 Tolerance**: Strict `0.03` tolerance enforced across all Shadbala subcomponents without tolerance inflation (`15.01` / `30.01` removed).
