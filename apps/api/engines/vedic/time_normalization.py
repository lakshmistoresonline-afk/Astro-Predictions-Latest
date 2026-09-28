"""
Deterministic Time Scale Normalization Module.
Converts Local Civil Time to UTC and computes astronomical Julian Day (Terrestrial Time).
"""
import math
from datetime import datetime
import pytz

from apps.api.engines.vedic.exceptions import (
    TimezoneResolutionError,
    OutOfBoundaryError
)
from apps.api.engines.vedic.models import BirthInput, TimeNormalization


MIN_SUPPORTED_YEAR = 1850
MAX_SUPPORTED_YEAR = 2150

def normalize_birth_time(input_data: BirthInput) -> TimeNormalization:
    """
    Normalizes local civil time to UTC and Julian Day (TT).
    Strict fail-closed checks on supported astronomical date window (1850-01-01 to 2150-01-22).
    """
    # Boundary check
    if input_data.year < MIN_SUPPORTED_YEAR or input_data.year > MAX_SUPPORTED_YEAR:
        raise OutOfBoundaryError(
            f"Birth year {input_data.year} is outside the supported Astrovision date horizon "
            f"({MIN_SUPPORTED_YEAR}-01-01 through {MAX_SUPPORTED_YEAR}-01-22)."
        )
    if input_data.year == MAX_SUPPORTED_YEAR and (input_data.month > 1 or input_data.day > 22):
        raise OutOfBoundaryError(
            f"Birth date {input_data.year}-{input_data.month:02d}-{input_data.day:02d} exceeds "
            f"maximum supported boundary of {MAX_SUPPORTED_YEAR}-01-22."
        )

    # Timezone resolution
    try:
        tz = pytz.timezone(input_data.timezone_str)
    except Exception as e:
        raise TimezoneResolutionError(f"Failed to resolve timezone '{input_data.timezone_str}': {str(e)}")

    dt_local = datetime(
        input_data.year,
        input_data.month,
        input_data.day,
        input_data.hour,
        input_data.minute,
        input_data.second
    )

    try:
        dt_localized = tz.localize(dt_local)
    except Exception as e:
        raise TimezoneResolutionError(f"Ambiguous or non-existent local civil time {dt_local} in timezone '{input_data.timezone_str}': {str(e)}")

    dt_utc = dt_localized.astimezone(pytz.utc)
    utc_offset_hrs = dt_localized.utcoffset().total_seconds() / 3600.0

    # Julian Day calculation from UTC
    y = dt_utc.year
    m = dt_utc.month
    d = dt_utc.day
    h = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0

    if m <= 2:
        y -= 1
        m += 12

    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)
    jd_utc = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + (h / 24.0) + B - 1524.5

    return TimeNormalization(
        local_datetime_iso=dt_localized.isoformat(),
        timezone_identifier=input_data.timezone_str,
        utc_datetime_iso=dt_utc.isoformat(),
        utc_offset_hours=round(utc_offset_hrs, 4),
        julian_day_tt=round(jd_utc, 6),
        time_scale="UTC / TT"
    )
