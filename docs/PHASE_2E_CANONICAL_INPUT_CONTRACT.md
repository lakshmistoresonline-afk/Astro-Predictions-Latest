# Phase 2E Canonical Input Contract

## 1. Requirement
The Authoritative Ashtakavarga and Shadbala engines MUST consume the exact canonical chart state provided by Phase 2A (`CanonicalVedicChart`).

## 2. Dependencies
- **Phase 2A Astronomy**: Provides full-precision geocentric planetary longitudes, latitudes, velocities, retrograde status, and the canonical Ascendant/MC points via `build_canonical_vedic_chart()`.
- **Phase 2B Vargas**: The `VargaEngine` generates the divisional charts (e.g., D9 Navamsa, D3 Drekkana) used for `Sapta Vargaja Bala` component in Shadbala.

## 3. Strict Prohibitions
The new Phase 2E engine MUST NOT:
- Independently recalculate planetary longitude or latitude.
- Call Skyfield/JPL or `AstronomicalEngine`.
- Use synthetic random, modulo, or multiplier hacks.
- Perform calculations using rounded display strings (e.g., `"Virgo 11°33'"`).

## 4. Input Schema Concept
```python
def calculate_shadbala_suite(canonical_chart: CanonicalVedicChart, varga_suite: Full16VargaSuite) -> ShadbalaSuiteResult:
    pass

def calculate_ashtakavarga(canonical_chart: CanonicalVedicChart) -> AshtakavargaSuiteResult:
    pass
```
The exact planetary degrees (`placement.sidereal_longitude`) are used for interpolating exact strength values (like directional strength `Dig Bala` and exaltation strength `Uccha Bala`).
