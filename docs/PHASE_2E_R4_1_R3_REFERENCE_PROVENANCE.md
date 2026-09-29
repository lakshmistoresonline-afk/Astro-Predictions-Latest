# Phase 2E-R4.1-R3 Reference Data Provenance & Manifest

## 1. Raw Reference Dataset Source
- **Software Library**: PyEphem 4.2.1 (XEphem C Astronomical Ephemeris Core).
- **License**: MIT License.
- **Generator Script**: `reference_source/standalone_ephemeris_extractor.py`.
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`).
- **Raw Files**: `reference_source/raw_reference/REF_001.json` through `REF_020.json`.
- **Target Fixtures**: `apps/api/tests/fixtures/phase_2e_r4_1_reference/`.
- **Cryptographic Manifest**: `PHASE_2E_R4_1_R3_REFERENCE_MANIFEST.json` containing SHA-256 signatures for all 20 reference files.

## 2. Real Birth Chart Profiles (15 Fixtures)
- `REF_001`: Subramanian T S (Palakkad, India: 1986-09-28 16:30 IST)
- `REF_002`: User A Kochi (Kochi, India: 1990-01-15 08:30 IST)
- `REF_003`: User B London (London, UK: 1985-07-22 18:45 BST)
- `REF_004`: New York Native (New York, USA: 2000-01-01 12:00 EST)
- `REF_005`: Tokyo Native (Tokyo, Japan: 1995-05-05 09:00 JST)
- `REF_006`: Sydney Native (Sydney, Australia: 1998-11-12 15:30 AEST)
- `REF_007`: Paris Native (Paris, France: 1975-03-21 06:00 CET)
- `REF_008`: Reykjavik Native (Reykjavik, Iceland: 1992-06-21 23:45 UTC)
- `SHADBALA_FIXTURE_009`: Singapore Native (Singapore: 2010-08-09 18:00 SGT)
- `SHADBALA_FIXTURE_010`: Los Angeles Retrograde (Los Angeles, USA: 2020-10-15 20:00 PDT)
- `REF_011`: Berlin Native (Berlin, Germany: 1988-12-12 10:15 CET)
- `REF_012`: Cairo Native (Cairo, Egypt: 1991-04-10 14:00 EET)
- `REF_013`: Buenos Aires Native (Buenos Aires, Argentina: 1982-02-28 08:00 ART)
- `REF_014`: Mumbai Native (Mumbai, India: 1994-08-15 22:30 IST)
- `REF_015`: Honolulu Native (Honolulu, Hawaii: 2005-07-04 05:30 HST)

## 3. Synthetic Boundary Profiles (5 Fixtures)
- `REF_016`: Sun Exaltation Boundary (Aries 10° Sun)
- `REF_017`: Sun Debilitation Boundary (Libra 10° Sun)
- `REF_018`: Cardinal Dig Bala Power (Sun MC 10th house)
- `REF_019`: Cardinal Dig Bala Zero (Sun IC 4th house)
- `REF_020`: High Speed Velocity (Mars Fast Velocity)
