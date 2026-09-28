# Phase 2D-R4.1 Default Profile Audit

## 1. Objective
Ensure no hidden fallback or default birth chart automatically loads when missing or partial parameters are passed to the API.

## 2. Findings
- In the initial code, `YogaEngine.detect_yogas()` contained a direct fallback to Subramanian T.S. (1986) if no `BirthInput` was explicitly passed.
- This was **removed** and refactored in the Phase 2D remediation. The API path (`apps/api/main.py`) correctly instantiates the `BirthInput` from the network request. The `ReportGeneratorEngine` passes this `BirthInput` directly into the canonical chart generator, and the resulting exact chart is passed by reference to `YogaEvaluator`.
- The `Subramanian` profile now only exists legitimately in test fixtures and documentation matrices (e.g., `test_yoga_independent_oracle.py`, `test_reference_chart.py`, and JSON audit dumps).

## 3. Conclusion
**PASS.** No default profile contaminates production endpoint execution. Missing planetary evidence correctly defaults to `INDETERMINATE` at the evaluation layer.
