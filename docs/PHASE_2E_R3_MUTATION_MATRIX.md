# Phase 2E-R3 Mutation Matrix

| Target Component | Mutation Injected | Expected Failing Test | Result |
|---|---|---|---|
| **Uccha Bala** | Changed Sun debilitation point from 190.0° to 195.0° | `test_shadbala_oracle_exaltation_boundary` | **DETECTED** |
| **Sapta Vargaja** | Modified Panchadha Maitri score for Adhi Mitra from 22.5 to 20.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Ojha-Yugma** | Inverted gender sign alignment for Venus/Moon | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Kendradi Bala** | Changed Panaphara score from 30.0 to 20.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Drekkana Bala** | Changed male planet 1st drekkana score from 15.0 to 10.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Dig Bala** | Inverted MC power house calculation for Sun/Mars | `test_shadbala_oracle_dig_bala_boundary` | **DETECTED** |
| **Nathonnatha Bala**| Inverted diurnal/nocturnal solar distance assignment | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Paksha Bala** | Inverted malefic/benefic Paksha calculation | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Ayana Bala** | Inverted declination Kranti sign multiplier | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Tribhaga Bala** | Removed Jupiter's constant 60 shashtiamsas assignment | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Vara Bala** | Changed Day Lord score from 45.0 to 40.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Hora Bala** | Changed Hour Lord score from 60.0 to 50.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Masa Bala** | Changed Month Lord score from 30.0 to 25.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Varsha Bala** | Changed Year Lord score from 15.0 to 10.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Cheshta Bala** | Forced `30.0` for retrograde planets | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Naisargika Bala**| Changed Sun natural strength from 60.0 to 50.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Drik Bala** | Inverted benefic/malefic aspect modifier | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Total Aggregation**| Omitted Drik Bala from total sum | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Rupa Conversion** | Changed divisor from 60.0 to 50.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **Strength %** | Changed Sun minimum required Rupas from 5.0 to 6.0 | `test_shadbala_oracle_subramanian` | **DETECTED** |
| **BAV Contributor**| Removed Lagna 12th house contribution to Jupiter BAV | `test_ashtakavarga_oracle_subramanian` | **DETECTED** |
| **SAV Aggregation**| Reduced total SAV sum from 337 to 335 | `test_ashtakavarga_oracle_subramanian` | **DETECTED** |

**Summary**: 22/22 mutations detected (100% mutation coverage).
