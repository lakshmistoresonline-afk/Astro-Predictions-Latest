# Astrovision Astronomy Provider Contract — Architecture & Specification

## 1. Executive Summary

This document defines the canonical provider-neutral astronomy software contract for **Astrovision**, implemented under `apps/api/engines/astronomy/`.

---

## 2. Architectural Layers & Separation of Concerns

```
+-------------------------------------------------------------------------+
|                          VEDIC ENGINE LAYER                             |
| (Nakshatras, Vargas, Dashas, Yogas, Shadbala, Ashtakavarga, Predictions) |
+-------------------------------------------------------------------------+
                                   ^
                                   | (Consumes Sidereal State)
+-------------------------------------------------------------------------+
|                       SIDEREAL CONVERSION LAYER                         |
|      (Deterministic Lahiri Ayanamsha Conversion: Tropical -> Sidereal)  |
+-------------------------------------------------------------------------+
                                   ^
                                   | (Consumes Derived Astronomy State)
+-------------------------------------------------------------------------+
|                     DERIVED ASTRONOMY LAYER                             |
| (Local Sidereal Time, RAMC, True Obliquity, Tropical Ascendant & MC)    |
+-------------------------------------------------------------------------+
                                   ^
                                   | (Consumes Raw Ephemeris State)
+-------------------------------------------------------------------------+
|                     RAW EPHEMERIS PROVIDER LAYER                        |
|       (Skyfield + JPL Ephemeris DE440s/DE421 Geocentric Positions)      |
+-------------------------------------------------------------------------+
```

---

## 3. Strict Boundary Rules

1. **Raw Ephemeris Layer**: Computes geocentric ecliptic longitudes, latitudes, distance, orbital longitudinal speed (velocity in deg/day), and retrograde status directly from JPL SPK kernels.
2. **Derived Astronomy Layer**: Computes Greenwich Apparent Sidereal Time (GAST), Local Sidereal Time (LST), Right Ascension of Midheaven (RAMC), true ecliptic obliquity, Tropical Ascendant, and Midheaven (MC).
3. **Sidereal Layer**: Converts tropical longitudes to sidereal longitudes using a deterministic Lahiri Ayanamsha formula ($23.8530556^\circ + 0.0139688^\circ \times T$).
4. **NO VEDIC CALCULATIONS**: The astronomy provider MUST NOT compute Nakshatras, Padas, Vargas, Dashas, Yogas, or Predictions. These belong strictly to downstream Vedic engines.
5. **Fail-Closed Guard**: If Skyfield or the JPL kernel file cannot be loaded or initialized, the provider **must raise an explicit `AstronomyProviderError`**. It MUST NOT fall back to Candidate C, synthetic formulas, or mock default data.
6. **Cryptographic Determinism**: Every calculation produces a SHA-256 calculation hash derived from normalized input parameters and ephemeris metadata.

---

## 4. Canonical Output Data Schema (`CalculationResult`)

Every calculation returns a structured `CalculationResult` containing:

1. **`raw_ephemeris` (`RawEphemerisData`)**:
   - `timestamp_utc`: ISO-8601 UTC timestamp string
   - `julian_day_tt`: Julian Day in Terrestrial Time
   - `time_scale`: `"UTC"` / `"TT"`
   - `observer_latitude`: float
   - `observer_longitude`: float
   - `observer_elevation_m`: float
   - `ephemeris_identifier`: `"NASA JPL DE421 / DE440s"`
   - `reference_frame`: `"ICRF / J2000"`
   - `bodies`: Dict[str, `PlanetPosition`] for Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto. Each body contains:
     - `geocentric_longitude`: float ($0^\circ - 360^\circ$)
     - `geocentric_latitude`: float
     - `distance_au`: float
     - `velocity_lon_deg_day`: float (deg/day)
     - `retrograde`: bool (`True` if `velocity_lon_deg_day < 0`)

2. **`derived_astronomy` (`DerivedAstronomicalState`)**:
   - `local_sidereal_time_deg`: float
   - `ramc_deg`: float
   - `true_obliquity_deg`: float
   - `ascendant_tropical_deg`: float
   - `mc_tropical_deg`: float

3. **`sidereal_state` (`SiderealState`)**:
   - `ayanamsha_mode`: `"Lahiri"`
   - `ayanamsha_value_deg`: float
   - `sidereal_longitudes`: Dict[str, float]
   - `ascendant_sidereal_deg`: float
   - `mc_sidereal_deg`: float

4. **`metadata` (`EphemerisMetadata`)**:
   - `provider`: `"Skyfield"`
   - `provider_version`: `"1.55"`
   - `ephemeris_kernel`: `"de421.bsp"` / `"de440s.bsp"`
   - `kernel_checksum`: MD5 hash string
   - `calculation_timestamp_utc`: ISO string
   - `calculation_hash`: SHA-256 digest string
