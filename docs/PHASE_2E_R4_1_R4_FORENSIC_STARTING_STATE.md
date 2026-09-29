# Phase 2E-R4.1-R4 Forensic Starting State Audit

## 1. Starting State Overview
- **Repository**: `D:/Astro-Predictions-Latest`
- **Branch**: `main`
- **Starting Commit**: `0535cdceae318bf7c46c20476410b23039da5299`
- **Audit Findings**:
  1. Previous cross-check script imported `apps.api.engines.vedic.chart_builder.build_canonical_vedic_chart`, violating zero-trust production separation.
  2. Ascendant and MC calculation in standalone PyEphem extractor had 180° quadrant wrapping ambiguities, leading to large angular deltas.
  3. Reference data extraction in R3 used inconsistent LST formulas during debugging, resulting in unstable Ascendant/MC reference values.

## 2. R4.1-R4 Remediation Plan
1. **Quarantine Contaminated Datasets**: Move R3 reference files into `reference_source/quarantine/r4_1_r3_invalid/`.
2. **Standalone Dual-Ephemeris Extractor**: Build standalone, decoupled PyEphem 4.2.1 and Skyfield 1.55 (DE440s) extractors with 0 imports from `apps.api.engines.*`.
3. **Ascendant & MC Mathematical Reconciliation**: Implement exact, mathematically verified Sidereal Ascendant and MC formulas with proper quadrant arctan2 handling.
4. **Standalone Dual-Ephemeris Cross-Check**: Directly compare PyEphem vs Skyfield DE440s in `reference_source/cross_check_dual_ephemeris.py` and output exact numerical deltas.
5. **Three-Way Comparison**: Validate `External Reference == R4.1 Independent Oracle == Production Engine Result`.
