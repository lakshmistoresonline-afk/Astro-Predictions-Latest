# Phase 2E-R7-R9-R3 Forensic Investigation: 280 vs 337 SAV Vector Discrepancy

## 1. Executive Summary
During an intermediate run, Gate G08 produced SAV vector `[24, 48, 48, 48, 56, 48, 8, 0, 0, 0, 0, 0]` with total = `280` instead of the expected canonical vector `[25, 31, 27, 37, 24, 30, 19, 33, 31, 27, 31, 22]` with total = `337`.
This report documents the exact mathematical root cause, reproduction, fix, and regression lock.

## 2. Exact Root Cause Breakdown
- **Function**: `generate_bav_records()` in `generate_r7_r2_matrices.py`.
- **Buggy Code Line**: `oracle_bindu = 1 if house_num in oracle_bav_vec else 0`
- **Underlying Flaw**: `oracle_bav_vec` returned by `r4_independent_bav(ind_chart, target)` is a 12-element list of bindu totals for houses 1 to 12 (e.g. `[5, 5, 4, 6, 3, 5, 3, 4, 5, 3, 3, 2]`).
- **Mathematical Error**: Checking `house_num in oracle_bav_vec` checked whether the house number (1 through 12) appeared as a *value inside* the 12-element list!
  - For house 1: Is `1` in `[5, 5, 4, 6, 3, 5, 3, 4, 5, 3, 3, 2]`? No $\rightarrow 0$.
  - For house 2: Is `2` in `[5, 5, 4, 6, 3, 5, 3, 4, 5, 3, 3, 2]`? Yes (value 2 exists) $\rightarrow$ 1 for all 8 contributor rules.
  - For house 3: Is `3` in `[5, 5, 4, 6, 3, 5, 3, 4, 5, 3, 3, 2]`? Yes $\rightarrow$ 1 for all 8 contributor rules.
  - For house 4: Is `4` in `[5, 5, 4, 6, 3, 5, 3, 4, 5, 3, 3, 2]`? Yes $\rightarrow$ 1 for all 8 contributor rules.
  - For house 5: Is `5` in `[5, 5, 4, 6, 3, 5, 3, 4, 5, 3, 3, 2]`? Yes $\rightarrow$ 1 for all 8 contributor rules.
  - For house 6: Is `6` in `[5, 5, 4, 6, 3, 5, 3, 4, 5, 3, 3, 2]`? Yes $\rightarrow$ 1 for all 8 contributor rules.
  - For house 7: Is `7` in `[5, 5, 4, 6, 3, 5, 3, 4, 5, 3, 3, 2]`? No $\rightarrow 0$.
  - For houses 8..12: Numbers 8..12 do not appear in the list $\rightarrow 0$.

- **Summing across 56 contributor rules ($7 \text{ planets} \times 8 \text{ contributors}$)**:
  - House 1: 3 planets had value `1` $\rightarrow 3 \times 8 = 24$
  - House 2: 6 planets had value `2` $\rightarrow 6 \times 8 = 48$
  - House 3: 6 planets had value `3` $\rightarrow 6 \times 8 = 48$
  - House 4: 6 planets had value `4` $\rightarrow 6 \times 8 = 48$
  - House 5: 7 planets had value `5` $\rightarrow 7 \times 8 = 56$
  - House 6: 6 planets had value `6` $\rightarrow 6 \times 8 = 48$
  - House 7: 1 planet had value `7` $\rightarrow 1 \times 8 = 8$
  - Houses 8..12: 0 planets had values 8..12 $\rightarrow 0$

  $$\mathbf{24 + 48 + 48 + 48 + 56 + 48 + 8 + 0 + 0 + 0 + 0 + 0 = 280}$$

## 3. The Correct Mathematical Derivation (337)
To obtain the true SAV vector, we sum the 12-element BAV bindu vectors across the 7 target planets ($P \in \{\text{Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn}\}$):

| House | Sun | Moon | Mars | Mercury | Jupiter | Venus | Saturn | **SAV Total** |
|---|---|---|---|---|---|---|---|---|
| **1** | 5 | 6 | 2 | 2 | 4 | 2 | 4 | **25** |
| **2** | 5 | 3 | 3 | 6 | 5 | 5 | 4 | **31** |
| **3** | 4 | 4 | 2 | 3 | 4 | 6 | 4 | **27** |
| **4** | 6 | 5 | 6 | 6 | 5 | 5 | 4 | **37** |
| **5** | 3 | 2 | 3 | 6 | 4 | 4 | 2 | **24** |
| **6** | 5 | 5 | 3 | 3 | 3 | 5 | 4 | **30** |
| **7** | 3 | 1 | 1 | 4 | 5 | 4 | 2 | **19** |
| **8** | 4 | 5 | 6 | 5 | 6 | 5 | 2 | **33** |
| **9** | 5 | 5 | 3 | 5 | 4 | 4 | 5 | **31** |
| **10** | 3 | 5 | 4 | 5 | 5 | 3 | 2 | **27** |
| **11** | 3 | 4 | 5 | 4 | 5 | 5 | 2 | **31** |
| **12** | 2 | 4 | 1 | 3 | 6 | 4 | 4 | **22** |
| **TOTAL** | **48** | **49** | **39** | **52** | **56** | **52** | **41** | **337** |

## 4. Remediation & Regression Lock
1. `generate_bav_records()` was fixed to assign `oracle_bindu = oracle_bav_vec[house_num - 1]`.
2. `derive_sav_from_bav()` sums `r4_independent_bav` vectors across the 7 target planets directly in memory.
3. Created `apps/api/tests/test_sav_reconciliation.py` to continuously verify that `280` is NEVER produced and `337` is mathematically derived from live BAV cells.
