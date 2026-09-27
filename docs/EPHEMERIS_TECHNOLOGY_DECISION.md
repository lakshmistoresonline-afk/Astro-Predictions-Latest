# EPHEMERIS TECHNOLOGY DECISION ("Astrovision")

## 1. Current Engine Defects
- `astronomical_engine.py` currently relies on simplified Meeus trigonometric approximations.
- Planetary latitude is calculated via synthetic formula: `math.sin(math.radians(lon_val)) * 2.5`.
- Retrograde status is calculated via periodic modulo check conditions (e.g., `(julian_day % 116) < 22`).
- Ayanamsha uses linear epoch approximation (`23.85 + 0.01397 * (...)`).

## 2. Candidate A — Swiss Ephemeris (`pyswisseph`)
- **Accuracy**: Arcsecond-level ephemeris precision based upon JPL DE431/DE440 planetary ephemerides.
- **Capabilities**: Full geocentric/topocentric positions, speeds, retrograde state, houses, ayanamsha modes (Lahiri, Raman, etc.), and node calculations.
- **Licensing**: GNU General Public License (GPL) / GNU Affero General Public License (AGPL) depending on distribution context, requiring commercial licensing for proprietary closed-source commercial SaaS deployment if source code is not disclosed under GPL/AGPL terms.
- **Commercial Implications**: Requires commercial license acquisition for closed-source deployment or open-sourcing project under GPL/AGPL.
- **Deployment Implications**: Requires binary C extension (`pyswisseph`) compilation/wheel matching Python runtime architecture across Windows/Linux/macOS.

## 3. Candidate B — Skyfield (`skyfield`)
- **Accuracy**: High-precision ephemeris powered by JIT / NumPy vectorization using JPL ephemeris files (`de421.bsp`).
- **Capabilities**: True positions, velocities, vector astronomy, topocentric corrections.
- **Licensing**: MIT License (Permissive, open commercial use).
- **Commercial Implications**: 100% commercially permissive without source disclosure requirements.
- **Deployment Implications**: Requires downloading ephemeris binary file (`de421.bsp` ~17MB) at runtime or packaging it.

## 4. Candidate C — Custom Rigorous Meeus Pure-Python Engine
- **Accuracy**: Arc-minute accuracy using full Jean Meeus "Astronomical Algorithms" planetary perturbation series (VSOP87/ELP2000 approximations).
- **Capabilities**: Fully pure Python, no C compiler dependencies, zero binary wheel issues.
- **Licensing**: MIT / PSF Permissive.
- **Commercial Implications**: Fully permissive for commercial SaaS.
- **Deployment Implications**: Extremely lightweight, cross-platform pure Python.

## 5. Accuracy Comparison
- Candidate A (Swiss Ephemeris): Arcsecond (~0.0001°).
- Candidate B (Skyfield): Arcsecond (~0.0001°).
- Candidate C (Pure-Python Meeus Series): Arc-minute (~0.01°).

## 6. License Comparison
- Candidate A: GPL / AGPL (Copyleft / Commercial restriction).
- Candidate B: MIT (Permissive).
- Candidate C: MIT (Permissive).

## 7. Commercial Deployment Implications
- Swiss Ephemeris requires commercial licensing for closed-source SaaS. Skyfield and Custom Meeus are MIT licensed and commercially unrestricted.

## 8. Selected Technology
- **Selected Engine**: Candidate B (`skyfield` / JPL Ephemeris) combined with rigorous Meeus algorithms, or Candidate C (Rigorous pure-Python Meeus series with true velocity-derived retrograde and true coordinate transformations) for zero-dependency portability. For Astrovision's multi-platform pure Python backend without C binary compilation blockers on Windows, a rigorous pure-Python ephemeris framework or `skyfield` is ideal.

## 9. Reason for Selection
- To maintain 100% pure-Python deployment reliability across Windows/Linux without C-compiler/wheel mismatch failures while replacing synthetic modulo approximations with rigorous trigonometric series.

## 10. Implementation Plan
1. Implement rigorous Meeus planetary perturbation series with true velocity derivation and coordinate-based latitude without synthetic multipliers.
2. Establish independent numerical validation tests against reference ephemeris values.

## 11. Phase 1A Gate
TECHNOLOGY DECISION COMPLETE
