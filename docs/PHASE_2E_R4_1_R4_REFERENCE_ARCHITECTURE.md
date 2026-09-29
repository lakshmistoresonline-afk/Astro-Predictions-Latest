# Phase 2E-R4.1-R4 Reference Architecture

## Decoupled Three-Layer Validation Pipeline
```
      [Inputs Specification] (reference_source/inputs/*.json)
                 │
  ┌──────────────┴──────────────┐
  ▼                             ▼
PyEphem 4.2.1               Skyfield 1.55
(XEphem C Core)            (NASA JPL DE421)
  │                             │
  └──────────────┬──────────────┘
                 ▼
     [Dual Ephemeris Cross-Check] (reference_source/cross_check_results.json)
                 │
                 ▼
  [Pure R4.1 Independent Oracle] (apps/api/tests/oracles/phase_2e_r4_1/)
                 │
                 ▼
   [Frozen Expected JSONs] (apps/api/tests/fixtures/phase_2e_r4_1_expected/*.json)
                 │
                 ▼
  [Astrovision Production Engine] (apps/api/engines/strength/)
                 │
                 ▼
   [Three-Way Validation: Frozen == Oracle == Production]
```

## Key Properties
- Zero calls to `apps.api.engines.*` during reference extraction or oracle calculation.
- Reference input data independently specified and stored in `reference_source/inputs/`.
- Dual ephemeris cross-check enforces sub-arcminute agreement (< 120 arcseconds) between PyEphem 4.2.1 and Skyfield 1.55.
