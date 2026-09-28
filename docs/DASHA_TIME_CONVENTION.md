# Vimshottari Dasha Time Scale & Calendar Conventions — Astrovision (Phase 2C)

## 1. Executive Summary

This document defines the calendar arithmetic conventions, time scales, interval boundary rules, and timezone handling for the **Vimshottari Dasha Engine** (Phase 2C) in **Astrovision**.

---

## 2. Dasha Year & Calendar Convention

### Selected Calendar Standard
- **CANONICAL TIME STANDARD**: **Tropical Solar Year ($365.25 \text{ Days}$)**
- **RATIONALE**:
  1. $365.25 \text{ days/year}$ directly aligns with standard UTC civil calendar date arithmetic (`datetime.timedelta`).
  2. $120 \text{ Vimshottari Years} \equiv 43,830.0 \text{ Days} \equiv 120 \text{ Julian Solar Years}$.
  3. Ensures precise, seamless alignment between UTC birth timestamps, current active queries, and future predictions without calendar drift.

---

## 3. Boundary Interval Convention

### Half-Open Interval Rule `[start, end)`
All Dasha periods (Mahadasha, Antardasha, Pratyantardasha, Sookshma, Prana) are defined as **half-open intervals**:
$$\text{Period} = [\text{Start Datetime}, \text{End Datetime})$$

- **INVARIANT 1 (Exact Active Uniqueness)**: At any query datetime $t$, exactly **ONE** period is active at each hierarchy level.
- **INVARIANT 2 (Zero Gaps / Zero Overlaps)**: For consecutive sub-periods $C_k$ and $C_{k+1}$:
  $$\text{End Datetime}(C_k) \equiv \text{Start Datetime}(C_{k+1})$$
- **INVARIANT 3 (Parent Boundary Equality)**:
  $$\text{Start Datetime}(C_1) \equiv \text{Start Datetime}(P)$$
  $$\text{End Datetime}(C_9) \equiv \text{End Datetime}(P)$$

---

## 4. Timezone & DST Handling

1. All birth dates and times are localized to their authoritative IANA timezone (`pytz`) and converted to UTC timestamps.
2. Dasha timelines and queries are computed using **timezone-aware UTC datetime objects** (`datetime.now(timezone.utc)` / ISO-8601 strings).
3. Ambiguous local times (DST overlap) or nonexistent local times (DST gap) fail closed immediately during input validation (`TimezoneResolutionError`).
