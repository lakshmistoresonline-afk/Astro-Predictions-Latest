# Phase 2E-R4.1-R7-R6 Oracle Forensic Dependency & Provenance Audit

## 1. Forensic Search Results
Recursive AST & string search across `apps/api/tests/oracles/phase_2e_r4_1/` for production engine patterns:
- `apps.api.engines.*` in core oracle files: **0**
- `build_canonical_vedic_chart` in core oracle files: **0**
- `ShadbalaEngine` in core oracle files: **0**
- `AshtakavargaEngine` in core oracle files: **0**
- `VargaEngine` in core oracle files: **0**
- `ReportGeneratorEngine` in core oracle files: **0**

## 2. Oracle File Inventory & Import Cleanliness
| Oracle Module | Purpose | Production Imports | Production Runtime Calls |
|---|---|---|---|
| `independent_chart.py` | Standalone In-Memory Chart Data Structure | **0** | **0** |
| `independent_geometry.py` | Trigonometric & BPHS Aspect Calculations | **0** | **0** |
| `independent_varga.py` | Pure Division Arithmetic for 16 Vargas | **0** | **0** |
| `independent_shadbala.py` | Pure BPHS 17-Subcomponent Shadbala Oracle | **0** | **0** |
| `independent_ashtakavarga.py` | Pure Parashari BAV / SAV Oracle | **0** | **0** |
| `generate_expected.py` | Pure Fixture Expected Value Generator | **0** | **0** |

## 3. Metric Summary
- **Production Imports**: `0`
- **Production Runtime Calls**: `0`
- **Production-Derived Expected Values**: `0`
- **Provenance Classification**: **ORACLE_DERIVED_REFERENCE** (Derived purely via standalone independent BPHS oracle algorithms from external astronomical inputs).
