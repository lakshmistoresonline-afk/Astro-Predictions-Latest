"""
Canonical Vedic Foundation Data Models.
Defines strict schemas for input, time normalization, Rashi, Nakshatra, Pada, Houses, and Canonical Chart.
Item 4 Compliance: Uses zoneinfo.ZoneInfo for timezone validation throughout!
"""
import zoneinfo
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional

class BirthInput(BaseModel):
    """Validated Canonical Birth Input."""
    name: str = Field(description="Full birth name")
    year: int = Field(description="Four-digit Gregorian birth year (1850-2150)")
    month: int = Field(description="Birth month (1-12)")
    day: int = Field(description="Birth day (1-31)")
    hour: int = Field(description="Local civil hour (0-23)")
    minute: int = Field(description="Local civil minute (0-59)")
    second: int = Field(default=0, description="Local civil second (0-59)")
    timezone_str: str = Field(description="Authoritative IANA timezone string (e.g. 'Asia/Kolkata')")
    latitude: float = Field(description="Geographic latitude in degrees [-90.0, 90.0]")
    longitude: float = Field(description="Geographic longitude in degrees [-180.0, 180.0]")
    elevation_m: float = Field(default=0.0, description="Observer elevation above sea level in meters")

    @field_validator("timezone_str")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Timezone string cannot be empty.")
        tz_clean = v.strip()
        try:
            zoneinfo.ZoneInfo(tz_clean)
        except Exception:
            try:
                import pytz
                pytz.timezone(tz_clean)
            except Exception as e:
                raise ValueError(f"Unknown or unresolvable IANA timezone string '{v}': {str(e)}")
        return tz_clean

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if not (-90.0 <= v <= 90.0):
            raise ValueError(f"Latitude {v} out of physical range [-90.0, 90.0].")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if not (-180.0 <= v <= 180.0):
            raise ValueError(f"Longitude {v} out of physical range [-180.0, 180.0].")
        return v

class TimeNormalization(BaseModel):
    """Normalized Time Outputs with explicit UTC and Terrestrial Time (TT) Julian Days."""
    local_datetime_iso: str
    timezone_identifier: str
    utc_datetime_iso: str
    utc_offset_hours: float
    julian_day_utc: float = Field(description="Julian Day in Universal Time Coordinated (UT/UTC)")
    julian_day_tt: float = Field(description="Julian Day in Terrestrial Time (TT)")
    time_scale: str = "UTC / TT"

class RashiPosition(BaseModel):
    """Full Precision Rashi (Zodiac Sign) Placement."""
    absolute_longitude: float = Field(description="Absolute sidereal longitude [0.0, 360.0)")
    sign: str = Field(description="Zodiac sign name")
    sign_index: int = Field(description="1-based sign index (1 = Aries, 12 = Pisces)")
    degree: int = Field(description="Degrees within sign [0, 29]")
    minute: int = Field(description="Arcminutes within degree [0, 59]")
    second: float = Field(description="Arcseconds within minute [0.0, 60.0)")

class NakshatraPada(BaseModel):
    """Full Precision Nakshatra and Pada Placement."""
    nakshatra: str = Field(description="Nakshatra name (e.g., 'Pushya')")
    nakshatra_index: int = Field(description="1-based Nakshatra index [1, 27]")
    absolute_start_deg: float = Field(description="Absolute start longitude of Nakshatra")
    absolute_end_deg: float = Field(description="Absolute end longitude of Nakshatra")
    degree_within_nakshatra: float = Field(description="Degrees within Nakshatra [0.0, 13.3333)")
    pada: int = Field(description="Pada number [1, 4]")

class PlanetaryVedicPlacement(BaseModel):
    """Combined Astronomical and Vedic placement for a celestial body."""
    body_name: str
    geocentric_tropical_lon: float
    geocentric_latitude: float
    distance_au: float
    velocity_deg_day: float
    retrograde: bool
    sidereal_longitude: float
    rashi: RashiPosition
    nakshatra_pada: NakshatraPada

class WholeSignHouse(BaseModel):
    """Whole Sign House Metadata."""
    house_number: int = Field(description="1-based house number [1, 12]")
    sign: str = Field(description="Zodiac sign occupying the house")
    sign_index: int = Field(description="1-based sign index [1, 12]")
    start_longitude: float = Field(description="Start longitude of house in sidereal zodiac")
    end_longitude: float = Field(description="End longitude of house in sidereal zodiac")

class CanonicalVedicChart(BaseModel):
    """Complete Canonical Vedic Chart Object."""
    input_data: BirthInput
    time_normalization: TimeNormalization
    ayanamsha_mode: str = "Lahiri"
    ayanamsha_value_deg: float
    ascendant: RashiPosition
    mc: RashiPosition
    placements: Dict[str, PlanetaryVedicPlacement]
    whole_sign_houses: List[WholeSignHouse]
    calculation_hash: str
    metadata: Dict[str, str]
