# Phase 2E-R4.1 Reference Data Provenance & Integrity Manifest

## 1. Reference Input Dataset (`apps/api/tests/fixtures/phase_2e_r4_1_reference/`)
All 20 reference JSON datasets (15 real birth charts + 5 synthetic boundary charts) contain frozen astronomical state values (sidereal longitudes, daily velocities, Ascendant, MC, ayanamsha, Julian Day Numbers) compiled independently.

### Real Birth Profiles (15 Fixtures)
- **REF_001**: Subramanian T S (Palakkad, India: 1986-09-28 16:30 IST)
- **REF_002**: User A Kochi (Kochi, India: 1990-01-15 08:30 IST)
- **REF_003**: User B London (London, UK: 1985-07-22 18:45 BST)
- **REF_004**: New York Native (New York, USA: 2000-01-01 12:00 EST)
- **REF_005**: Tokyo Native (Tokyo, Japan: 1995-05-05 09:00 JST)
- **REF_006**: Sydney Native (Sydney, Australia - Southern Hemisphere: 1998-11-12 15:30 AEST)
- **REF_007**: Paris Native (Paris, France - Near Sunrise: 1975-03-21 06:00 CET)
- **REF_008**: Reykjavik Native (Reykjavik, Iceland - High Latitude Midnight: 1992-06-21 23:45 UTC)
- **SHADBALA_FIXTURE_009**: Singapore Native (Singapore - Equatorial Sunset: 2010-08-09 18:00 SGT)
- **SHADBALA_FIXTURE_010**: Los Angeles Retrograde (Los Angeles, USA - Retrograde Planets: 2020-10-15 20:00 PDT)
- **REF_011**: Berlin Native (Berlin, Germany: 1988-12-12 10:15 CET)
- **REF_012**: Cairo Native (Cairo, Egypt: 1991-04-10 14:00 EET)
- **REF_013**: Buenos Aires Native (Buenos Aires, Argentina: 1982-02-28 08:00 ART)
- **REF_014**: Mumbai Native (Mumbai, India: 1994-08-15 22:30 IST)
- **REF_015**: Honolulu Native (Honolulu, Hawaii: 2005-07-04 05:30 HST)

### Synthetic Boundary Charts (5 Fixtures)
- **REF_016**: Sun Exaltation Boundary (Aries 10° Sun)
- **REF_017**: Sun Debilitation Boundary (Libra 10° Sun)
- **REF_018**: Cardinal Dig Bala Power (Sun MC 10th house)
- **REF_019**: Cardinal Dig Bala Zero (Sun IC 4th house)
- **REF_020**: High Speed Velocity (Mars Fast Velocity)

## 2. Integrity Principle
Neither `generate_expected.py` nor any test runner invokes production engines (`build_canonical_vedic_chart`, `SkyfieldJPLProvider`, `AstronomicalEngine`, `VargaEngine`, `ShadbalaEngine`, `AshtakavargaEngine`) to build reference data. Reference files are frozen and hashed with SHA-256 signatures.
