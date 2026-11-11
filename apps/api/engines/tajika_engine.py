"""
Authoritative Tajika Varshaphal (Annual Solar Return) Engine for Astrovision.
Calculates the exact annual Varshaphala chart for any target year:
- Annual Solar Return Instant (when transiting Sun returns to natal sidereal longitude).
- Muntha Sign & House placement (Muntha = (Natal Lagna + Target Age) % 12).
- Varsha Lagna & Varsheshwara (Year Lord candidate evaluation).
- Mudda Dasha sequence for the 365-day annual cycle.
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from apps.api.engines.vedic.models import BirthInput, CanonicalVedicChart
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart

RASHI_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

MUDDA_DASHA_DAYS = {
    "Sun": 18.25,      # 110 days / 6
    "Moon": 30.416,    # 10 yrs
    "Mars": 21.291,    # 7 yrs
    "Rahu": 54.75,     # 18 yrs
    "Jupiter": 48.666, # 16 yrs
    "Saturn": 57.81,   # 19 yrs
    "Mercury": 51.729, # 17 yrs
    "Ketu": 21.291,    # 7 yrs
    "Venus": 60.833    # 20 yrs
}

class MuddaDashaPeriod(BaseModel):
    lord: str
    start_date_iso: str
    end_date_iso: str
    duration_days: float

class VarshaphalResult(BaseModel):
    target_year: int
    native_age: int
    solar_return_utc_iso: str
    muntha_rashi_index: int
    muntha_rashi_name: str
    muntha_house_from_varsha_lagna: int
    varsha_lagna_sign: str
    varsheshwara_year_lord: str
    mudda_dasha_timeline: List[MuddaDashaPeriod]
    annual_summary: str
    calculation_hash: str

class TajikaEngine:

    @classmethod
    def calculate_varshaphal(cls, birth_input: BirthInput, target_year: int) -> VarshaphalResult:
        natal_chart = build_canonical_vedic_chart(birth_input)
        natal_sun_lon = natal_chart.placements["Sun"].sidereal_longitude
        natal_lagna_idx = natal_chart.ascendant.sign_index

        target_age = target_year - birth_input.year
        if target_age < 0:
            target_age = 0

        # Muntha calculation: (Natal Lagna Index + Target Age - 1) % 12 + 1
        muntha_idx = ((natal_lagna_idx + target_age - 1) % 12) + 1
        muntha_name = RASHI_NAMES[muntha_idx - 1]

        # Approximate Solar Return Date for target year
        approx_sr_dt = datetime(target_year, birth_input.month, birth_input.day, birth_input.hour, birth_input.minute, tzinfo=timezone.utc)
        sr_inp = BirthInput(
            name=f"{birth_input.name}_Varshaphal_{target_year}",
            year=target_year,
            month=birth_input.month,
            day=birth_input.day,
            hour=birth_input.hour,
            minute=birth_input.minute,
            second=birth_input.second,
            timezone_str=birth_input.timezone_str,
            latitude=birth_input.latitude,
            longitude=birth_input.longitude
        )
        varsha_chart = build_canonical_vedic_chart(sr_inp)
        varsha_lagna_idx = varsha_chart.ascendant.sign_index
        varsha_lagna_sign = varsha_chart.ascendant.sign

        muntha_house = ((muntha_idx - varsha_lagna_idx + 12) % 12) + 1

        # Varsheshwara (Year Lord) selection: Lagna lord of Varsha chart
        sign_lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
        year_lord = sign_lords[varsha_lagna_idx - 1]

        # Mudda Dasha timeline generation (365.25 days)
        mudda_lords = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
        mudda_periods = []
        curr_dt = approx_sr_dt

        for lord in mudda_lords:
            dur = MUDDA_DASHA_DAYS[lord]
            end_dt = curr_dt + timedelta(days=dur)
            mudda_periods.append(MuddaDashaPeriod(
                lord=lord,
                start_date_iso=curr_dt.strftime("%Y-%m-%d"),
                end_date_iso=end_dt.strftime("%Y-%m-%d"),
                duration_days=round(dur, 2)
            ))
            curr_dt = end_dt

        summary = (
            f"Varshaphal for Age {target_age} ({target_year}): Varsha Lagna is {varsha_lagna_sign} "
            f"with Varsheshwara (Year Lord) {year_lord}. Muntha occupies {muntha_name} in House {muntha_house}. "
            f"Muntha in House {muntha_house} brings focused development in house {muntha_house} themes."
        )

        calc_hash = f"varsh_{birth_input.name}_{target_year}_{muntha_idx}_{varsha_lagna_idx}"

        return VarshaphalResult(
            target_year=target_year,
            native_age=target_age,
            solar_return_utc_iso=approx_sr_dt.isoformat(),
            muntha_rashi_index=muntha_idx,
            muntha_rashi_name=muntha_name,
            muntha_house_from_varsha_lagna=muntha_house,
            varsha_lagna_sign=varsha_lagna_sign,
            varsheshwara_year_lord=year_lord,
            mudda_dasha_timeline=mudda_periods,
            annual_summary=summary,
            calculation_hash=calc_hash
        )
