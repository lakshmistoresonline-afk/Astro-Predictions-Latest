# Phase 2E-R4.1-R4 Reference Quarantine Report

## 1. Quarantined Artifacts
- **Location**: `reference_source/quarantine/r4_1_r3_invalid/`
- **Quarantined Files**: All 20 JSON datasets previously generated in `reference_source/raw_reference/`.

## 2. Reason for Quarantine
1. The cross-check script invoked production `build_canonical_vedic_chart()`, creating an illegal circular dependency.
2. The standalone Ascendant/MC calculation in PyEphem script suffered from 180° quadrant wrapping ambiguities, resulting in non-reconciled Ascendant/MC reference values.

## 3. Replacement Plan
1. Standalone PyEphem 4.2.1 extractor in `reference_source/pyephem_reference/standalone_pyephem.py`.
2. Standalone Skyfield 1.55 (DE440s) extractor in `reference_source/skyfield_reference/standalone_skyfield.py`.
3. Standalone dual-ephemeris cross-check runner in `reference_source/cross_check_dual_ephemeris.py`.
4. Neither script imports `apps.api.engines.*`.
