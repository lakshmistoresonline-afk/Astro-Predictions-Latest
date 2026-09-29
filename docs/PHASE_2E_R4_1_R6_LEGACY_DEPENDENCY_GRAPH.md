# Phase 2E-R4.1-R6 Legacy Engine Isolation & Dependency Audit

## 1. Production Dependency Graph
```
POST /api/v1/birth-profile (apps/api/main.py)
        │
        ▼
ReportGeneratorEngine.generate_comprehensive_report (apps/api/engines/report_engine.py)
        │
        ▼
build_canonical_vedic_chart (apps/api/engines/vedic/chart_builder.py)
        │  [Skyfield 1.55 + NASA JPL DE440s Kernel]
        ▼
VargaEngine.calculate_all_16_vargas (apps/api/engines/varga/engine.py)
        │
        ▼
AshtakavargaEngine & ShadbalaEngine (apps/api/engines/strength/)
        │
        ▼
HTTP 200 JSON Response
```

## 2. Legacy Engine Isolation Audit
- `apps/api/engines/astronomy/` & `apps/api/engines/astronomical_engine.py` (Candidate C Meeus math): **UNREACHABLE** from any production route or report generation pipeline.
- `apps/api/engines/strength_engine.py` (Synthetic modulo math): **UNREACHABLE** from any production route or report generation pipeline.
- Production API handlers enforce strict schema validation via Pydantic models and fail closed if required birth input parameters are missing. No hardcoded Subramanian default fallbacks exist in production code paths.
