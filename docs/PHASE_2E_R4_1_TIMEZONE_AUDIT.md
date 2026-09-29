# Phase 2E-R4.1 Timezone & DST Audit

## Timezone Normalization
- All local civil timestamps in `apps/api/tests/fixtures/phase_2e_r4_1_reference/` preserve the exact local civil parameters (`local_year`, `local_month`, `local_day`, `local_hour`, `local_minute`, `timezone_str`).
- `build_canonical_vedic_chart` converts local civil time to strict UTC ISO-8601 strings and Julian Day Numbers (`julian_day_tt`) using `pytz`.
- Differential testing across 10 global birth locations (London BST, Los Angeles PDT, Tokyo JST, Sydney AEST, Reykjavik UTC, etc.) confirms that Hora, Vara, Masa, Varsha, Nathonnatha, and Tribhaga Balas modulate accurately based on local civil time and astronomical UTC time.
