# Phase 2E-R4 Expected Value Provenance & SHA-256 Hashes

## Provenance
All 15 frozen JSON fixtures in `apps/api/tests/fixtures/phase_2e_r4_expected/` contain independently calculated expected values.

- Creator: R4 Independent Oracle (`apps/api/tests/oracles/phase_2e_r4/`)
- Input Source: Phase 2A Canonical Astronomy (`build_canonical_vedic_chart`) for birth profiles; synthetic angular boundaries for fixtures 11-15.
- Calculation Method: Pure mathematical functions operating on `IndependentChart` data structures.
- Precision: 64-bit floating point precision, rounded to 2 decimal places for shashtiamsas and 6 decimal places for longitudes.

## Three-Way Validation
Every test in `test_r4_oracle.py` enforces:
`Frozen Expected == R4 Independent Oracle == Production Engine Result` within `<= 0.03` shashtiamsas.
