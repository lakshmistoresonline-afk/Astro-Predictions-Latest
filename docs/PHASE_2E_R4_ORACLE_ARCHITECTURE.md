# Phase 2E-R4 Oracle Architecture

## Zero-Trust Independent Architecture
The Phase 2E-R4 oracle package in `apps/api/tests/oracles/phase_2e_r4/` is designed with zero dependencies on production engines:

1. **Independent State**: Uses `IndependentChart` (`independent_chart.py`) to hold astronomical parameters.
2. **Independent Astronomy & Geometry**:
   - `independent_geometry.py`: Shortest angular distance, declination (`independent_declination`), and aspectual power (`independent_drishti_pinda`).
   - `independent_calendar.py`: Weekday, Vara, Hora, Masa, and Varsha lords derived from Julian Day.
   - `independent_varga.py`: Independent calculation of D1, D2, D3, D7, D9, D12, D30 varga sign indices (1-12) directly from longitude without importing `VargaEngine`.
3. **Independent Strength Rules**:
   - `independent_ashtakavarga.py`: Pure BAV and SAV matrices.
   - `independent_shadbala.py`: Pure Sthana, Dig, Kala, Cheshta, Naisargika, Drik Balas.
4. **Zero-Trust Import Isolation**: `test_r4_independence.py` verifies both AST static isolation and runtime monkeypatch isolation.
