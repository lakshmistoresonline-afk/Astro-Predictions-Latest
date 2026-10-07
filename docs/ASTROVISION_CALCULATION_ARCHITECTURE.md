# Astrovision Calculation & Evidence Pipeline Architecture

## 1. Pipeline Flow
```
User Input (DOB, Time, Place, IANA Timezone)
  ↓
Time Normalization (zoneinfo.ZoneInfo, UTC, TT, Espenak-Meeus Delta-T)
  ↓
Astronomy Provider (SkyfieldJPLProvider & NASA JPL DE440s Kernel)
  ↓
Canonical Vedic Chart Builder (Sidereal Rashi, Lagna, Whole Sign Houses)
  ↓
Varga Engine (16 Parashari Divisional Charts D1 through D60 & Vargottama)
  ↓
Vimshottari Dasha Engine (120-Year Timeline, Birth Balance, 5-Level Hierarchy)
  ↓
Shadbala & Ashtakavarga Engines (Six-Fold Strengths, BAV & Dynamic SAV)
  ↓
Yoga & Dosha Engines (Parashari Rule Conditions & Cancellation Exceptions)
  ↓
Jaimini Engine (7 Chara Karakas, Arudha Lagna, Upapada Lagna, Karakamsha)
  ↓
Panchanga & Muhurta Engines (Local Solar Timing, Rahu Kalam, Rule Precedence)
  ↓
Transit & Timing Engines (Real-Time Transit Contacts & Convergent Timing Windows)
  ↓
Canonical Astrology Evidence Pipeline (Master Evidence Package & Immutable Hashes)
  ↓
Prediction Engine (14 Domain Prediction Evidence Packages)
  ↓
Report Generator Engine (12-Chapter Comprehensive Treatise) & PDF Renderer
  ↓
AI Interpretation Service (Server-Owned Evidence Synthesis & Structured Validation)
  ↓
Persistence Layer (SQLAlchemy ORM + SQLite/PostgreSQL) & API Response
```

## 2. Canonical Ownership
For complete details on the authoritative engine files, entry point methods, and contract models for each domain, see [`docs/CANONICAL_OWNERSHIP_MAP.md`](./CANONICAL_OWNERSHIP_MAP.md).
