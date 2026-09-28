# Phase 2D-R4 Forensic Repository Audit

## 1. Objective
Identify all rules, evaluators, duplicate astronomical code, legacy logic, and rule-evaluation pipelines to ensure strict adherence to Phase 2A canonical charting and separation of concerns.

## 2. Legacy Code & Duplicate Astronomy Analysis
| File | Component | Role | Disposition |
|---|---|---|---|
| `apps/api/engines/astronomical_engine.py` | `AstronomicalEngine` | Legacy Meeus math | **DANGEROUS DUPLICATE**. Used by `report_engine.py` and `masterwork_engine.py`. Must be removed from production path to prevent duplicate / conflicting astronomy. |
| `apps/api/engines/masterwork_engine.py` | `MasterworkEngine` | Legacy Vargas & Dasha Mock | **DANGEROUS DUPLICATE**. Contains mocked 5-level Dasha calculation and an obsolete 16-Varga calculation that does not use Phase 2B `VargaEngine`. Needs adaptation/removal. |
| `apps/api/engines/vedic_engine.py` | `VedicEngine` | Analysis / Aspects | Redundant if replacing legacy astronomy, but safe if mapping canonical data into its expected format. |

## 3. Yoga & Dosha Evaluators
- `apps/api/engines/yogas/evaluator.py`: `YogaEvaluator` - Cleanly consumes `CanonicalVedicChart`. Uses Phase 2A data.
- `apps/api/engines/yogas/rules.py`: Contains implementations for Mahapurusha, Gaja Kesari, Budha Aditya, Dharma-Karma, Parivartana, Viparita, Neecha Bhanga, Chandra, and Surya yogas.
- `apps/api/engines/doshas/evaluator.py`: `DoshaEvaluator` - Cleanly consumes `CanonicalVedicChart`. Uses Phase 2A data.
- `apps/api/engines/doshas/rules.py`: Contains Manglik, Kemadruma, Kala Sarpa implementations.
- `apps/api/engines/yoga_engine.py`: Adapter wrapper. Currently consumes `BirthInput` directly but falls back to Subramanian T.S. if missing.

## 4. Production API Flow (`apps/api/main.py`)
Currently, `main.py` -> `ReportGeneratorEngine` -> `AstronomicalEngine.calculate_positions()`.
This bypasses Phase 2A `build_canonical_vedic_chart` entirely! The legacy adapter `YogaEngine.detect_yogas` is called with no `birth_input`, defaulting all users to Subramanian T.S.!
**Risk**: HIGH. Total violation of personalized astrology logic.
**Disposition**: `ReportGeneratorEngine.generate_comprehensive_report` MUST be refactored to construct a `BirthInput`, pass it to `build_canonical_vedic_chart()`, map its outputs to `planetary_positions` for legacy backwards-compatibility, and explicitly pass the chart down to `VargaEngine`, `AuthoritativeDashaEngine`, and `YogaEngine`/`YogaEvaluator`.
