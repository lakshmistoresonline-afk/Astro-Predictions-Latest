# Phase 2E-R4.1-R5 Forensic Audit of 19.81 Arcsecond Moon Case

## 1. Case Details
- **Fixture ID**: `SHADBALA_FIXTURE_009` (Singapore Native)
- **Birth UTC**: `2010-08-09T10:00:00Z`
- **Julian Day Number**: `2455417.916667`
- **Lahiri Ayanamsha**: `23.998024°`

## 2. Numerical Comparison
- **PyEphem 4.2.1 (XEphem Engine)**:
  - Tropical Longitude: `126.471498°` (Leo 6° 28' 17.39")
  - Sidereal Longitude: `102.473474°` (Cancer 12° 28' 24.51")
- **Skyfield 1.55 (NASA JPL DE420/DE421/DE440s Kernel)**:
  - Tropical Longitude: `126.477002°` (Leo 6° 28' 37.21")
  - Sidereal Longitude: `102.478978°` (Cancer 12° 28' 44.32")
- **Absolute Delta**: `0.005504°` = **`19.8144 arcseconds`**.
- **Allowable Tolerance**: `< 120.0 arcseconds` (2 arcminutes).
- **Evaluation Status**: **PASS** (19.81" is well within the 120.0" tolerance).

## 3. Mathematical Cause
The Moon exhibits the fastest apparent motion of any celestial body (~13.2° per day or ~0.55 arcseconds per second). The 19.81 arcsecond variance between PyEphem and Skyfield is caused by differences in lunar perturbation theories:
- **PyEphem (XEphem Core)**: Employs truncated VSOP87 analytical series for lunar perturbation and libration.
- **Skyfield (JPL DE440s)**: Numerically integrates Chebyshev polynomials fitting lunar laser ranging (LLR) measurements directly.
