# Astrovision Birth-Time Normalization & Timezone Pipeline

## 1. Pipeline Overview
Birth-time normalization transforms local civil birth particulars into Universal Time Coordinated (UTC) and astronomical Julian Day time scales (UTC & Terrestrial Time TT) for sub-arcsecond NASA JPL DE440s ephemeris evaluation.

```
[ BirthInput (Local Civil Particulars + IANA Timezone) ]
                        │
                        ▼
[ IANA Time Zone Resolution via Python zoneinfo.ZoneInfo ]
                        │
                        ▼
[ Local Civil Datetime (dt_local with explicit ZoneInfo) ]
                        │
                        ▼
[ UTC Normalization (dt_utc = dt_local.astimezone(UTC)) ]
                        │
                        ▼
[ Julian Day UTC Calculation (Meeus Astronomical Algorithms) ]
                        │
                        ▼
[ NASA Espenak-Meeus (TP-2006-214141) Delta-T Calculation (TT - UT) ]
                        │
                        ▼
[ Astronomical Terrestrial Time Julian Day (julian_day_tt) ]
```

## 2. Key Design Principles
1. **Mandatory IANA Timezone Keys**: No silent timezone defaults (e.g. `Asia/Kolkata` fallbacks removed). Every birth profile request requires an explicit IANA timezone string (e.g. `Asia/Kolkata`, `Europe/London`, `America/New_York`, `Australia/Sydney`).
2. **Historical Timezone & DST Accuracy**: Timezone resolution relies on Python's built-in `zoneinfo.ZoneInfo`, which uses the official IANA Time Zone Database (`tzdata`). This accounts for historical Daylight Saving Time (DST) transitions, wartime clock shifts, and regional offset changes for all global locations back to 1850.
3. **Time Scale Separation**:
   - `local_datetime_iso`: Local civil time in observer's `ZoneInfo` (used for local civil date and Vara/weekday).
   - `utc_datetime_iso`: UTC normalized datetime (`dt_utc`).
   - `utc_offset_hours`: Exact UTC offset in hours at the birth instant.
   - `julian_day_utc`: Julian Day in Universal Time Coordinated.
   - `julian_day_tt`: Julian Day in Terrestrial Time ($JD_{TT} = JD_{UTC} + \Delta T / 86400$).
4. **NASA Espenak-Meeus Delta-T Polynomials**: High-precision Delta-T ($\Delta T = TT - UT$) polynomials covering the complete 1850-2150 date horizon based on NASA TP-2006-214141.
5. **Rectification Preservation**: Birth time rectification candidate generation preserves `base_birth_input.timezone_str` 100% across all evaluated candidate offsets.
