# Phase 2E-R4.1 Unverified Reference Audit & Quarantine Notice

## 1. Audit Finding
In the previous R4.1 iteration, fixture generator scripts wrote static sidereal longitudes directly into `apps/api/tests/fixtures/phase_2e_r4_1_reference/` with the label `"Standalone Swiss Ephemeris / Meeus Verified Reference Table"`.

However, no standalone external ephemeris extraction program was executed or included in the repository to demonstrate the actual derivation of those numbers from an external software source.

Therefore, the previous reference dataset was classified as **UNVERIFIED_REFERENCE_DATA** and quarantined.

## 2. Quarantine Action
All files previously located in `apps/api/tests/fixtures/phase_2e_r4_1_reference/` have been moved to `apps/api/tests/fixtures/phase_2e_r4_1_unverified_reference/`.

## 3. Remediation Strategy
1. A standalone ephemeris extraction runner (`reference_source/standalone_ephemeris_extractor.py`) has been constructed. It executes standalone ephemeris libraries (PyEphem 4.2.1 and Skyfield 1.55 JPL DE440s) outside the Astrovision application package (with 0 imports from `apps.api.engines.*`).
2. Every generated reference fixture is stored in `reference_source/raw_reference/` and copied to `apps/api/tests/fixtures/phase_2e_r4_1_reference/` with complete extraction logs and cryptographic SHA-256 signatures.
3. A 5-chart cross-check comparing PyEphem (XEphem) vs Skyfield (DE440s) is documented in `docs/PHASE_2E_R4_1_EPHEMERIS_CROSS_CHECK.md`.
