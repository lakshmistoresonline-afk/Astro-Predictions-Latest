# Phase 2E-R4.1-R3 Mutation Execution Report

## Executed Production Rule Mutations

| Mutation ID | Component | Original Rule | Mutated Rule | Expected Failing Assertion | Actual Failure | Result |
|---|---|---|---|---|---|---|
| `MUT_001_UCCHA_BALA` | Sthana Bala (Uccha) | Sun debilitation at 190.0° | Sun debilitation at 195.0° | `Uccha Bala == 9.49` | `Uccha Bala == 7.82` | **DETECTED** |
| `MUT_002_BAV_JUPITER` | Ashtakavarga BAV | Lagna gives 9 bindus to Jupiter BAV | Lagna gives 8 bindus to Jupiter BAV | `SAV Sum == 337` | `SAV Sum == 336` | **DETECTED** |
| `MUT_003_DIG_BALA` | Dig Bala | Sun Dig Bala = 38.33 shashtiamsas | Sun Dig Bala forced to 0.0 shashtiamsas | `Dig Bala == 38.33` | `Dig Bala == 0.0` | **DETECTED** |

Mutation Detection Rate: **100%**. Output logged to `docs/PHASE_2E_R4_1_MUTATION_RESULTS.json`.
