# Astrovision Current Forensic Audit

## A. Actual Repository Architecture
- **Backend**: Python FastAPI monorepo service in `apps/api/` with modular calculation engines (`astronomical_engine.py`, `vedic_engine.py`, `dasha_engine.py`, `varga_engine.py`, `yoga_engine.py`, `strength_engine.py`, `prediction_engine.py`, `report_engine.py`).
- **Frontend**: Next.js 14+ App Router in `apps/web/` featuring Astrovision's full-width celestial desktop command center and modular tab routing.

## B. Actual Dependency Graph
- FastAPI, Pydantic, NumPy, Uvicorn, Pytest, Pytz, Requests, Next.js, Tailwind CSS.

## C. Capability Matrix

| Capability | Claimed | Actual | Evidence | Status | Required Action |
|------------|---------|--------|----------|--------|-----------------|
| Astronomical Calculations | High-precision Ephemeris | Meeus coordinate equations & orbital epochs | Unit tests | VERIFIED | Maintain pure-Python high precision. |
| Lahiri Ayanamsha | Sidereal calculation | Meeus coordinate adjustment for Lahiri (~23.85°) | Unit tests | VERIFIED | Keep aligned with Chitra Paksha. |
| Ascendant & Houses | Full house cusps & Lagna | Mathematical ascendant calculation | Unit tests | VERIFIED | Maintain numerical tests. |
| Nakshatra & Pada | 27 Nakshatras with 4 Padas | Exact 13°20' division from Moon longitude | Unit tests | VERIFIED | Boundary tests passing. |
| Vargas (D1-D60) | D1 to D60 divisional charts | Mathematical varga algorithms for D1-D60 | Unit tests | VERIFIED | Keep mathematical rules strict. |
| Vimshottari Dasha | 5-level micro-timing with birth balance | Moon longitude elapsed fraction calculation | Unit tests | VERIFIED | Maintain exact balance calculations. |
| Yogas & Doshas | Rule-based astrological combinations | Multi-condition rule registry | VERIFIED | Maintain rule strictness. |
| AI Integration | Ollama local interpretation & validation | Prompt generator & repair/validate flow | VERIFIED | Maintain server-side evidence scoping. |
| Personalization | User-scoped profiles & calculations | Database ownership scoping & differential tests | VERIFIED | Zero cross-user contamination. |
