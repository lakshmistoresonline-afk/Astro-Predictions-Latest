# Phase 2D-R3 Production Path Certification

## 1. Executive Summary
This document traces the actual production API execution path to ensure it uses the exact authoritative calculation layers certified in Phase 2D-R3, without silently falling back to legacy implementations.

---

## 2. API Production Path Trace

1. **API Endpoint (`apps/api/main.py`)**:
   - Route: `POST /api/v1/birth-profile`
   - Payload: `BirthProfileRequest` (Name, Year, Month, Day, Hour, Minute, Lat, Lon, TZ).

2. **Birth Normalization (`apps/api/engines/vedic/time_normalization.py`)**:
   - `normalize_birth_time()` maps the input parameters to strict UTC timezone-aware datetimes and Julian Day using the authoritative `pytz` package.

3. **Canonical Astronomy Engine (`apps/api/engines/vedic/chart_builder.py`)**:
   - `build_canonical_vedic_chart()` receives normalized time.
   - Instantiates `SkyfieldJPLProvider` (Phase 1D-R) pointing strictly to `DE440s.bsp`.
   - Produces geocentric planetary positions, true obliquity, local sidereal time, and canonical sidereal Ascendant/MC.
   - Creates the unified `CanonicalVedicChart` state.

4. **Yoga & Dosha Evaluation (`apps/api/engines/yoga_engine.py` wrapper)**:
   - `YogaEngine.detect_yogas()` acts as an adapter.
   - It directly invokes `YogaEvaluator.evaluate_all_yogas(chart)` and `DoshaEvaluator.evaluate_all_doshas(chart)`.
   - The result dictionary maps the new machine-readable evidence (`DETECTED`, `INDETERMINATE`, etc.) into the legacy JSON schema format for the front-end API.

5. **Prediction Engine / Report Aggregator**:
   - `EvidenceAggregator` uses the output of the wrapper.

## 3. Legacy Path Analysis
- The legacy engine `apps/api/engines/astronomical_engine.py` (Candidate C) is completely disconnected from this chain. It exists only for forensic benchmark referencing in tests.
- There are no duplicate astronomical recalculations inside `YogaEvaluator` or `DoshaEvaluator`.

## 4. Conclusion
The production path perfectly matches the certified architecture diagram. The `CanonicalVedicChart` serves as the exact single source of truth for all downstream rule evaluation.
