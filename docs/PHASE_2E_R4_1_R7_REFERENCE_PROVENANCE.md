# Phase 2E-R4.1-R7 Reference Provenance & Integrity

## 1. Reference Data Sourcing
- **Reference A**: PyEphem 4.2.1 (XEphem C Ephemeris Core).
- **Reference B**: Skyfield 1.55 (NASA JPL DE440s Kernel).
- **Kernel File**: `apps/api/engines/astronomy/de440s.bsp` (Size: 32,726,016 bytes, SHA-256: `c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2`).
- **Inputs**: Stored in `reference_source/inputs/`.
- **Raw Reference Storage**: `reference_source/pyephem_reference/` and `reference_source/skyfield_reference/`.
- **Manifest**: `PHASE_2E_R4_1_R3_REFERENCE_MANIFEST.json`.
- **Production Imports**: **0** (0 imports from `apps.api.engines.*`).
