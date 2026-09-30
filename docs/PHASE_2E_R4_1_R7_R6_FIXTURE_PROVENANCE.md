# Phase 2E-R4.1-R7-R6 Multi-Fixture Provenance & Diversity Audit

## 1. Provenance Chain Architecture
```
              [External Ephemeris / Astronomical Input]
             (PyEphem / JPL DE440s Astronomical Ephemeris)
                                │
                                ▼
         [Raw Inputs] (phase_2e_r4_1_reference/*.json)
                                │
                                ▼
          [Pure Independent Oracle] (generate_expected.py)
        (Zero Imports from apps.api.engines.*)
                                │
                                ▼
       [Immutable Fixtures] (phase_2e_r4_1_expected/*.json)
```

## 2. 20 Immutable Fixtures Diversity Audit
The 20 reference fixtures (`REF_001` through `REF_020` in `apps/api/tests/fixtures/phase_2e_r4_1_expected/*.json`) cover diverse astronomical and Vedic boundary conditions:

| Fixture ID | Category | Birth Date / Time | Ascendant Sign | Solar State | Special Features |
|---|---|---|---|---|---|
| `REF_001` | Canonical Profile | 1986-09-28 16:30 IST | Sagittarius | Sun in Virgo | Subramanian T S Benchmark Profile |
| `REF_002` | Historical Profile | 1869-10-02 07:45 IST | Libra | Sun in Virgo | Mahatma Gandhi Profile |
| `REF_003` | Historical Profile | 1889-11-14 23:00 IST | Cancer | Sun in Scorpio | Jawaharlal Nehru Profile |
| `REF_004` | Historical Profile | 1891-04-14 12:00 IST | Aries | Sun in Aries | B. R. Ambedkar Profile |
| `REF_005` | Modern Profile | 1970-01-01 00:00 UTC | Virgo | Sun in Sagittarius | Epoch Boundary Benchmark |
| `REF_006` | High Latitude | 1980-06-21 12:00 UTC | Virgo | Summer Solstice | Tromsø, Norway (69.65°N) |
| `REF_007` | Southern High Lat | 1980-12-21 12:00 UTC | Sagittarius | Winter Solstice | Ushuaia, Argentina (54.80°S) |
| `REF_008` | Equatorial | 1995-03-21 06:00 UTC | Pisces | Vernal Equinox | Pontianak, Indonesia (0.0° Lat) |
| `REF_009` | Retrograde Suite | 2008-03-15 18:30 IST | Leo | Sun in Pisces | Multiple Planets Retrograde |
| `REF_010` | Fast Velocity Suite | 2012-09-12 10:00 IST | Gemini | Sun in Leo | High Planetary Velocities |
| `REF_011` | Midnight Birth | 2015-12-31 23:59 IST | Virgo | Sun in Sagittarius | Year-End Midnight Transition |
| `REF_012` | Noon Birth | 2018-06-15 12:00 IST | Virgo | Sun in Gemini | Midday Diurnal Strength Maximum |
| `REF_013` | Southern Hemisphere| 2020-02-29 14:15 UTC | Cancer | Sun in Aquarius | Sydney, Australia Leap Day |
| `REF_014` | Eclipse Conjunction| 2022-10-25 11:30 UTC | Libra | Sun in Libra | Partial Solar Eclipse Conjunction |
| `REF_015` | Extreme Ayanamsha | 2025-01-01 00:00 UTC | Sagittarius | Sun in Sagittarius| Future Epoch Boundary |
| `REF_016` | Synthetic Boundary | N/A (Aries 0.0°) | Aries 0° | Cardinal Boundary | Exaltation Boundary Checks |
| `REF_017` | Synthetic Boundary | N/A (Cancer 0.0°) | Cancer 0° | Cardinal Boundary | Debilitation Boundary Checks |
| `REF_018` | Synthetic Boundary | N/A (Libra 0.0°) | Libra 0° | Cardinal Boundary | Diurnal/Nocturnal Boundary |
| `REF_019` | Synthetic Boundary | N/A (Capricorn 0.0°)| Capricorn 0° | Cardinal Boundary | Kendradi Boundary Checks |
| `REF_020` | Synthetic Boundary | N/A (Pisces 29.9°) | Pisces 29.9° | Sign Boundary | 29.99° Boundary Crossing Check |

## 3. Contamination Verdict
- **Contaminated Fixtures**: `0`
- **Pure Independent Fixtures**: `20`
