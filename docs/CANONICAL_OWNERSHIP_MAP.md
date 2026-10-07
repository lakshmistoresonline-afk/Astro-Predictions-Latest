# Astrovision Canonical Ownership & Engine Dependency Map

## 1. Core Architectural Principle
Astrovision strictly enforces **Single Source of Truth** for all astronomical, astrological, and predictive computations.
No downstream module or API route calculates astronomy or astrology independently. Every calculation flows through its designated authoritative engine.

```
BirthInput
   │
   ▼
[ 1. Time Normalization ] ──► (apps/api/engines/vedic/time_normalization.py)
   │
   ▼
[ 2. Astronomy Engine ] ────► (apps/api/engines/astronomy/providers/skyfield_jpl.py - DE440s)
   │
   ▼
[ 3. Vedic Chart Builder ] ─► (apps/api/engines/vedic/chart_builder.py)
   │
   ├─► [ 4. 16 Vargas Engine ] ────────► (apps/api/engines/varga/engine.py)
   ├─► [ 5. Vimshottari Dasha ] ────────► (apps/api/engines/dasha/engine.py)
   ├─► [ 6. Yoga Evaluation Engine ] ──► (apps/api/engines/yogas/evaluator.py)
   ├─► [ 7. Dosha Evaluation Engine ] ──► (apps/api/engines/doshas/evaluator.py)
   ├─► [ 8. Shadbala Strength Engine ] ─► (apps/api/engines/strength/shadbala.py)
   ├─► [ 9. Ashtakavarga Engine ] ──────► (apps/api/engines/strength/ashtakavarga.py)
   ├─► [ 10. Jaimini Engine ] ──────────► (apps/api/engines/jaimini/engine.py)
   ├─► [ 11. Transit Engine ] ──────────► (apps/api/engines/transit/engine.py)
   ├─► [ 12. Panchanga Engine ] ────────► (apps/api/engines/panchanga/engine.py)
   ├─► [ 13. Muhurta Engine ] ──────────► (apps/api/engines/muhurta/engine.py)
   └─► [ 14. Timing Engine ] ───────────► (apps/api/engines/timing/engine.py)
   │
   ▼
[ Master Evidence Pipeline ] ────────► (apps/api/engines/canonical_evidence.py)
   │
   ├─► [ Prediction Evidence Engine ] ─► (apps/api/engines/prediction_engine.py)
   ├─► [ Report Generator Engine ] ────► (apps/api/engines/report_engine.py)
   ├─► [ PDF / HTML Treatise Engine ] ─► (apps/api/engines/pdf_report_engine.py)
   └─► [ AI Interpretation Service ] ─► (apps/api/services/ai_service.py)
```

## 2. Canonical Ownership Matrix

| Domain | Authoritative Engine Implementation File | Primary Entry Point Method | Model / Contract Output |
| :--- | :--- | :--- | :--- |
| **Astronomy** | `apps/api/engines/astronomy/providers/skyfield_jpl.py` | `SkyfieldJPLProvider.calculate_astronomical_state` | `AstronomicalState` |
| **Time Normalization** | `apps/api/engines/vedic/time_normalization.py` | `normalize_birth_time` | `TimeNormalization` |
| **Vedic Chart** | `apps/api/engines/vedic/chart_builder.py` | `build_canonical_vedic_chart` | `CanonicalVedicChart` |
| **16 Vargas** | `apps/api/engines/varga/engine.py` | `VargaEngine.calculate_all_16_vargas` | `Full16VargaSuite` |
| **Vimshottari Dasha** | `apps/api/engines/dasha/engine.py` | `AuthoritativeDashaEngine.calculate_dasha_suite` | `FullVimshottariDashaResult` |
| **Classical Yogas** | `apps/api/engines/yogas/evaluator.py` | `YogaEvaluator.evaluate_all_yogas` | `YogaSuiteResult` |
| **Classical Doshas** | `apps/api/engines/doshas/evaluator.py` | `DoshaEvaluator.evaluate_all_doshas` | `DoshaSuiteResult` |
| **Shadbala Strength** | `apps/api/engines/strength/shadbala.py` | `AuthoritativeShadbalaEngine.calculate_shadbala_suite` | `ShadbalaSuiteResult` |
| **Ashtakavarga BAV/SAV**| `apps/api/engines/strength/ashtakavarga.py` | `AuthoritativeAshtakavargaEngine.calculate_ashtakavarga` | `AshtakavargaSuiteResult` |
| **Jaimini Sutras** | `apps/api/engines/jaimini/engine.py` | `JaiminiEngine.calculate_jaimini_suite` | `JaiminiSuiteResult` |
| **Planetary Transits** | `apps/api/engines/transit/engine.py` | `TransitEngine.calculate_transit_snapshot` | `TransitSnapshot` |
| **Panchanga Elements** | `apps/api/engines/panchanga/engine.py` | `PanchangaEngine.calculate_panchanga` | `PanchangaResult` |
| **Activity Muhurtas** | `apps/api/engines/muhurta/engine.py` | `MuhurtaEngine.evaluate_all_activities` | `MuhurtaSuiteResult` |
| **Predictive Timing** | `apps/api/engines/timing/engine.py` | `TimingEngine.generate_timing_suite` | `TimingSuiteResult` |
| **Domain Predictions** | `apps/api/engines/prediction_engine.py` | `PredictionEngine.generate_all_predictions` | `ComprehensivePredictionPackage` |
| **Report Generation** | `apps/api/engines/report_engine.py` | `ReportGeneratorEngine.generate_comprehensive_report` | `Dict[str, Any]` (12 Chapters) |
| **PDF Treatise Export** | `apps/api/engines/pdf_report_engine.py` | `PDFReportEngine.generate_pdf_report` | `bytes` (HTML/PDF) |
| **AI Evidence Synthesis**| `apps/api/services/ai_service.py` | `AIService.synthesize_interpretation` | `Dict[str, Any]` |

## 3. Legacy Adapter Policy
Top-level legacy wrapper modules (`astronomical_engine.py`, `vedic_engine.py`, `varga_engine.py`, `dasha_engine.py`, `strength_engine.py`, `yoga_engine.py`) serve strictly as thin facade delegates pointing directly to their authoritative single-source-of-truth engines. Zero calculation logic is duplicated inside wrapper adapters.
