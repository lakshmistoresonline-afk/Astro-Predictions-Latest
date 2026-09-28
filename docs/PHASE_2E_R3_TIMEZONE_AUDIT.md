# Phase 2E-R3 Timezone & DST Audit

## Timezone Normalization
- All incoming local civil birth times are normalized to strict UTC ISO-8601 strings and Julian Day Numbers (`julian_day_tt`) via Phase 2A `time_normalization.py` using `pytz`.
- Time-dependent Kala Bala components (Nathonnatha, Vara, Hora, Masa, Varsha) utilize the normalized `julian_day_tt` and UTC birth hours.
- Differential testing across 10 global birth locations (including London BST, Los Angeles PDT, Tokyo JST, Sydney AEST, and Reykjavik UTC) verifies that timezone offsets and DST transitions modulate Kala Bala scores accurately.
