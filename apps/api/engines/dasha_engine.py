"""
Legacy Adapter Wrapper for Vimshottari Dasha Engine.
Delegates to the Authoritative Vimshottari Dasha Engine (apps.api.engines.dasha).
Preserves API contract for existing report generation and prediction consumers.
Section 4, 5, 6 & 7 Compliance:
- Strict calendar date validation via datetime.strptime.
- Fails closed if Moon placement is missing from calculated chart.
- Imports DASHA_YEARS and DASHA_ORDER from canonical Dasha engine (apps.api.engines.dasha).
- Validates supplied moon_nakshatra and nakshatra_pada against canonical chart calculation.
- Requires explicit hour, minute, second, location, and timezone parameters. Zero silent location or noon defaults!
"""
from datetime import datetime
from typing import Dict, Any, Optional

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.dasha import AuthoritativeDashaEngine, DASHA_YEARS, DASHA_ORDER


class DashaEngine:
    """
    Adapter wrapper ensuring single source of truth delegation to AuthoritativeDashaEngine.
    """

    DASHA_YEARS = DASHA_YEARS
    DASHA_ORDER = DASHA_ORDER

    @classmethod
    def calculate_vimshottari_dasha(
        cls,
        birth_date_str: str,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float,
        timezone_str: str,
        second: int = 0,
        moon_nakshatra: Optional[str] = None,
        nakshatra_pada: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calculates Vimshottari Dasha timeline using the Authoritative Dasha Engine.
        Fails closed if birth_date_str, hour, minute, latitude, longitude, or timezone_str is invalid/missing.
        Validates supplied moon_nakshatra and nakshatra_pada against canonical chart calculation.
        """
        if hour is None or minute is None or second is None or latitude is None or longitude is None or not timezone_str:
            raise ValueError("hour, minute, second, latitude, longitude, and timezone_str must be explicitly provided for Dasha calculation.")

        if not (0 <= hour <= 23) or not (0 <= minute <= 59) or not (0 <= second <= 59):
            raise ValueError("hour (0-23), minute (0-59), and second (0-59) must be within valid time bounds.")

        # Section 4: Strict calendar date validation
        try:
            parsed_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"birth_date_str '{birth_date_str}' must be a valid real calendar date in YYYY-MM-DD format.")

        try:
            inp = BirthInput(
                name="Native",
                year=parsed_date.year,
                month=parsed_date.month,
                day=parsed_date.day,
                hour=hour,
                minute=minute,
                second=second,
                timezone_str=timezone_str,
                latitude=latitude,
                longitude=longitude
            )
        except Exception as e:
            raise ValueError(f"Invalid birth parameters for Dasha calculation: {str(e)}")

        chart = build_canonical_vedic_chart(inp)

        # Section 4 Compliance: Fail closed if Moon is missing from canonical chart placements
        if "Moon" not in chart.placements:
            raise ValueError("Moon placement is missing from calculated canonical chart.")

        calc_nak = chart.placements["Moon"].nakshatra_pada.nakshatra
        calc_pada = chart.placements["Moon"].nakshatra_pada.pada
        if moon_nakshatra and moon_nakshatra != calc_nak:
            raise ValueError(
                f"Supplied moon_nakshatra '{moon_nakshatra}' disagrees with calculated Moon Nakshatra '{calc_nak}' at birth instant."
            )
        if nakshatra_pada is not None:
            if not (1 <= nakshatra_pada <= 4):
                raise ValueError("nakshatra_pada must be an integer between 1 and 4.")
            if nakshatra_pada != calc_pada:
                raise ValueError(
                    f"Supplied nakshatra_pada '{nakshatra_pada}' disagrees with calculated Moon Nakshatra Pada '{calc_pada}' at birth instant."
                )

        res = AuthoritativeDashaEngine.calculate_dasha_suite(chart)

        return {
            "birth_balance": res.birth_balance.model_dump(),
            "mahadasha_periods": [m.model_dump() for m in res.mahadashas],
            "current_mahadasha": res.active_hierarchy.mahadasha.model_dump() if res.active_hierarchy else {},
            "calculation_hash": res.calculation_hash
        }
