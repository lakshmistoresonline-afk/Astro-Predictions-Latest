# Phase 2E-R4.1 Expected Value Integrity Manifest

## Frozen Expected Fixture Hashes
Every frozen expected JSON file in `apps/api/tests/fixtures/phase_2e_r4_1_expected/` contains a cryptographic `integrity_hash` computed over the canonical serialized JSON payload.

## Verification Protocol
1. Input files in `apps/api/tests/fixtures/phase_2e_r4_1_reference/` contain zero production engine outputs.
2. Expected JSON files in `apps/api/tests/fixtures/phase_2e_r4_1_expected/` are generated purely via `generate_expected.py` using `apps/api/tests/oracles/phase_2e_r4/` independent functions.
3. Tests in `test_r4_1_oracle.py` verify that `Frozen Expected == Independent Oracle == Production Engine Result` for all 20 fixtures.
