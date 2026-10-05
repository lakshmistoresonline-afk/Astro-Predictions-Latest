"""
Legacy Adapter Wrapper for Masterwork Engine.
Delegates ALL 16 Vargas, Jaimini Karakas, and Vimshottari Dashas to Authoritative Canonical Engines.
Sections 1, 2, 3 & 4 Compliance: Pure delegation adapter over AuthoritativeVargaEngine, JaiminiEngine, and AuthoritativeDashaEngine!
Strict longitude domain validation [0.0, 360.0) rejecting booleans for Jaimini. Reconciled Dasha return contract across all entry points!
"""
import math
from datetime import datetime
from typing import Dict, Any, Optional

from apps.api.engines.vedic.models import BirthInput, CanonicalVedicChart
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.varga.engine import VargaEngine as AuthoritativeVargaEngine
from apps.api.engines.jaimini.engine import JaiminiEngine
from apps.api.engines.dasha.engine import AuthoritativeDashaEngine

class MasterworkEngine:
    """
    Adapter wrapper ensuring single source of truth delegation to canonical engines.
    """

    @classmethod
    def calculate_all_16_vargas(cls, canonical_chart: CanonicalVedicChart) -> dict:
        """
        Delegates Varga calculations completely to AuthoritativeVargaEngine.
        """
        if not isinstance(canonical_chart, CanonicalVedicChart):
            raise ValueError("MasterworkEngine.calculate_all_16_vargas requires a CanonicalVedicChart instance.")
        return AuthoritativeVargaEngine.calculate_all_16_vargas(canonical_chart).model_dump()

    @staticmethod
    def calculate_jaimini_karakas(planetary_positions: dict) -> dict:
        """
        Delegates Jaimini Karaka calculations completely to canonical JaiminiEngine logic.
        Fails closed if any of the 7 core classical planets is missing or has invalid/out-of-range longitude.
        """
        if not isinstance(planetary_positions, dict):
            raise ValueError("planetary_positions must be a dictionary")

        seven_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        longitudes = {}
        for p in seven_planets:
            if p not in planetary_positions or not isinstance(planetary_positions[p], dict) or "longitude" not in planetary_positions[p]:
                raise ValueError(f"Required classical planet '{p}' is missing or has invalid longitude in planetary_positions.")
            lon = planetary_positions[p]["longitude"]
            if isinstance(lon, bool) or not isinstance(lon, (int, float)) or math.isnan(lon) or math.isinf(lon):
                raise ValueError(f"Longitude for planet '{p}' must be a finite numeric float (cannot be boolean).")
            if not (0.0 <= lon < 360.0):
                raise ValueError(f"Longitude for planet '{p}' ({lon}) must be in valid astronomical range [0.0, 360.0).")
            longitudes[p] = float(lon)

        return JaiminiEngine.calculate_chara_karakas_from_longitudes(longitudes)

    @classmethod
    def calculate_5_level_dasha_from_chart(cls, canonical_chart: CanonicalVedicChart) -> dict:
        """
        Delegates 5-level Vimshottari Dasha calculations completely to AuthoritativeDashaEngine.
        """
        res = AuthoritativeDashaEngine.calculate_dasha_suite(canonical_chart)
        current_md_dict = res.active_hierarchy.mahadasha.model_dump() if res.active_hierarchy else {}
        current_md_lord = res.active_hierarchy.mahadasha.lord_planet if res.active_hierarchy else "UNAVAILABLE"
        return {
            "current_mahadasha_lord": current_md_lord,
            "current_mahadasha": current_md_dict,
            "dasha_data": res.model_dump()
        }

    @classmethod
    def calculate_5_level_dasha(
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
    ) -> dict:
        """
        Delegates 5-level Vimshottari Dasha calculations completely to AuthoritativeDashaEngine with full birth parameters.
        """
        if hour is None or minute is None or second is None or latitude is None or longitude is None or not timezone_str:
            raise ValueError("hour, minute, second, latitude, longitude, and timezone_str must be explicitly provided.")

        try:
            parsed_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
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

        if "Moon" in chart.placements:
            calc_nak = chart.placements["Moon"].nakshatra_pada.nakshatra_name
            calc_pada = chart.placements["Moon"].nakshatra_pada.pada
            if moon_nakshatra and moon_nakshatra != calc_nak:
                raise ValueError(
                    f"Supplied moon_nakshatra '{moon_nakshatra}' disagrees with calculated Moon Nakshatra '{calc_nak}' at birth instant."
                )
            if nakshatra_pada is not None and nakshatra_pada != calc_pada:
                raise ValueError(
                    f"Supplied nakshatra_pada '{nakshatra_pada}' disagrees with calculated Moon Nakshatra Pada '{calc_pada}' at birth instant."
                )

        return cls.calculate_5_level_dasha_from_chart(chart)
