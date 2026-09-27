# Ephemeris Technology Decision Audit ("Astrovision")

## 1. Executive Conclusion
The previous Phase 1A decision document (`docs/EPHEMERIS_TECHNOLOGY_DECISION.md`) proposed a "pure-Python Meeus perturbation engine" (Candidate C) without independent numerical benchmark verification or formal license provenance audits. Under forensic re-audit, Candidate C remains **unproven** at arcsecond precision, and Candidate A (Swiss Ephemeris / `pyswisseph`) presents GPL/AGPL copyleft and binary deployment constraints. Therefore, the technology decision is currently classified as **DECISION NOT VERIFIED**.

## 2. Existing Decision Audit
- **Claimed Precision**: "Arc-minute accuracy" for Candidate C.
- **Verification Status**: UNVERIFIED. No independent arcsecond comparison against JPL DE431/DE440 ephemerides has been executed.
- **Licensing**: Candidate A (Swiss Ephemeris) requires rigorous commercial licensing review for proprietary SaaS. Candidate Cprovenance needs formal source review.

## 3. Astrovision Astronomy Requirements
- Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Rahu, Ketu.
- Geocentric/sidereal longitude, latitude, distance, velocity, retrograde state.
- Lahiri ayanamsha, Ascendant, MC, house cusps, local sidereal time, and historical DST/timezone handling across multi-century date ranges.

## 4. Candidate Comparison
| Candidate | Precision | License | Binary Dependency | Commercial SaaS Risk |
|---|---|---|---|---|
| A. Swiss Ephemeris (`pyswisseph`) | Arcsecond (~0.0001°) | GPL / AGPL | Yes (C Extension) | High (Copyleft / Commercial Dual License) |
| B. Skyfield (`skyfield` + JPL) | Arcsecond (~0.0001°) | MIT | No (Pure Python + Data File) | Low (Permissive) |
| C. Custom Meeus (Pure Python) | Arc-minute (~0.01°) | MIT / PSF | No (Pure Python) | Low (Permissive) |

## 5. Licensing/Provenance Matrix
- Swiss Ephemeris: GPL/AGPL license with commercial licensing options.
- Skyfield: MIT license.
- Custom Meeus: MIT / PSF license.

## 6. Final Gate Status
DECISION NOT VERIFIED
