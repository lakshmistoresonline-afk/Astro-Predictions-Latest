# Phase 2E-R4.1-R12-R1 Production / Oracle Separation Architecture

## 1. Bi-Directional Isolation Architecture

```
                                  BirthInput
                                       │
                     ┌─────────────────┴─────────────────┐
                     │                                   │
                     ▼                                   ▼
              PRODUCTION PATH                    INDEPENDENT ORACLE
                     │                                   │
     (Zero Oracle / Reference Imports)           (Zero Production Imports)
                     │                                   │
                     ▼                                   ▼
             Production Engine                   Independent Oracle
       (ShadbalaEngine, AshtakavargaEngine)     (r4_calculate_shadbala, r4_independent_bav)
                     │                                   │
                     ▼                                   ▼
             Production Result                       Oracle Result
                     │                                   │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                            3-WAY RECONCILIATION LAYER
                                       │
                                       ▼
                             Immutable Reference Data
```

## 2. Strict Isolation Invariants
1. **Production Adapters**: `apps/api/tests/certification/production_shadbala.py` and `production_bav.py` import ONLY `apps.api.engines.*`. They return production records containing ONLY `production_value` calculated by real production engines.
2. **Oracle Modules**: `apps/api/tests/oracles/phase_2e_r4_1/independent_*.py` import ZERO `apps.api.engines.*` modules.
3. **Reconciliation Layer**: The certification runner `run_phase_2e_r4_1_r7_r12_certification.py` collects production results, oracle results, and reference fixture data independently and executes 3-way deltas:
   - `production_vs_oracle_delta`
   - `oracle_vs_reference_delta`
   - `production_vs_reference_delta`
