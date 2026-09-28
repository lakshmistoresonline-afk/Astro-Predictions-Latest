# Astrovision Astronomical Date Range Requirements

## 1. Executive Overview

Astrovision requires high-precision astronomical ephemeris calculations across historical, contemporary, and long-term future time horizons. This document details the exact date boundaries derived from repository features and astrological calculation contracts.

---

## 2. Feature-by-Feature Date Requirement Analysis

| Feature Area | Min Date Supported | Max Date Supported | Repository Engine / File Reference | Justification & Astronomical Constraints |
|---|---|---|---|---|
| **Natal Birth Charts** | `1850-01-01` | `2050-12-31` | `apps/api/engines/birth_engine.py` | Accommodates multi-generational family charts, historical records, contemporary charts, and future newborn chart requests over a 200-year window. |
| **Vimshottari Dasha Cycles** | Birth Date | Birth Date + 120 Years | `apps/api/engines/dasha_engine.py` | Full Vimshottari Dasha timeline spans **120 solar years** (Ketu 7y, Venus 20y, Sun 6y, Moon 10y, Mars 7y, Rahu 18y, Jupiter 16y, Saturn 19y, Mercury 17y). A native born in 2030 requires accurate Dasha timeline projections through **2150-12-31**. |
| **5-Level Micro-Timing Hierarchy** | Birth Date | Birth Date + 120 Years | `apps/api/engines/masterwork_engine.py` | Calculates Mahadasha $\rightarrow$ Antardasha $\rightarrow$ Pratyantardasha $\rightarrow$ Sookshmadasha $\rightarrow$ Pranadasha hierarchies across the native's complete lifespan. |
| **Active Planetary Transits** | `1850-01-01` | `2150-12-31` | `apps/api/engines/report_engine.py` (Chapter 10) | Evaluates current and projected transit positions against natal longitudes for lifecycle event timing and transit predictions. |
| **Birth-Time Rectification** | Event Date - 100 Years | Event Date + 10 Years | `apps/api/engines/rectification_engine.py` | Evaluates life event timestamps against candidate birth times over extended past spans. |

---

## 3. Consolidated Date Range Summary

- **Minimum Required Date**: **1850-01-01** (JD `2396758.5`)
- **Maximum Required Date**: **2150-12-31** (JD `2506626.5`)
- **Total Continuous Horizon**: **300 Years** (1850 through 2150)

---

## 4. Verification & Ephemeris Compatibility

To satisfy all Astrovision requirements, any production ephemeris provider kernel MUST cover at least **1850-01-01 to 2150-12-31** without interpolation failure, extrapolation fallback, or boundary truncation errors.
