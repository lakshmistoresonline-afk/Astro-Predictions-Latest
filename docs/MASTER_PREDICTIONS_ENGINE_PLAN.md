# Astrovision Version 6.0.0 — True Master Predictions Engine Implementation Plan

## Executive Summary & Baseline Analysis
An in-depth analysis of the 4 reference gold-standard benchmark files on the desktop:
1. `Subramanian_TS_TRUE_MAXIMUM_WORLD_CLASS_Vedic_Astrology_Report.pdf` (46 Pages, 32,088 Characters)
2. `Subramanian_TS_TRUE_ULTIMATE_Vedic_Astrology_Report.pdf` (23 Pages, 57,439 Characters)
3. `Subramanian_TS_Ultimate_Vedic_Astrology_Report.pdf` (17 Pages, 36,697 Characters — *The Celestial Dossier*)
4. `Subramanian_TS_TRUE_MAXIMUM_Gold_Standard.json` (Structured Astronomical & Astrological JSON Payload)

reveals that Astrovision's calculation core (NASA JPL DE440s ephemeris, Whole Sign houses, Lahiri ayanamsha, 16 Vargas, 5-level Vimshottari Dashas, Shadbala, Ashtakavarga, Jaimini Chara Karakas, and Transits) already produces the **exact same sub-arcsecond astronomical longitudes and planetary positions** as the reference reports.

To elevate Astrovision from a calculation engine into a **True Master Predictions Engine**, we must bridge the gap between calculation evidence and multi-layered, publication-grade, 30+ section predictive treatises.

---

## 5-Phase Implementation Blueprint

```
Phase 1: Deep Evidence Synthesis & Master Narrative Builder
       ↓
Phase 2: Shodasha Varga & Jaimini Integration Enhancement
       ↓
Phase 3: 5-Layer Convergent Domain Predictive Engine
       ↓
Phase 4: Gold Standard Machine-Readable JSON Export
       ↓
Phase 5: World-Class ReportLab 30+ Section PDF Treatise Engine
```

---

### Phase 1: Deep Evidence Synthesis & Master Narrative Builder
**Target File**: `apps/api/engines/treatise_builder.py`

Implement a dedicated **`MasterTreatiseBuilder`** engine that compiles all 30 sections + 4 appendices featured in *The Celestial Dossier* and *World-Class Reports*:

1. **Executive Summary & Anchor Metrics**:
   - Ascendant, Moon (Nakshatra, Pada), Sun, Current Mahadasha/Antardasha, Dominant Structural Themes, Strong Dignities, Retrograde Planets.
2. **Section 1–3: Calculation Standards & Planetary Ledger**:
   - Civil to UTC time conversion, Julian Day (UT/TT), Lahiri Ayanamsha value.
   - Verified Planetary Ledger Table (Graha, Sidereal $\lambda$, Tropical $\lambda$, WS House, Nakshatra/Pada, Star Lord, Motion, Dignity).
   - Rashi (D1) Architecture Table (House, Sign, Lord, Occupants).
3. **Section 4–6: Lagna, Planet-by-Planet & House-by-House Deep Dives**:
   - Detailed individual narratives for Lagna and all 9 planets (Sun through Ketu).
   - Detailed individual narratives for all 12 Bhavas (1st through 12th Houses).
4. **Section 7–10: Aspect Matrix, Yoga Audit & Nakshatra Atlas**:
   - Classical Graha Drishti aspect contact matrix.
   - Conservative Yoga Audit Table (Combination, Basis, Assessment, Traditional Implication) including Viparita Raja Yogas, Dhana Yogas, Kendra-Trikona Yogas.
   - Janma Nakshatra deep dive & complete Nakshatra placement matrix.
   - Divisional Chart Overview Table (D1, D9 Navamsha, D3, D7, D12, D10, D24, D60).
5. **Section 11–13: Vimshottari Dasha & Transit Architecture**:
   - 120-year Vimshottari Mahadasha timeline + birth balance.
   - Active Mahadasha/Antardasha deep dive with exact dates and house activations.
   - Current Transit Snapshot (query date transits, signs, houses, aspect contacts).
6. **Section 14–22: 9 Core Life Domain Deep Dives**:
   - **Career & Professional Destiny** (10th Bhava, D10 Dashamsha, Saturn, Mercury).
   - **Wealth, Income & Asset Strategy** (2nd/11th Bhavas, D2 Hora, Dhana Yogas).
   - **Business & Entrepreneurship** (7th/10th Bhavas, commerce, partnerships).
   - **Relationships & Marriage** (7th Bhava, Venus, D9 Navamsha).
   - **Education, Intelligence & Research** (4th/5th/9th Bhavas, D24 Chaturvimshamsha).
   - **Foreign Travel, Relocation & Global Work** (9th/12th Bhavas, foreign settlement).
   - **Home, Property & Vehicles** (4th Bhava, D4 Chaturthamsha, Mars/Saturn).
   - **Health & Lifestyle** (1st/6th/8th Bhavas, immunity & vitality).
   - **Spiritual & Philosophical Themes** (9th/12th/5th Bhavas, D20 Vimshamsha, Ketu).
7. **Section 23–25: Risk Register & Strategic Astrology Timelines**:
   - Risk Register Table (Risk Area, Factor, Traditional Mitigation).
   - 2026–2030 Strategic Astrology Timeline Table (5-Year Window).
   - 2031–2044 Strategic Astrology Timeline Table (Long Horizon Window).
8. **Section 26–30: Remedial Framework & Validation Audits**:
   - Traditional non-medical Remedial Framework (Upayas, mantras, service).
   - Application Benchmark Specification & Validation Checklist.
   - Interpretation Confidence Framework Table (Classes A–D).
   - Final Integrated Reading Synthesis.
9. **Appendices A–D**:
   - Appendix A: Raw Longitudes and Speeds Table.
   - Appendix B: Placidus Cusps (Audit Only).
   - Appendix C: Source & Method Notes.
   - Appendix D: Important Limitations.

---

### Phase 2: Shodasha Varga & Jaimini Integration Enhancement
**Target Files**: `apps/api/engines/varga/engine.py`, `apps/api/engines/jaimini/engine.py`

1. **Complete Shodasha Varga Placements**:
   - Ensure all 16 Vargas (D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60) calculate Lagna, Sun, Moon, and planetary sign placements for tabular rendering in Section 10 and Appendix tables.
2. **Jaimini Sutra Integrations**:
   - Calculate Chara Karakas (Atmakaraka, Amatyakaraka, Bhratrukaraka, Matrukaraka, Putrakaraka, Gnatikaraka, Darakaraka) and Arudha Padas (AL, UL, A1..A12).
3. **Vargottama & Dignity Calculation**:
   - Identify Vargottama planets (planets occupying the same sign in D1 and D9) and exaltation/own-sign dignities across all divisional charts.

---

### Phase 3: 5-Layer Convergent Domain Predictive Engine
**Target File**: `apps/api/engines/prediction_engine.py`

Upgrade the domain prediction algorithm to evaluate 5 convergent evidence layers for every domain:

$$\text{Domain Strength Score} = w_1 \cdot \text{D1 Placements} + w_2 \cdot \text{Varga Dignity} + w_3 \cdot \text{Active Dasha Activation} + w_4 \cdot \text{Transit SAV Bindus} + w_5 \cdot \text{Shadbala}$$

- **Layer 1**: D1 House Lord & Karaka placements.
- **Layer 2**: Relevant Divisional Chart dignities (D9 for Marriage, D10 for Career, D2 for Wealth, D4 for Property, D24 for Education, D20 for Spirituality).
- **Layer 3**: Active Vimshottari Mahadasha/Antardasha Lord activations.
- **Layer 4**: Transiting Jupiter/Saturn/Rahu/Ketu house aspects and Ashtakavarga SAV bindus.
- **Layer 5**: Classical Yogas & Shadbala strengths.

Generates specific, time-bounded strategic guidance instead of generic boilerplate text.

---

### Phase 4: Gold Standard Machine-Readable JSON Export
**Target Endpoint**: `POST /api/v1/export/gold-standard-json` & `apps/api/routers/admin_export.py`

Expose a dedicated JSON export endpoint producing the exact machine-readable JSON structure as `Subramanian_TS_TRUE_MAXIMUM_Gold_Standard.json`:

```json
{
  "title": "THE CELESTIAL DOSSIER",
  "subtitle": "A Comprehensive Vedic Astrology Calculation & Interpretation Report",
  "meta": {
    "native_name": "SUBRAMANIAN T S",
    "birth_date": "1986-09-28",
    "birth_time": "16:30:00",
    "timezone": "Asia/Kolkata",
    "coordinates": {"lat": 10.7867, "lon": 76.6548, "place": "Palakkad, Kerala", "country": "India"},
    "julian_day_utc": 2446701.958333333,
    "ayanamsha_mode": "Lahiri",
    "ayanamsha_value_deg": 23.671877038,
    "master_evidence_hash": "c1c7feeab882263f..."
  },
  "vargas": { "D1": {...}, "D9": {...}, "D10": {...}, ... },
  "ashtakavarga": { "bav": {...}, "sav": [...] },
  "chara_karakas": { "AK": "Mars", "AmK": "Mercury", ... },
  "arudhas": { "AL": "Scorpio", "UL": "Capricorn", ... },
  "vargottama": ["Mars", "Venus"],
  "current_dasha": { "active_mahadasha": "Venus", "active_antardasha": "Venus", ... },
  "panchanga": { "tithi": "Dashami", "nakshatra": "Pushya", "pada": 2, "yoga": "Siddhi", "karana": "Bava", "vara": "Sunday" }
}
```

---

### Phase 5: World-Class ReportLab 30+ Section PDF Treatise Engine
**Target File**: `apps/api/engines/pdf_report_engine.py`

Upgrade `PDFReportEngine` to build the full 30-Section + 4 Appendices PDF document using ReportLab:

1. **Numbered Canvas Page Decorator**:
   - Running Header (Pages 2+): `THE CELESTIAL DOSSIER | <NAME>` (Bold 8pt, Champagne Gold Line `#D6B36A`).
   - Running Footer (Pages 2+): `Calculation-auditable Jyotisha reference report • Page X of Y`.
2. **Color Palette & Styling**:
   - Primary Header: `#B8860B` (Dark Goldenrod / Champagne Gold)
   - Accent Navy: `#0B1026` (Deep Cosmic Navy)
   - Table Background: `#F9F6EE` (Champagne Cream)
   - Body Text: `#222222` (Charcoal)
3. **Structured Tables**:
   - Anchor Verified Result Table (Executive Summary)
   - Calculation Standards Table (Section 1)
   - Verified Planetary Ledger Table (Section 2)
   - Rashi D1 Architecture Table (Section 3)
   - Aspect Contact Matrix Table (Section 7)
   - Yoga Audit Table (Section 8)
   - Nakshatra Placements Table (Section 9)
   - Divisional Chart Overview Table (Section 10)
   - Vimshottari Mahadasha Timeline Table (Section 11)
   - Antardasha Timeline Table (Section 12)
   - Risk Register Table (Section 23)
   - Strategic Timeline 2026–2030 Table (Section 24)
   - Strategic Timeline 2031–2044 Table (Section 25)
   - Interpretation Confidence Framework Table (Section 29)
   - Raw Longitudes & Speeds Table (Appendix A)

---

## Verification & Testing Strategy

1. **Regression Unit Testing**:
   - Run `python -m pytest apps/api/tests/` to ensure all existing 136 Pytest unit tests pass.
2. **26-Gate Release Certification**:
   - Run `python scripts/run_release_certification.py` to verify 100% pass across all 26 Release Gates.
3. **Gold Standard Reference Comparison Test**:
   - Execute a comparison test taking Subramanian T S birth data (28 September 1986, 16:30 IST, Palakkad) and comparing generated PDF sections, tables, and JSON export against the baseline desktop files:
     - `Subramanian_TS_TRUE_MAXIMUM_Gold_Standard.json`
     - `Subramanian_TS_Ultimate_Vedic_Astrology_Report.pdf`
     - `Subramanian_TS_TRUE_MAXIMUM_WORLD_CLASS_Vedic_Astrology_Report.pdf`
     - `Subramanian_TS_TRUE_ULTIMATE_Vedic_Astrology_Report.pdf`
