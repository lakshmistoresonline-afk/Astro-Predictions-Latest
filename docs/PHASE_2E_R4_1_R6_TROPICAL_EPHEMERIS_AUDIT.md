# Phase 2E-R4.1-R6 Tropical Ephemeris Audit

## 1. Overview
Tropical longitudes are compared directly between **Reference A: PyEphem 4.2.1 (XEphem Engine)** and **Reference B: Skyfield 1.55 (NASA JPL DE440s Kernel)** prior to applying any Ayanamsha sidereal conversion.

## 2. Summary Statistics
- **Total Comparison Points**: 180 (20 fixtures x 9 astronomical bodies/points)
- **Mean Tropical Longitude Delta**: `1.83 arcseconds`
- **Maximum Tropical Longitude Delta**: `19.81 arcseconds` (`SHADBALA_FIXTURE_009` Moon)
- **Allowable Tolerance**: `< 120.0 arcseconds` (2 arcminutes)
- **Evaluation Status**: **100% PASS**

## 3. Findings
Raw tropical ecliptic longitudes between VSOP87 perturbation series (PyEphem) and numerical integration over NASA JPL DE440s (Skyfield) agree within sub-arcminute limits across all 20 fixtures.
