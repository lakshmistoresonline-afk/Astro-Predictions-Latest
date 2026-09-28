# Phase 2C Pre-Implementation Audit — Vimshottari Dasha Engine

## 1. Executive Summary

This pre-implementation audit inspects all Dasha-related implementations, formulas, assumptions, consumers, and limitations across the repository prior to implementing **Phase 2C (Authoritative Vimshottari Dasha Engine)**.

---

## 2. Audit of Existing Dasha Implementations

### A. `apps/api/engines/dasha_engine.py`
- **Current Signature**: `DashaEngine.calculate_vimshottari_dasha(birth_date_str: str, moon_nakshatra: str, nakshatra_pada: int)`
- **Current Methodology & Critical Flaws**:
  1. **Ignores Moon's Exact Longitude**: Takes `moon_nakshatra` as a text string instead of using full-precision Moon longitude from Phase 2A canonical astronomy.
  2. **Zero Birth Balance Calculation**: Assumes the birth Mahadasha starts at 100% full duration at birth date. Fails to calculate elapsed/remaining Nakshatra fraction and remaining Mahadasha balance ($MD_{\text{balance}}$).
  3. **No Nested Sub-Period Timelines**: Generates only a flat list of 9 top-level Mahadashas without true nested Antardasha, Pratyantardasha, Sookshma, or Prana calculations.
  4. **Naive Date Arithmetic**: Adds fixed `365.25 * years` timedelta to string dates without timezone sensitivity or astronomical time conventions.

### B. `apps/api/engines/masterwork_engine.py` (`calculate_5_level_dasha`)
- **Current Signature**: `MasterworkEngine.calculate_5_level_dasha(birth_date_str: str, moon_nakshatra: str)`
- **Current Methodology & Critical Flaws**:
  1. **Mock Sub-Period Selection**: Takes current Mahadasha lord index in `["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]` and simply assigns the next 4 planets sequentially in order (`(idx+1)%9`, `(idx+2)%9`, `(idx+3)%9`, `(idx+4)%9`).
  2. **No Date or Duration Formulas**: Does not perform nested duration calculations ($AD = MD \times \frac{AD_{lord}}{120}$). Returns static strings without timeline start/end dates.

---

## 3. Dependency Graph & Repository Consumers

```
[Phase 2A Canonical Astronomy] (Canonical Sidereal Moon Longitude)
               │
               ▼
[Phase 2C Authoritative Dasha Engine] (`apps/api/engines/dasha/`)
               │
   ┌───────────┼──────────────────────────┐
   ▼           ▼                          ▼
[Report Engine] [Evidence Aggregator] [Prediction Engine]
   │           │                          │
   └───────────┴──────────┬───────────────┘
                          ▼
             [API Routers & Frontend / AI]
```

### Active Consumer Locations
1. `apps/api/engines/report_engine.py`: Invokes `DashaEngine` for Chapter 8 report generation (`chapter_8_dasha`).
2. `apps/api/engines/evidence_aggregator.py`: Consumes current active Mahadasha for domain prediction evidence.
3. `apps/api/engines/prediction_engine.py`: Passes Dasha evidence to prediction pipeline.
4. `apps/api/main.py`: Serializes `dasha_info` in `/api/v1/birth-profile` endpoint.
5. `apps/api/services/ai_service.py`: Passes Dasha evidence in prompt context.

---

## 4. Replacement & Migration Strategy

1. **New Authoritative Package**: Build `apps/api/engines/dasha/` with `DashaEngine`, `models.py`, `calculator.py`, `timeline.py`, `hash.py`, and `exceptions.py`.
2. **Single Source of Truth**: Consume `CanonicalVedicChart` (Phase 2A sidereal Moon position) directly.
3. **5-Level Hierarchy & Balance**: Implement exact Parashari $MD_{\text{balance}}$, nested AD, PD, Sookshma, and Prana timelines.
4. **Adapter / Replacement for Legacy Code**: Adapt `apps/api/engines/dasha_engine.py` to delegate directly to `apps/api/engines/dasha/`, ensuring 100% backward compatibility for API responses while using the authoritative calculation engine.
5. **Deprecate Synthetic Code**: Deprecate `MasterworkEngine.calculate_5_level_dasha` mock logic in favor of true nested 5-level Dasha hierarchy from Phase 2C.
