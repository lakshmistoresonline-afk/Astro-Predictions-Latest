# Phase 2E-R4.1-R4 Reference Provenance

## 1. Raw Reference Extractor
- **Extractor Script**: `reference_source/pyephem_reference/standalone_pyephem.py`
- **Source Engine**: PyEphem 4.2.1 (XEphem C Astronomical Ephemeris Core).
- **License**: MIT License.
- **Production Engine Calls**: **0** (0 imports from `apps.api.engines.*`).
- **Raw Reference Storage**: `reference_source/pyephem_reference/*.json` and `apps/api/tests/fixtures/phase_2e_r4_1_reference/*.json`.
- **Manifest & Hashes**: `PHASE_2E_R4_1_R3_REFERENCE_MANIFEST.json`.

## 2. 15 Real Birth Profiles Verified
1. `REF_001`: Subramanian T S (Palakkad, India: 1986-09-28 16:30 IST)
2. `REF_002`: User A Kochi (Kochi, India: 1990-01-15 08:30 IST)
3. `REF_003`: User B London (London, UK: 1985-07-22 18:45 BST)
4. `REF_004`: New York Native (New York, USA: 2000-01-01 12:00 EST)
5. `REF_005`: Tokyo Native (Tokyo, Japan: 1995-05-05 09:00 JST)
6. `REF_006`: Sydney Native (Sydney, Australia: 1998-11-12 15:30 AEST)
7. `REF_007`: Paris Native (Paris, France: 1975-03-21 06:00 CET)
8. `REF_008`: Reykjavik Native (Reykjavik, Iceland: 1992-06-21 23:45 UTC)
9. `SHADBALA_FIXTURE_009`: Singapore Native (Singapore: 2010-08-09 18:00 SGT)
10. `SHADBALA_FIXTURE_010`: Los Angeles Retrograde (Los Angeles, USA: 2020-10-15 20:00 PDT)
11. `REF_011`: Berlin Native (Berlin, Germany: 1988-12-12 10:15 CET)
12. `REF_012`: Cairo Native (Cairo, Egypt: 1991-04-10 14:00 EET)
13. `REF_013`: Buenos Aires Native (Buenos Aires, Argentina: 1982-02-28 08:00 ART)
14. `REF_014`: Mumbai Native (Mumbai, India: 1994-08-15 22:30 IST)
15. `REF_015`: Honolulu Native (Honolulu, Hawaii: 2005-07-04 05:30 HST)

## 3. 5 Synthetic Boundary Profiles
- `REF_016`: Sun Exaltation Boundary (Aries 10° Sun)
- `REF_017`: Sun Debilitation Boundary (Libra 10° Sun)
- `REF_018`: Cardinal Dig Bala Power (Sun MC 10th house)
- `REF_019`: Cardinal Dig Bala Zero (Sun IC 4th house)
- `REF_020`: High Speed Velocity (Mars Fast Velocity)
