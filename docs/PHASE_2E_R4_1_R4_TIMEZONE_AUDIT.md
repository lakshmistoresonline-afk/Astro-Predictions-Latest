# Phase 2E-R4.1-R4 Timezone & DST Audit

## 1. Audit Summary
- All local civil timestamps in `reference_source/inputs/` preserve local civil date/time (`local_year`, `local_month`, `local_day`, `local_hour`, `local_minute`) and IANA timezone strings (`Asia/Kolkata`, `Europe/London`, `America/New_York`, `Asia/Tokyo`, `Australia/Sydney`, `Europe/Paris`, `Atlantic/Reykjavik`, `Asia/Singapore`, `America/Los_Angeles`, `Europe/Berlin`, `Africa/Cairo`, `America/Argentina/Buenos_Aires`, `Pacific/Honolulu`).
- Production normalization converts local civil time to UTC using `pytz`.
- Differential testing across global locations confirms that time-dependent Kala Bala components (Vara, Hora, Masa, Varsha, Nathonnatha, Tribhaga) modulate accurately based on local civil time and astronomical UTC.
