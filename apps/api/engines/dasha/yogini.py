"""
Authoritative Yogini Dasha Engine (36-Year Cycle) for Astrovision.
Calculates the 36-year Yogini Dasha sequence and active Yogini period for any native:
1. Mangala   (Moon)    — 1 Year
2. Pingala   (Sun)     — 2 Years
3. Dhanya    (Jupiter) — 3 Years
4. Bhramari  (Mars)    — 4 Years
5. Bhadrika  (Mercury) — 5 Years
6. Ulka      (Saturn)  — 6 Years
7. Siddha    (Venus)   — 7 Years
8. Sankata   (Rahu)    — 8 Years
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from apps.api.engines.vedic.models import CanonicalVedicChart

YOGINI_ORDER = [
    ("Mangala", "Moon", 1.0),
    ("Pingala", "Sun", 2.0),
    ("Dhanya", "Jupiter", 3.0),
    ("Bhramari", "Mars", 4.0),
    ("Bhadrika", "Mercury", 5.0),
    ("Ulka", "Saturn", 6.0),
    ("Siddha", "Venus", 7.0),
    ("Sankata", "Rahu", 8.0)
]

TOTAL_YOGINI_CYCLE_YEARS = 36.0
DAYS_PER_YEAR = 365.25

class YoginiDashaPeriod(BaseModel):
    yogini_name: str
    ruling_planet: str
    start_date_iso: str
    end_date_iso: str
    duration_years: float

class YoginiDashaResult(BaseModel):
    birth_yogini: str
    ruling_planet: str
    remaining_birth_years: float
    yogini_periods: List[YoginiDashaPeriod]
    active_yogini: Optional[YoginiDashaPeriod] = None
    calculation_hash: str

class YoginiDashaEngine:

    @classmethod
    def calculate_yogini_dasha(
        cls,
        canonical_chart: CanonicalVedicChart,
        query_dt_utc: Optional[datetime] = None
    ) -> YoginiDashaResult:
        if "Moon" not in canonical_chart.placements:
            raise ValueError("Moon placement missing from canonical chart.")

        moon_p = canonical_chart.placements["Moon"]
        nak_num = moon_p.nakshatra_pada.nakshatra_number  # 1 to 27
        rem_frac = moon_p.nakshatra_pada.degree_within_nakshatra / 13.333333
        rem_frac = max(0.0, min(1.0, 1.0 - rem_frac))

        # Yogini index formula: (Nakshatra Number + 3) % 8
        yog_idx = (nak_num + 3) % 8
        if yog_idx == 0:
            yog_idx = 8

        birth_yogini_tuple = YOGINI_ORDER[yog_idx - 1]
        birth_yog_name, birth_planet, full_years = birth_yogini_tuple

        rem_years = full_years * rem_frac

        # Birth date UTC
        time_norm = canonical_chart.time_normalization
        birth_dt = datetime.fromisoformat(time_norm.utc_datetime_iso)

        periods = []

        # 1st Yogini Period
        first_dur_days = rem_years * DAYS_PER_YEAR
        end_dt = birth_dt + timedelta(days=first_dur_days)
        periods.append(YoginiDashaPeriod(
            yogini_name=birth_yog_name,
            ruling_planet=birth_planet,
            start_date_iso=birth_dt.strftime("%Y-%m-%d"),
            end_date_iso=end_dt.strftime("%Y-%m-%d"),
            duration_years=round(rem_years, 2)
        ))

        curr_dt = end_dt
        curr_idx = yog_idx % 8  # Next yogini

        # Generate 36-year cycles (up to 3 cycles = 108 years)
        for _ in range(24):
            y_name, y_planet, y_years = YOGINI_ORDER[curr_idx]
            y_days = y_years * DAYS_PER_YEAR
            next_dt = curr_dt + timedelta(days=y_days)
            periods.append(YoginiDashaPeriod(
                yogini_name=y_name,
                ruling_planet=y_planet,
                start_date_iso=curr_dt.strftime("%Y-%m-%d"),
                end_date_iso=next_dt.strftime("%Y-%m-%d"),
                duration_years=y_years
            ))
            curr_dt = next_dt
            curr_idx = (curr_idx + 1) % 8

        active_p = None
        if query_dt_utc:
            q_str = query_dt_utc.strftime("%Y-%m-%d")
            for p in periods:
                if p.start_date_iso <= q_str <= p.end_date_iso:
                    active_p = p
                    break

        calc_hash = f"yogini_{birth_dt.isoformat()}_{nak_num}_{yog_idx}"

        return YoginiDashaResult(
            birth_yogini=birth_yog_name,
            ruling_planet=birth_planet,
            remaining_birth_years=round(rem_years, 2),
            yogini_periods=periods,
            active_yogini=active_p,
            calculation_hash=calc_hash
        )
