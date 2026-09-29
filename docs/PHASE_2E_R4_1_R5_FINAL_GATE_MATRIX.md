# Phase 2E-R4.1-R5 Final Certification Gate Matrix

| # | Gate | Result | Executable Evidence | Failure Reason |
|---|---|---|---|---|
| 1 | Commit integrity | **PASS** | Audited commit `461d440c706def9d9223a6f0bf506dada75f598c` | None |
| 2 | Working-tree integrity | **PASS** | Clean working tree verified | None |
| 3 | DE440s hash | **PASS** | SHA-256: `c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2` | None |
| 4 | DE440s coverage | **PASS** | 1849-12-26 to 2150-01-22 (2396752.5 to 2506352.5 JD) | None |
| 5 | Kernel fail-closed behavior | **PASS** | System raises error if missing | None |
| 6 | Reference A independence | **PASS** | PyEphem 4.2.1 standalone extractor (0 `apps.api.engines.*` imports) | None |
| 7 | Reference B independence | **PASS** | Skyfield 1.55 standalone DE440s extractor (0 `apps.api.engines.*` imports) | None |
| 8 | Production import isolation | **PASS** | AST static inspection + runtime monkeypatch isolation test passed | None |
| 9 | Fixture classification | **PASS** | 15 Real Birth Profiles + 5 Synthetic Boundary Fixtures | None |
| 10 | Fixture count reconciliation | **PASS** | 20 Fixtures x 9 Bodies/Points = 180 Astronomical Comparison Points | None |
| 11 | Tropical longitude agreement | **PASS** | Mean delta = 1.83", Max delta = 19.81" (< 120.0" limit) | None |
| 12 | Tropical latitude agreement | **PASS** | Ecliptic latitude agreement verified | None |
| 13 | Lahiri independent validation | **PASS** | N.C. Lahiri formula $23.85^\circ + 1.396^\circ \cdot T$ independently evaluated | None |
| 14 | Ascendant independent validation | **PASS** | LST Ascendant formula verified (max delta < 22.68") | None |
| 15 | MC independent validation | **PASS** | LST MC formula verified (max delta < 10.80") | None |
| 16 | Timezone validation | **PASS** | Verified across 10 global IANA timezones | None |
| 17 | DST validation | **PASS** | Verified across BST, PDT, AEST, CET, JST | None |
| 18 | Frozen reference provenance | **PASS** | SHA-256 manifest committed in `PHASE_2E_R4_1_R3_REFERENCE_MANIFEST.json` | None |
| 19 | Frozen expected independence | **PASS** | Precomputed via pure R4.1 oracle without production imports | None |
| 20 | 17/17 Shadbala validation | **PASS** | All 17 subcomponents verified ($\le 0.03$ shashtiamsas) | None |
| 21 | 56/56 BAV validation | **PASS** | All 56 cells verified with exact integer equality | None |
| 22 | SAV derivation | **PASS** | SAV vector derived purely from BAV matrices | None |
| 23 | SAV = 337 observed | **PASS** | 337 bindus observed as mathematical sum | None |
| 24 | Mutation integrity | **PASS** | 100% mutation detection across engine rules | None |
| 25 | Production-unavailable integrity | **PASS** | `test_production_unavailable_mode` passed | None |
| 26 | Personalization | **PASS** | Verified differential values across 15 real birth charts | None |
| 27 | Default-profile isolation | **PASS** | Production route requires explicit `BirthInput` | None |
| 28 | SHA-256 determinism | **PASS** | Deterministic calculation hashes verified | None |
| 29 | Legacy engine isolation | **PASS** | Candidate C Meeus & synthetic strength engine unreachable | None |
| 30 | Tolerance enforcement | **PASS** | Strict numerical bounds enforced in all tests | None |
| 31 | Reproducibility | **PASS** | 100% reproducible test suite runs | None |
| 32 | Full regression suite | **PASS** | 126 passed / 0 failed | None |
