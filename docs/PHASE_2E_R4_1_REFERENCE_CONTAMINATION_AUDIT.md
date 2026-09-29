# Phase 2E-R4.1 Reference Contamination Audit & Quarantine

## 1. Incident Analysis
A forensic audit identified that the script used to generate the Phase 2E-R4.1 reference dataset (`apps/api/tests/fixtures/phase_2e_r4_1_reference/`) imported and executed Astrovision's production astronomy engine:
```python
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
chart = build_canonical_vedic_chart(inp)
```
This created a circular chain where Astrovision's production astronomy generated the reference inputs that were fed into the independent oracle to produce expected values to validate Astrovision's production strength engines.

## 2. Remediation & Quarantine Action
- **Quarantine Action**: All reference JSON files created during that run have been moved from `apps/api/tests/fixtures/phase_2e_r4_1_reference/` to `apps/api/tests/fixtures/phase_2e_r4_1_contaminated_reference/`.
- **Absolute Prohibition**: No reference generation script, fixture generator, or oracle module may import `build_canonical_vedic_chart`, `SkyfieldJPLProvider`, `AstronomicalEngine`, or any `apps.api.engines.*` production module.
- **Independent Sourcing**: Reference astronomical inputs for R4.1-R1 will be sourced independently from static, externally verified Lahiri sidereal ephemeris reference tables and pure standalone astronomical calculations without calling Astrovision production code.
