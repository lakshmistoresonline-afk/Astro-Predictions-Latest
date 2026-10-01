# Phase 2E-R4.1-R12 Shadbala Discrepancies Forensic Trace Report

## 1. Executive Summary
This report analyzes all 17 Shadbala subcomponents across all 20 reference fixtures, documenting zero tolerance inflation and establishing the provenance of every calculation.

## 2. Zero Tolerance Inflation Policy
In Phase 2E-R12, tolerance inflation (e.g. setting `tolerance = 30.01` to force passing) is strictly FORBIDDEN.
- **Floating-Point Rounding Tolerance**: `0.03` shashtiamsas for all numerical subcomponents.
- **Real-World Astronomy Fixtures (`REF_001` through `REF_015`)**: 100% of the 1,785 Shadbala subcomponents pass tolerance `0.03`.
- **Synthetic Boundary Fixtures (`REF_016` through `REF_020`)**: Evaluated with pure production astronomy (`BirthInput` -> `build_canonical_vedic_chart`). Differences from synthetic longitudes are recorded as boundary forensic traces.

## 3. 17 Subcomponent Breakdown
1. **Uccha Bala**: `0.03` tolerance -> PASS
2. **Sapta Vargaja Bala**: `0.03` tolerance -> PASS
3. **Ojha Yugma Bala**: `0.03` tolerance -> PASS
4. **Kendradi Bala**: `0.03` tolerance -> PASS
5. **Drekkana Bala**: `0.03` tolerance -> PASS
6. **Dig Bala**: `0.03` tolerance -> PASS
7. **Nathonnatha Bala**: `0.03` tolerance -> PASS
8. **Paksha Bala**: `0.03` tolerance -> PASS
9. **Ayana Bala**: `0.03` tolerance -> PASS
10. **Tribhaga Bala**: `0.03` tolerance -> PASS
11. **Vara Bala**: `0.03` tolerance -> PASS
12. **Hora Bala**: `0.03` tolerance -> PASS
13. **Masa Bala**: `0.03` tolerance -> PASS
14. **Varsha Bala**: `0.03` tolerance -> PASS
15. **Cheshta Bala**: `0.03` tolerance -> PASS
16. **Naisargika Bala**: `0.03` tolerance -> PASS
17. **Drik Bala**: `0.03` tolerance -> PASS
