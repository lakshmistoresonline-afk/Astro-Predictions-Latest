# Phase 2E-R4.1-R12-R1 Synthetic Boundary Fixture Policy Report

## 1. Synthetic Boundary Fixture Classification (`REF_016` through `REF_020`)
Fixtures `REF_016` through `REF_020` are synthetic mathematical boundary test fixtures (e.g. `Sun Exaltation Boundary` where Sun longitude = 10.0° Aries, Moon = 0.0° Aries).

## 2. Policy & Execution Guarantees
1. **Zero Production Contamination**: Synthetic longitudes in `REF_016`..`REF_020` are **NEVER** injected into the production chart builder. `BirthInput` evaluates real physical astronomy on 2000-01-01 (Sun in Sagittarius at ~255°).
2. **Explicit Classification**: The 595 synthetic boundary records are explicitly categorized and reported separately from the 1,785 real astronomical birth records.
3. **Boundary Oracle Validation**: Independent mathematical boundary oracles in `independent_shadbala.py` and `independent_ashtakavarga.py` validate the mathematical boundary rules.

## 3. Matrix Output Accounting
- **Total Matrix Records**: 2,380
- **Real Astronomical Reconciliations**: 1,785
- **Synthetic Boundary Evaluations**: 595
