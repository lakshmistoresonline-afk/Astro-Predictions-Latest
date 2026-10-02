"""
Canonical Reference Fixture Adapter for Phase 2E-R4.1-R12-R10.
Explicitly transforms raw reference fixture JSON documents into validated BirthInput objects.
Provides strict validation and malformed fixture rejection.
"""
from typing import Dict, Any
from apps.api.engines.vedic.models import BirthInput

def reference_fixture_to_birth_input(ref_doc: Dict[str, Any]) -> BirthInput:
    """
    Transforms a reference fixture JSON document into a canonical BirthInput object.
    Supports both direct fields (local_year, local_month, etc.) and nested 'input' dictionaries.
    """
    if not isinstance(ref_doc, dict):
        raise ValueError("Malformed reference fixture: Expected a JSON object dictionary.")

    # Check if nested 'input' dict exists or use top-level fields
    data = ref_doc.get("input", ref_doc)

    required_keys = ["local_year", "local_month", "local_day", "local_hour", "local_minute", "latitude", "longitude"]

    # Also support year/month/day field names
    year = data.get("local_year") if "local_year" in data else data.get("year")
    month = data.get("local_month") if "local_month" in data else data.get("month")
    day = data.get("local_day") if "local_day" in data else data.get("day")
    hour = data.get("local_hour") if "local_hour" in data else data.get("hour")
    minute = data.get("local_minute") if "local_minute" in data else data.get("minute")
    lat = data.get("latitude")
    lon = data.get("longitude")

    if None in (year, month, day, hour, minute, lat, lon):
        missing = []
        if year is None: missing.append("local_year/year")
        if month is None: missing.append("local_month/month")
        if day is None: missing.append("local_day/day")
        if hour is None: missing.append("local_hour/hour")
        if minute is None: missing.append("local_minute/minute")
        if lat is None: missing.append("latitude")
        if lon is None: missing.append("longitude")
        raise ValueError(f"Malformed reference fixture: missing required birth input fields {missing}")

    tz_str = data.get("timezone_str") or data.get("timezone") or "Asia/Kolkata"

    return BirthInput(
        name=str(data.get("name") or data.get("fixture_id") or "Canonical Reference User"),
        year=int(year),
        month=int(month),
        day=int(day),
        hour=int(hour),
        minute=int(minute),
        second=int(data.get("local_second", data.get("second", 0))),
        timezone_str=str(tz_str),
        latitude=float(lat),
        longitude=float(lon)
    )
