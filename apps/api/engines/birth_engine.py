from datetime import datetime
import pytz
import math

class BirthDataEngine:
    """
    Dedicated BirthDataEngine for normalizing place, latitude, longitude,
    historical timezone, DST, UTC timestamp, and Julian Day.
    """

    CITY_TIMEZONES = {
        "new delhi": "Asia/Kolkata",
        "delhi": "Asia/Kolkata",
        "mumbai": "Asia/Kolkata",
        "bangalore": "Asia/Kolkata",
        "london": "Europe/London",
        "new york": "America/New_York",
        "tokyo": "Asia/Tokyo",
        "sydney": "Australia/Sydney"
    }

    @staticmethod
    def calculate_julian_day(year: int, month: int, day: int, hour: float = 0.0) -> float:
        """Calculates Julian Day Number from Gregorian calendar date and UTC hour."""
        if month <= 2:
            year -= 1
            month += 12
        A = math.floor(year / 100)
        B = 2 - A + math.floor(A / 4)
        JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5 + (hour / 24.0)
        return JD

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
        birth_time_accuracy: str = "exact"
    ) -> dict:
        tz_name = cls.CITY_TIMEZONES.get(place_name.lower().strip())
        if not tz_name:
            offset_hours = round(longitude / 15.0)
            tz_name = "UTC" if offset_hours == 0 else f"Etc/GMT{'-' if offset_hours > 0 else '+'}{abs(offset_hours)}"

        try:
            local_tz = pytz.timezone(tz_name)
        except Exception:
            local_tz = pytz.utc
            tz_name = "UTC"

        local_dt = datetime(year, month, day, hour, minute)

        try:
            localized_dt = local_tz.localize(local_dt, is_dst=None)
        except Exception:
            localized_dt = local_tz.localize(local_dt, is_dst=False)

        utc_dt = localized_dt.astimezone(pytz.utc)
        utc_hour = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
        julian_day = cls.calculate_julian_day(utc_dt.year, utc_dt.month, utc_dt.day, utc_hour)

        utc_offset = localized_dt.utcoffset().total_seconds() / 3600.0 if localized_dt.utcoffset() else 0.0
        dst_applied = localized_dt.dst().total_seconds() != 0 if localized_dt.dst() else False

        return {
            "name": name,
            "place_name": place_name,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
            "timezone_name": tz_name,
            "utc_offset": utc_offset,
            "dst_applied": dst_applied,
            "birth_local_datetime": localized_dt.isoformat(),
            "birth_utc_datetime": utc_dt.isoformat(),
            "julian_day": julian_day,
            "birth_time_accuracy": birth_time_accuracy,
            "engine_version": "1.0.0",
            "ephemeris_version": "swiss-ephemeris-2.10"
        }
