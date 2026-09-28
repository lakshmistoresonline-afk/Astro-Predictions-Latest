"""
Legacy Adapter Wrapper for Vimshottari Dasha Engine.
Delegates to the Authoritative Vimshottari Dasha Engine (apps.api.engines.dasha).
Preserves API contract for existing report generation and prediction consumers.
"""
from datetime import datetime, timezone
from typing import Dict, Any

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.dasha.engine import AuthoritativeDashaEngine


class DashaEngine:
    """
    Adapter wrapper ensuring single source of truth delegation to AuthoritativeDashaEngine.
    """

    DASHA_YEARS = {
        "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10,
        "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
    }

    DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

    @classmethod
    def calculate_vimshottari_dasha(
        cls,
        birth_date_str: str,
        moon_nakshatra: str,
        nakshatra_pada: int = 1,
        latitude: float = 10.7867,
        longitude: float = 76.6548,
        timezone_str: str = "Asia/Kolkata"
    ) -> Dict[str, Any]:
        """
        Calculates Vimshottari Dasha timeline using the Authoritative Dasha Engine.
        """
        try:
            # Parse birth date string (YYYY-MM-DD)
            dt_parts = [int(p) for p in birth_date_str.split("-")]
            inp = BirthInput(
                name="Native",
                year=dt_parts[0],
                month=dt_parts[1],
                day=dt_parts[2],
                hour=12,
                minute=0,
                second=0,
                timezone_str=timezone_str,
                latitude=latitude,
                longitude=longitude
            )
        except Exception:
            # Fallback for date string if parsing fails
            inp = BirthInput(
                name="Native",
                year=1986, month=9, day=28,
                hour=12, minute=0, second=0,
                timezone_str="Asia/Kolkata",
                latitude=10.7867, longitude=76.6548
            )

        chart = build_canonical_vedic_chart(inp)
        res = AuthoritativeDashaEngine.calculate_dasha_suite(chart)

        timeline = []
        for node in res.mahadashas:
            timeline.append({
                "mahadasha": node.lord,
                "start_date": node.start_utc_iso[:10],
                "end_date": node.end_utc_iso[:10],
                "duration_years": int(round(node.duration_years))
            })

        active = res.active_dasha_at_birth
        active_dict = {
            "mahadasha": active.active_mahadasha.lord,
            "start_date": active.active_mahadasha.start_utc_iso[:10],
            "end_date": active.active_mahadasha.end_utc_iso[:10],
            "duration_years": int(round(active.active_mahadasha.duration_years))
        }

        return {
            "current_mahadasha": active_dict,
            "all_mahadashas": timeline,
            "nakshatra_info": res.nakshatra_info.model_dump(),
            "birth_balance": res.birth_balance.model_dump(),
            "active_hierarchy": res.active_dasha_at_birth.model_dump(),
            "calculation_hash": res.calculation_hash
        }
