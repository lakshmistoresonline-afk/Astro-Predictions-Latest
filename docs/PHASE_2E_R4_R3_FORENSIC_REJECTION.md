# Phase 2E-R4 Forensic Rejection of Phase 2E-R3 Oracle & Fixtures

## 1. Forensic Audit Summary
A forensic audit of the Phase 2E-R3 commit (`4c61f12f232dc5584f35161385198f27986ca970`) revealed that while the production Shadbala and Ashtakavarga engines were correctly expanded, the fixture generation process was **circular**:

1. **Circular Astronomy & Varga Calls**: The R3 script `generate_r3_fixtures.py` imported `build_canonical_vedic_chart` from `apps.api.engines.vedic` and `VargaEngine` from `apps.api.engines.varga`.
2. **Circular Oracle Module Re-use**: The fixture generator imported `independent_bav`, `independent_sav`, and Shadbala rule functions directly from previous test oracle packages (`apps.api.tests.oracles.phase_2e_ashtakavarga.rules` and `apps.api.tests.oracles.phase_2e_shadbala.rules`).
3. **Contaminated Expected Values**: Because expected values were dynamically generated using existing codebase components rather than completely independent mathematical derivation from raw external inputs, the expected values were contaminated.

## 2. Rejection & Remediation Decision
- **Rejection**: All R3 expected value JSONs in `apps/api/tests/fixtures/phase_2e_r3_expected/` are rejected as certification proof.
- **R4 Remediation Architecture**:
  1. Build a zero-trust, decoupled oracle package in `apps/api/tests/oracles/phase_2e_r4/`.
  2. Implement pure, self-contained mathematical calculations for Astronomy (Julian Date, tropical-to-sidereal, declination), Vargas (D1 to D30), Ashtakavarga, and Shadbala without importing ANY production modules (`apps.api.engines.*`).
  3. Pre-calculate and freeze immutable input and expected fixture JSON files in `apps/api/tests/fixtures/phase_2e_r4_inputs/` and `apps/api/tests/fixtures/phase_2e_r4_expected/`.
  4. Perform three-way validation: `Frozen Expected == R4 Independent Oracle == Production Engine Result`.
