"""
Legacy Adapter Wrapper for Birth Data Processing.
Delegates time normalization to apps.api.engines.vedic.time_normalization.
"""
from datetime import datetime
import pytz

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.time_normalization import normalize_birth_time

class BirthDataEngine:
    """
    Adapter wrapper ensuring single source of truth delegation for time normalization and Julian Day.
    """

    @classmethod
    def process_birth_data(
        cls,
        name: str,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float,
        place_name: str,
        country: str,
        birth_time_accuracy: str = "exact",
        timezone_str: str = "Asia/Kolkata"
    ) -> dict:
        inp = BirthInput(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=0,
            timezone_str=timezone_str,
            latitude=latitude,
            longitude=longitude
        )

        norm = normalize_birth_time(inp)

        return {
            "name": name,
            "place_name": place_name,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
            "timezone_name": norm.timezone_identifier,
            "utc_offset": norm.utc_offset_hours,
            "birth_local_datetime": norm.local_datetime_iso,
            "birth_utc_datetime": norm.utc_datetime_iso,
            "julian_day": norm.julian_day_tt,
            "julian_day_tt": norm.julian_day_tt,
            "birth_time_accuracy": birth_time_accuracy,
            "engine_version": "6.0.0-Celestial-Astrolabe",
            "ephemeris_version": "NASA JPL DE440s via Skyfield 1.55"
        }
