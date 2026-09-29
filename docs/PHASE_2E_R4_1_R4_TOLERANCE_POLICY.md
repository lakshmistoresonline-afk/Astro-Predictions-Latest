# Phase 2E-R4.1-R4 Numerical Tolerance Policy

## 1. Astronomical Ephemeris Cross-Check
- **Quantity**: Planetary Longitudes, Ascendant, Midheaven (MC).
- **Tolerance Limit**: `< 120.0 arcseconds` (2 arcminutes / 0.033°).
- **Justification**: VSOP87 perturbation series (PyEphem) vs Chebyshev DE421 numerical integration (Skyfield) naturally vary by 5 to 30 arcseconds due to orbital perturbation truncation differences.
- **Enforcement**: Tested via `reference_source/cross_check_dual_ephemeris.py` and asserted in `test_r4_1_oracle.py`.

## 2. Shadbala Subcomponent Strength Comparison
- **Quantity**: Shashtiamsas (raw strength values).
- **Tolerance Limit**: `<= 0.03 shashtiamsas`.
- **Justification**: Accommodates 64-bit floating point rounding at the 2nd decimal place across complex angular interpolations.
- **Enforcement**: Asserted in `test_r4_1_oracle.py` across all 17 subcomponents.

## 3. Ashtakavarga BAV / SAV
- **Quantity**: Bindu counts (integers).
- **Tolerance Limit**: **EXACT EQUALITY** (`0.0` tolerance).
- **Enforcement**: Exact integer comparison across all 56 BAV cells and 12 SAV houses.
