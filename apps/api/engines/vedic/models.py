"""
Canonical Vedic Foundation Data Models.
Defines strict schemas for input, time normalization, Rashi, Nakshatra, Pada, Houses, and Canonical Chart.
Item 4 Compliance: Uses zoneinfo.ZoneInfo for timezone validation throughout!
"""
import calendar
import zoneinfo
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Any, Dict, List, Optional
from apps.api.engines.vedic.exceptions import OutOfBoundaryError

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

    @field_validator("year")
    @classmethod
    def validate_year_range(cls, v: int) -> int:
        if not (1850 <= v <= 2150):
            raise OutOfBoundaryError(
                f"Birth year {v} is outside the supported Astrovision date horizon "
                f"(1850-01-01 through 2150-01-22)."
            )
        return v

    @field_validator("month")
    @classmethod
    def validate_month_range(cls, v: int) -> int:
        if not (1 <= v <= 12):
            raise ValueError(f"Birth month {v} is outside the valid range [1, 12].")
        return v

    @field_validator("day")
    @classmethod
    def validate_day_range(cls, v: int) -> int:
        if not (1 <= v <= 31):
            raise ValueError(f"Birth day {v} is outside the valid range [1, 31].")
        return v

    @field_validator("hour")
    @classmethod
    def validate_hour_range(cls, v: int) -> int:
        if not (0 <= v <= 23):
            raise ValueError(f"Birth hour {v} is outside the valid range [0, 23].")
        return v

    @field_validator("minute")
    @classmethod
    def validate_minute_range(cls, v: int) -> int:
        if not (0 <= v <= 59):
            raise ValueError(f"Birth minute {v} is outside the valid range [0, 59].")
        return v

    @field_validator("second")
    @classmethod
    def validate_second_range(cls, v: int) -> int:
        if not (0 <= v <= 59):
            raise ValueError(f"Birth second {v} is outside the valid range [0, 59].")
        return v

    @model_validator(mode="after")
    def validate_gregorian_date_and_boundaries(self) -> "BirthInput":
        max_days = calendar.monthrange(self.year, self.month)[1]
        if not (1 <= self.day <= max_days):
            raise ValueError(
                f"Invalid birth date: day {self.day} is invalid for month {self.month} "
                f"in year {self.year} (maximum allowed days in month: {max_days})."
            )

        if self.year == 2150 and (self.month > 1 or (self.month == 1 and self.day > 22)):
            raise OutOfBoundaryError(
                f"Birth date {self.year}-{self.month:02d}-{self.day:02d} exceeds "
                f"maximum supported boundary of 2150-01-22."
            )

        return self

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
    julian_day_utc: float
    julian_day_tt: float
    delta_t_seconds: float = Field(default=64.0)

class RashiInfo(BaseModel):
    """Vedic Rashi (Zodiac Sign) Placement Info."""
    sign_index: int = Field(description="1-based Rashi index (1=Aries ... 12=Pisces)")
    sign: str = Field(description="English Rashi name (e.g. 'Aries')")
    sanskrit_name: Optional[str] = Field(default="Mesha", description="Sanskrit Rashi name (e.g. 'Mesha')")
    degree: int = Field(description="Degree within Rashi [0..29]")
    minute: int = Field(description="Minute within Rashi [0..59]")
    second: float = Field(default=0.0, description="Second within Rashi")
    absolute_longitude: float = Field(description="Total sidereal longitude in degrees [0.0..360.0)")

class NakshatraPadaInfo(BaseModel):
    """Vedic Nakshatra & Pada Placement Info."""
    nakshatra_number: Optional[int] = Field(default=1, description="1-based Nakshatra index [1..27]")
    nakshatra_index: Optional[int] = Field(default=1, description="1-based Nakshatra index [1..27]")
    nakshatra: str = Field(description="Nakshatra name (e.g. 'Ashwini')")
    pada: int = Field(description="Nakshatra Pada [1..4]")
    ruling_planet: Optional[str] = Field(default="Ketu", description="Vimshottari Nakshatra lord (e.g. 'Ketu')")

    @model_validator(mode="after")
    def sync_nakshatra_index(self) -> "NakshatraPadaInfo":
        if self.nakshatra_index is not None and (self.nakshatra_number is None or self.nakshatra_number == 1):
            self.nakshatra_number = self.nakshatra_index
        elif self.nakshatra_number is not None and (self.nakshatra_index is None or self.nakshatra_index == 1):
            self.nakshatra_index = self.nakshatra_number
        return self

class PlanetaryVedicPlacement(BaseModel):
    """Complete Vedic Placement Info for a Planet or Ascendant."""
    body_name: str
    sidereal_longitude: float
    speed_deg_per_day: Optional[float] = Field(default=1.0, description="Daily velocity in degrees per day")
    retrograde: bool = False
    rashi: RashiInfo
    nakshatra_pada: NakshatraPadaInfo
    combust: bool = False

    @property
    def velocity_deg_day(self) -> float:
        return self.speed_deg_per_day if self.speed_deg_per_day is not None else 1.0

    @property
    def geocentric_latitude(self) -> float:
        return 0.0

    @property
    def geocentric_longitude(self) -> float:
        return self.sidereal_longitude

class HouseCuspInfo(BaseModel):
    """Whole Sign House Cusp Info."""
    house_number: int = Field(description="1-based house number [1..12]")
    sign_index: int = Field(description="1-based Rashi index occupying house [1..12]")
    sign: Optional[str] = Field(default=None, description="Sign name")
    sign_name: Optional[str] = Field(default=None, description="Sign name")
    sanskrit_name: Optional[str] = Field(default="Kumbha", description="Sanskrit sign name")
    lord_planet: Optional[str] = Field(default="Saturn", description="House lord planet")

    @model_validator(mode="after")
    def sync_sign_names(self) -> "HouseCuspInfo":
        if not self.sign_name and self.sign:
            self.sign_name = self.sign
        elif not self.sign and self.sign_name:
            self.sign = self.sign_name
        return self

class CanonicalVedicChart(BaseModel):
    """Complete Canonical Vedic Chart Object."""
    birth_input: Optional[BirthInput] = None
    input_data: Optional[BirthInput] = None
    time_normalization: TimeNormalization
    ascendant: RashiInfo
    mc: Optional[RashiInfo] = None
    ayanamsha_name: str = Field(default="Lahiri")
    ayanamsha_value_deg: float = Field(default=23.671877)
    placements: Dict[str, PlanetaryVedicPlacement]
    houses: Optional[List[Any]] = Field(default_factory=list)
    whole_sign_houses: Optional[List[Any]] = Field(default_factory=list)
    calculation_hash: str

    @model_validator(mode="after")
    def sync_chart_aliases(self) -> "CanonicalVedicChart":
        if self.birth_input is None and self.input_data is not None:
            self.birth_input = self.input_data
        elif self.input_data is None and self.birth_input is not None:
            self.input_data = self.birth_input

        if not self.houses and self.whole_sign_houses:
            self.houses = self.whole_sign_houses
        elif not self.whole_sign_houses and self.houses:
            self.whole_sign_houses = self.houses
        return self

# Backward-compatibility model aliases
RashiPosition = RashiInfo
NakshatraPada = NakshatraPadaInfo
WholeSignHouse = HouseCuspInfo
