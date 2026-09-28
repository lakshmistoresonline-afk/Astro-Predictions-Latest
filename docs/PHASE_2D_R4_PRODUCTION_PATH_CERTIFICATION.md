# Phase 2D-R4 Production Path Certification

## 1. Trace of Production Execution (API to Report)

### PRE-R4 STATE (Defective):
`apps/api/main.py` -> `ReportGeneratorEngine.generate_comprehensive_report` -> `AstronomicalEngine.calculate_positions` (Legacy Meeus math).
`ReportGeneratorEngine` then passed `planetary_positions` to `YogaEngine.detect_yogas` without `birth_input`. `YogaEngine` defaulted to Subramanian T.S. (1986). Thus, ALL API calls returned the 1986 Yoga suite.

### POST-R4 REMEDIATION (Certified):
1. **API Endpoint**: `POST /api/v1/birth-profile` accepts user input.
2. **Report Generator**: `ReportGeneratorEngine.generate_comprehensive_report` builds a strict `BirthInput` object.
3. **Phase 2A Canonical State**: Invokes `build_canonical_vedic_chart(inp)` which securely calls `SkyfieldJPLProvider` (`DE440s.bsp`).
4. **Data Mapping**: To preserve downstream legacy components without rewriting the entire app, the `CanonicalVedicChart`'s placements are mapped to the old `planetary_positions` dict format.
5. **Phase 2B Vargas**: Delegates to `VargaEngine.calculate_all_16_vargas(canonical_chart)`.
6. **Phase 2C Dashas**: Delegates to `AuthoritativeDashaEngine.calculate_dasha_suite(canonical_chart)`.
7. **Phase 2D Yogas/Doshas**: Delegates directly to `YogaEvaluator.evaluate_all_yogas(canonical_chart)` and `DoshaEvaluator.evaluate_all_doshas(canonical_chart)`.

## 2. Legacy Engine Unreachability
The `apps/api/engines/astronomical_engine.py` (Candidate C) is now completely excised from the `ReportGeneratorEngine` production pathway. It exists in the repository strictly for archival test-harness bench-marking (e.g., `test_ephemeris_accuracy.py`). 

## 3. Personalization and Data Isolation
Because `YogaEngine` no longer receives empty `birth_input`, the default fallback is never triggered in production. Every user request dynamically generates a unique `CanonicalVedicChart` and corresponding SHA-256 calculation hash, guaranteeing complete data isolation and true personalization.
