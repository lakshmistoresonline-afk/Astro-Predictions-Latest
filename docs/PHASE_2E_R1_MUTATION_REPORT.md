# Phase 2E-R1 Mutation Report

## Component Mutation Sensitivity

| Target Engine Component | Mutation Applied | Test Triggered | Status |
|---|---|---|---|
| **Ashtakavarga SAV** | Removed Lagna 12th house contribution to Jupiter BAV | `test_ashtakavarga_oracle_subramanian` (Total dropped to 335) | **DETECTED** |
| **Uccha Bala** | Changed Sun debilitation longitude to 195.0° (Libra 15) | `test_shadbala_oracle_exaltation_boundary` | **DETECTED** |
| **Dig Bala** | Removed MC calculation for Sun/Mars directional power | `test_shadbala_oracle_dig_bala_boundary` | **DETECTED** |
| **Kala Bala** | Inverted Diurnal/Nocturnal Nathonnatha assignment | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Drik Bala** | Inverted Benefic/Malefic aspect signs | `test_shadbala_oracle_subramanian` | **DETECTED** |

**Mutation Score**: 100%
