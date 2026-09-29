# Phase 2E-R4.1-R3 Production Dependency Audit

## Production Execution Path Graph
```
POST /api/v1/birth-profile
        ↓
ReportGeneratorEngine.generate_comprehensive_report
        ↓
build_canonical_vedic_chart (Skyfield 1.55 + NASA JPL DE440s)
        ↓
VargaEngine.calculate_all_16_vargas
        ↓
AshtakavargaEngine.calculate_ashtakavarga & ShadbalaEngine.calculate_shadbala_suite
        ↓
JSON Response
```

## Legacy Engine Reachability Audit
- `apps/api/engines/astronomical_engine.py` (Candidate C Meeus ephemeris): **UNREACHABLE** from production paths.
- `apps/api/engines/strength_engine.py` (Legacy synthetic modulo math): **UNREACHABLE** from production paths.
- No fallback or default birth chart injection exists in production API handlers. Missing inputs return HTTP 422 errors.
