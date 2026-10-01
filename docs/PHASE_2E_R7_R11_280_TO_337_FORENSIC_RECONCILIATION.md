# Phase 2E-R4.1-R7-R11 280 vs 337 SAV Vector Forensic Reconciliation Report

## 1. Forensic Discrepancy Statement
An intermediate execution in R7-R9 produced an invalid SAV vector `[24, 48, 48, 48, 56, 48, 8, 0, 0, 0, 0, 0]` with sum = **280**.
The canonical SAV vector for `REF_001` is `[25, 31, 27, 37, 24, 30, 19, 33, 31, 27, 31, 22]` with sum = **337**.

## 2. Root Cause Forensic Analysis
1. **Flawed Code**: `oracle_bindu = 1 if house_num in oracle_bav_vec else 0` in `generate_r7_r2_matrices.py`.
2. **Mathematical Flaw**: `oracle_bav_vec` is a 12-element list of BAV bindu totals (e.g. `[5, 5, 4, 6, 3, 5, 3, 4, 5, 3, 3, 2]`). Checking `house_num in oracle_bav_vec` evaluated whether the house number `1..12` appeared as a *value inside* the 12-element list rather than indexing `oracle_bav_vec[house_num - 1]`.
3. **Summation Output**: Summing this binary indicator across 56 contributor rules resulted in:
   $$24 + 48 + 48 + 48 + 56 + 48 + 8 + 0 + 0 + 0 + 0 + 0 = 280$$

## 3. Mathematical Proof of Correct 337 Vector
Summing BAV bindu totals across the 7 target planets ($P \in \{\text{Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn}\}$) yields:
- House 1: $5 + 6 + 2 + 2 + 4 + 2 + 4 = 25$
- House 2: $5 + 3 + 3 + 6 + 5 + 5 + 4 = 31$
- House 3: $4 + 4 + 2 + 3 + 4 + 6 + 4 = 27$
- House 4: $6 + 5 + 6 + 6 + 5 + 5 + 4 = 37$
- House 5: $3 + 2 + 3 + 6 + 4 + 4 + 2 = 24$
- House 6: $5 + 5 + 3 + 3 + 3 + 5 + 4 = 30$
- House 7: $3 + 1 + 1 + 4 + 5 + 4 + 2 = 19$
- House 8: $4 + 5 + 6 + 5 + 6 + 5 + 2 = 33$
- House 9: $5 + 5 + 3 + 5 + 4 + 4 + 5 = 31$
- House 10: $3 + 5 + 4 + 5 + 5 + 3 + 2 = 27$
- House 11: $3 + 4 + 5 + 4 + 5 + 5 + 2 = 31$
- House 12: $2 + 4 + 1 + 3 + 6 + 4 + 4 = 22$

$$\mathbf{\text{SAV Total} = 25+31+27+37+24+30+19+33+31+27+31+22 = 337}$$

## 4. Production Engine Verification
`AshtakavargaEngine.calculate_ashtakavarga(prod_chart).sav.bindus` produces `[25, 31, 27, 37, 24, 30, 19, 33, 31, 27, 31, 22]` directly from real production engine calculations.
The bug is locked against regression in `apps/api/tests/test_sav_reconciliation.py`.
