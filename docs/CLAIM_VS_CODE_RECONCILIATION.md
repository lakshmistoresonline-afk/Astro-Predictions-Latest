# Claim vs Code Reconciliation ("Astrovision")

| Capability | Documentation Claim | Actual Code | Test Evidence | Status |
|------------|---------------------|-------------|---------------|--------|
| Astronomical Calculations | High-precision Meeus / Ephemeris | Meeus coordinate equations & orbital epochs | Unit tests | IMPLEMENTED |
| Lahiri Ayanamsha | Sidereal Lahiri calculation | Meeus coordinate adjustment for Lahiri | Unit tests | IMPLEMENTED |
| Ascendant & Houses | Full house cusps & Lagna | Mathematical ascendant calculation from Julian Day and lat/lon | Unit tests | IMPLEMENTED |
| Nakshatra & Pada | 27 Nakshatras with 4 Padas | Exact degree calculation (13°20' per Nakshatra) | Unit tests | IMPLEMENTED |
| Planetary Dignities | Exaltation, debilitation, own sign | Dignity rule engine | Unit tests | IMPLEMENTED |
| Vargas (D1-D60) | Classical divisional charts | Mathematical varga boundary algorithms | Unit tests | IMPLEMENTED |
| Vimshottari Dasha | 5-level micro-timing with birth balance | Moon longitude elapsed fraction calculation | Unit tests | IMPLEMENTED |
| Yogas & Doshas | Rule-based astrological combinations | Multi-condition rule registry | Unit tests | IMPLEMENTED |
| Shadbala & Ashtakavarga | Quantitative planetary strength & bindus | Rule-based calculation or explicit status | Unit tests | IMPLEMENTED |
| Transits | Real-time transit positions | Target datetime coordinate computation | Unit tests | IMPLEMENTED |
| Prediction Engine | Evidence-based domain interpretation | Structured factor aggregation | Unit tests | IMPLEMENTED |
| AI Integration | Ollama local model interpretation & validation | Prompt generator & repair/validate flow | Unit tests | IMPLEMENTED |
| Personalization | User-scoped profiles & calculations | Database ownership scoping & differential tests | Unit tests | IMPLEMENTED |
| Frontend Modules | Full modular navigation & tabs | Componentized routes & views | E2E / Manual | IMPLEMENTED |
