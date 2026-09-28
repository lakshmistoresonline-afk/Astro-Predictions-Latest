# Phase 2E-R2 Mutation Report

| Subcomponent / Rule | Mutation Injected | Expected Test Failure | Result |
|---|---|---|---|
| **Uccha Bala** | Changed Sun debilitation longitude to 195.0° | `test_shadbala_oracle_exaltation_boundary` | **DETECTED** |
| **Dig Bala** | Removed MC power house calculation for Sun/Mars | `test_shadbala_oracle_dig_bala_boundary` | **DETECTED** |
| **Nathonnatha Bala** | Inverted diurnal/nocturnal assignment | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Cheshta Bala** | Forces `30.0` for retrograde planets | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Drik Bala** | Inverted benefic/malefic aspect sign modifier | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **BAV Matrix** | Removed 12th house contribution to Jupiter BAV from Lagna | `test_ashtakavarga_oracle_subramanian` | **DETECTED** |

**Mutation Score**: 100%
