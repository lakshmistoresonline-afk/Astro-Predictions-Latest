# Phase 2D-R4.1 Legacy Astronomy Path Audit

## 1. Scope
Trace the usage of `apps/api/engines/astronomical_engine.py`.

## 2. Findings
- **Production Path Unreachable**: As of the R4 remediation on `ReportGeneratorEngine`, the primary endpoint no longer invokes `AstronomicalEngine.calculate_positions()`. The system exclusively consumes `SkyfieldJPLProvider` via `build_canonical_vedic_chart()`.
- **Test Only Artifact**: The file `astronomical_engine.py` is still heavily invoked inside `apps/api/tests/ephemeris_benchmark/benchmark_runner.py` and `independent_validator.py`. These files are forensic benchmarks dating to Phase 1B/1C used explicitly to prove that "Candidate C" (the legacy Meeus engine) lacked the required sub-arcsecond accuracy compared to `Skyfield`.

## 3. Conclusion
**PASS.** The legacy engine is mathematically orphaned from the production calculation chain. Its existence is preserved solely as a forensic testing artifact.
