# Phase 2A: Canonical Vedic Chart Foundation Architecture & Specification

## 1. Executive Summary

This document defines the architecture, coordinate conventions, precision rules, and mathematical methodologies for the **Canonical Vedic Chart Foundation** (Phase 2A) built on top of the approved Skyfield 1.55 + NASA JPL DE440s ephemeris provider.

---

## 2. Layered Architecture & Source Separation

```
+-------------------------------------------------------------------------+
|                       CANONICAL VEDIC CHART                             |
|      (Rashi, Nakshatra, Pada, Ascendant, MC, Whole Sign Houses)         |
+-------------------------------------------------------------------------+
                                   ^
                                   | (Consumes Sidereal Placements)
+-------------------------------------------------------------------------+
|                  VEDIC MATHEMATICS ENGINE LAYER                         |
|     (apps/api/engines/vedic/rashi.py, nakshatra.py, houses.py)          |
+-------------------------------------------------------------------------+
                                   ^
                                   | (Consumes Astronomical State)
+-------------------------------------------------------------------------+
|                       TIME NORMALIZATION LAYER                          |
|         (Local Civil Time -> IANA Timezone -> UTC -> Julian Day)        |
+-------------------------------------------------------------------------+
                                   ^
                                   | (Consumes Raw Ephemeris Data)
+-------------------------------------------------------------------------+
|                     ASTRONOMY PROVIDER LAYER                            |
| (Skyfield 1.55 + NASA JPL DE440s: apps/api/engines/astronomy/)          |
+-------------------------------------------------------------------------+
```

### Strict Source Separation Rule
Vedic modules MUST NOT call Skyfield or `jplephem` directly. All planetary calculations are mediated exclusively through `BaseAstronomyProvider` (`SkyfieldJPLProvider`).

---

## 3. Coordinate Conventions & Astronomical Definitions

- **Ephemeris Standard**: NASA JPL DE440s (`de440s.bsp`), covering 1849-12-26 through 2150-01-22.
- **Geocentric vs Topocentric**: Planetary longitudes are geocentric ecliptic longitudes in the ICRF / J2000 reference frame.
- **Orbital Velocities & Retrograde**: Longitudinal velocity is differentiated over a 1-hour interval ($\text{deg/day}$). Retrograde is boolean `True` if $\text{velocity} < 0$.
- **Precession & Nutation**: IAU 2006 precession and IAU 2000A nutation models.
- **Lunar Node Model**: Mean Lunar Node ($\text{Rahu}$), opposite point ($\text{Ketu} = \text{Rahu} + 180^\circ$).

---

## 4. Methodologies

### Time Normalization
1. Input validated via `BirthInput` schema (strict IANA timezone verification via `pytz`).
2. Local Civil Time converted to UTC using localized timezone offsets.
3. Julian Day ($JD_{TT}$) calculated via Fliegel-Van Flandern algorithm.

### Lahiri Ayanamsha & Sidereal Conversion
- Formula: $\text{Ayanamsha} = 23.8530556^\circ + 0.0139688^\circ \times \frac{JD_{TT} - 2451545.0}{365.25}$
- Sidereal Longitude: $\text{Sidereal Lon} = (\text{Tropical Lon} - \text{Ayanamsha}) \pmod{360^\circ}$

### Rashi Classification
- 12 Signs ($30^\circ$ each).
- $\text{Sign Index} = \lfloor \text{Sidereal Lon} / 30 \rfloor + 1$
- Full precision: Degree ($0-29$), Minute ($0-59$), Second ($0.0-59.999$). Never pre-rounded.

### Nakshatra & Pada Classification
- 27 Nakshatras ($13^\circ 20' = 13.3333333^\circ$ each).
- 4 Padas per Nakshatra ($3^\circ 20' = 3.3333333^\circ$ each).
- Computed at full double-precision floating-point arithmetic.

### Ascendant & Midheaven (MC)
- Computed from Local Sidereal Time (LST) and true obliquity ($\epsilon$):
  $$\text{RAMC} = \text{LST}$$
  $$\text{MC}_{\text{trop}} = \arctan2(\sin \text{RAMC}, \cos \text{RAMC} \cos \epsilon)$$
  $$\text{Asc}_{\text{trop}} = \arctan2(\cos \text{RAMC}, -\sin \text{RAMC} \cos \epsilon - \tan \phi \sin \epsilon)$$
- Converted to sidereal longitudes via Lahiri Ayanamsha.

### Whole Sign House System
- House 1 = Entire sign of the Ascendant.
- House $N = (\text{Ascendant Sign Index} + N - 2) \pmod{12} + 1$.

---

## 5. Fail-Closed Policy & Error Handling

If any of the following occur, the engine fails closed immediately with an explicit exception (`InvalidBirthDataError`, `TimezoneResolutionError`, `OutOfBoundaryError`, or `KernelNotFoundError`):
1. Unknown/invalid IANA timezone string
2. Invalid physical geographic coordinates
3. Birth date outside supported horizon (1850-01-01 to 2150-01-22)
4. Missing or corrupted JPL ephemeris kernel
5. Any calculation failure

No default profiles, fallback to Candidate C, or synthetic charts are permitted.
