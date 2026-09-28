# Phase 2C: Authoritative Vimshottari Dasha Engine Validation Report

## 1. Executive Summary

This report documents the mathematical validation, 5-level nested hierarchy invariants, canonical chart verification, and independent test fixture results for **Phase 2C (Authoritative Vimshottari Dasha Engine)** of **Astrovision**.

---

## 2. Test Execution & Coverage Summary

- **Test Suite Location**: `apps/api/tests/test_dasha_engine.py`
- **Total Tests Executed**: 7 test modules (covering 10-chart personalization suite and 5-level hierarchy invariant checks)
- **Passed**: 7 (100%)
- **Failed**: 0
- **Execution Time**: ~14.44 seconds

---

## 3. Part 41 — Canonical Subramanian T S Dasha Validation Table

**Birth Data**: 1986-09-28, 16:30 IST (11:00 UTC), Palakkad, Kerala ($10.7867^\circ$ N, $76.6548^\circ$ E)

| Field / Parameter | Expected / Reference Value | Authoritative Engine Output | Difference / Status |
|---|---|---|---|
| **Moon Sidereal Longitude** | Cancer 07° 12' 18.7" ($97.2052^\circ$) | `97.2052°` | **Exact Match** |
| **Birth Nakshatra** | Pushya | `Pushya` | **Exact Match** |
| **Nakshatra Pada** | 2 | `2` | **Exact Match** |
| **Nakshatra Lord** | Saturn | `Saturn` | **Exact Match** |
| **Elapsed Fraction** | 0.290389 ($29.0\%$) | `0.290389` | **Exact Match** |
| **Remaining Fraction** | 0.709611 ($71.0\%$) | `0.709611` | **Exact Match** |
| **Birth Mahadasha** | Saturn (Total 19.0 Years) | `Saturn` (19.0 Years) | **Exact Match** |
| **Remaining Birth MD Balance** | ~13.4826 Years (~4,924.5 Days) | `13.4826 Years` | **Exact Match** |
| **First MD End Date (UTC)** | ~2000-03-22 | `2000-03-22T05:00:00+00:00` | **Exact Match** |
| **Active MD at Birth** | Saturn | `Saturn` | **Exact Match** |
| **Active AD at Birth** | Mercury | `Mercury` | **Exact Match** |
| **Active PD at Birth** | Saturn | `Saturn` | **Exact Match** |
| **Active Sookshma at Birth** | Sun | `Sun` | **Exact Match** |
| **Active Prana at Birth** | Venus | `Venus` | **Exact Match** |
| **Active MD (Query Date 2026-09-28)** | Venus | `Venus` | **Exact Match** |

---

## 4. Part 40 — Numerical Validation Table (10 Independent Charts)

Query Date for Active Dasha Hierarchy: Birth Datetime UTC.

| Chart ID | DOB & Time | Timezone & Location | Moon Sidereal Lon | Nakshatra (Pada) | Lord | Elap % | Rem % | Birth MD | MD Balance | 1st MD End Date | Active MD at Birth | Active AD | Active PD | Active Sookshma | Active Prana |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | 1986-09-28 16:30 | Asia/Kolkata (Palakkad) | $97.21^\circ$ | Pushya (2) | Saturn | $29.0\%$ | $71.0\%$ | Saturn | 13.48y | 2000-03-22 | Saturn | Mercury | Saturn | Sun | Venus |
| **2** | 1990-01-15 08:30 | Asia/Kolkata (Kochi) | $139.22^\circ$ | Purva Phalguni (2) | Venus | $44.1\%$ | $55.9\%$ | Venus | 11.17y | 2001-03-19 | Venus | Rahu | Mercury | Jupiter | Venus |
| **3** | 1985-07-22 18:45 | Europe/London (London) | $156.90^\circ$ | Uttara Phalguni (4) | Sun | $76.7\%$ | $23.3\%$ | Sun | 1.40y | 1986-12-15 | Sun | Mercury | Saturn | Moon | Venus |
| **4** | 2000-01-01 12:00 | UTC (Greenwich) | $199.47^\circ$ | Swati (4) | Rahu | $96.1\%$ | $3.9\%$ | Rahu | 0.71y | 2000-09-16 | Rahu | Mars | Ketu | Rahu | Sun |
| **5** | 2026-09-27 12:00 | America/New_York (New York) | $352.24^\circ$ | Revati (2) | Mercury | $41.8\%$ | $58.2\%$ | Mercury | 9.89y | 2036-08-19 | Mercury | Moon | Moon | Rahu | Saturn |
| **6** | 2050-01-01 12:00 | Asia/Tokyo (Tokyo) | $355.11^\circ$ | Revati (3) | Mercury | $63.3\%$ | $36.7\%$ | Mercury | 6.24y | 2056-03-28 | Mercury | Saturn | Rahu | Saturn | Ketu |
| **7** | 1950-06-15 12:00 | Europe/Paris (Paris) | $59.03^\circ$ | Mrigashira (2) | Mars | $42.7\%$ | $57.3\%$ | Mars | 4.01y | 1954-06-19 | Mars | Saturn | Sun | Rahu | Mercury |
| **8** | 1995-12-25 12:00 | Australia/Sydney (Sydney) | $290.67^\circ$ | Shravana (4) | Moon | $80.0\%$ | $20.0\%$ | Moon | 2.00y | 1997-12-23 | Moon | Venus | Venus | Jupiter | Moon |
| **9** | 2010-03-20 12:00 | Asia/Singapore (Singapore) | $24.76^\circ$ | Bharani (4) | Venus | $85.7\%$ | $14.3\%$ | Venus | 2.86y | 2013-01-29 | Venus | Ketu | Rahu | Jupiter | Venus |
| **10** | 2015-06-21 12:00 | Atlantic/Reykjavik (Reykjavik) | $123.22^\circ$ | Magha (1) | Ketu | $24.1\%$ | $75.9\%$ | Ketu | 5.31y | 2020-10-11 | Ketu | Sun | Rahu | Moon | Mercury |

---

## 5. Invariant & Boundary Validation Results

1. **Hierarchy Duration Invariants ($\sum \text{child durations} \equiv \text{parent duration}$)**:
   - Level 1 MD $\rightarrow$ Level 2 AD sum: Discrepancy $< 0.001$ days. `PASS`
   - Level 2 AD $\rightarrow$ Level 3 PD sum: Discrepancy $< 0.001$ days. `PASS`
   - Level 3 PD $\rightarrow$ Level 4 Sookshma sum: Discrepancy $< 0.001$ days. `PASS`
   - Level 4 Sookshma $\rightarrow$ Level 5 Prana sum: Discrepancy $< 0.001$ days. `PASS`

2. **Half-Open Boundary Rule `[start, end)` & Non-Overlap**:
   - For all consecutive sub-periods $C_k$ and $C_{k+1}$: $\text{end}(C_k) \equiv \text{start}(C_{k+1})$.
   - At any query datetime $t$, exactly **ONE** period is active per level. `PASS`

3. **Personalization & Hash Identity**:
   - 10 charts produced 10 distinct SHA-256 calculation hashes. `PASS`

4. **Fail-Closed Behavior**:
   - Missing Moon state, invalid timezone, or out-of-range query datetimes fail closed with explicit exceptions (`InvalidMoonStateError`, `OutOfQueryRangeError`). `PASS`

---

## 6. Files Changed & Deprecated

| File Path | Action | Description |
|---|---|---|
| `apps/api/engines/dasha/` | **[NEW]** | Authoritative 5-Level Vimshottari Dasha Engine Package |
| `apps/api/engines/dasha/calculator.py` | **[NEW]** | Nakshatra progress, $MD_{\text{balance}}$, and sub-period duration formulas |
| `apps/api/engines/dasha/timeline.py` | **[NEW]** | 5-level timeline generator & `get_dasha_at` query resolver |
| `apps/api/engines/dasha/engine.py` | **[NEW]** | `AuthoritativeDashaEngine` main class |
| `apps/api/engines/dasha/models.py` | **[NEW]** | Pydantic schema models for Dasha contracts |
| `apps/api/engines/dasha/hash.py` | **[NEW]** | Cryptographic SHA-256 calculation hash |
| `apps/api/engines/dasha/exceptions.py` | **[NEW]** | Custom fail-closed exceptions |
| `apps/api/engines/dasha_engine.py` | **[MODIFY]** | Legacy adapter wrapper delegating directly to `AuthoritativeDashaEngine` |
| `apps/api/tests/test_dasha_engine.py` | **[NEW]** | Comprehensive unit & invariant test suite |
| `docs/PHASE_2C_PREIMPLEMENTATION_AUDIT.md` | **[NEW]** | Repository audit report |
| `docs/DASHA_RULE_PROVENANCE.md` | **[NEW]** | Parashari rule provenance document |
| `docs/DASHA_TIME_CONVENTION.md` | **[NEW]** | Time scale & calendar convention specification |

---

## 7. Verification Verdict

# **PHASE 2C PASS**
