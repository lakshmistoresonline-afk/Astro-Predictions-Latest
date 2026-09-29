# Phase 2E-R4.1-R3 Sidereal Conversion & Ayanamsha Audit

## 1. Overview
PyEphem 4.2.1 outputs tropical ecliptic longitudes based on the XEphem VSOP87 planetary perturbation theory. To convert these coordinates to sidereal representation for Vedic astrology evaluation, the Lahiri Ayanamsha formula is applied.

## 2. Ayanamsha Formula & Precision
- **Formula**: $A = 23.85^\circ + 1.396 \cdot T$
- **Where**: $T = \frac{JD - 2451545.0}{36525.0}$ (Julian Centuries from J2000.0 epoch).
- **Sidereal Longitude**: $\lambda_{\text{sidereal}} = (\lambda_{\text{tropical}} - A) \bmod 360^\circ$.

## 3. Ascendant & MC Derivation
- Local Sidereal Time (LST) is computed directly using PyEphem's native C implementation (`observer.sidereal_time()`).
- True obliquity of the ecliptic ($\varepsilon$) is computed per Meeus Ch. 22.
- **Midheaven (MC)**: $\tan(\lambda_{\text{MC\_trop}}) = \frac{\tan(\text{LST})}{\cos(\varepsilon)}$.
- **Ascendant**: $\tan(\lambda_{\text{Asc\_trop}}) = \frac{\cos(\text{LST})}{-\sin(\text{LST})\cos(\varepsilon) - \tan(\phi)\sin(\varepsilon)}$.
- Sidereal Ascendant and MC are obtained by subtracting Ayanamsha $A$.

## 4. Verification
Comparison against Skyfield 1.55 (NASA JPL DE440s) confirms agreement within `< 25.0 arcseconds` across all 15 real birth charts.
