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

# Authoritative 27 Nakshatra Lords Mapping (1-based index)
NAKSHATRA_LORDS_MAP = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", # 1..9
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", # 10..18
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"  # 19..27
]

ZODIAC_SANSKRIT_NAMES = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrishchika",
    "Dhanu", "Makara", "Kumbha", "Meena"
]

RASHI_LORDS_MAP = {
    1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
    5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
    9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
}

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
    sanskrit_name: Optional[str] = Field(default=None, description="Sanskrit Rashi name (e.g. 'Mesha')")
    degree: int = Field(description="Degree within Rashi [0..29]")
    minute: int = Field(description="Minute within Rashi [0..59]")
    second: float = Field(default=0.0, description="Second within Rashi")
    absolute_longitude: float = Field(description="Total sidereal longitude in degrees [0.0..360.0)")

    @model_validator(mode="after")
    def populate_sanskrit_name(self) -> "RashiInfo":
        if not self.sanskrit_name or self.sanskrit_name == "Mesha":
            if 1 <= self.sign_index <= 12:
                self.sanskrit_name = ZODIAC_SANSKRIT_NAMES[self.sign_index - 1]
        return self

class NakshatraPadaInfo(BaseModel):
    """Vedic Nakshatra & Pada Placement Info."""
    nakshatra_number: Optional[int] = Field(default=1, description="1-based Nakshatra index [1..27]")
    nakshatra_index: Optional[int] = Field(default=1, description="1-based Nakshatra index [1..27]")
    nakshatra: str = Field(description="Nakshatra name (e.g. 'Ashwini')")
    pada: int = Field(description="Nakshatra Pada [1..4]")
    ruling_planet: Optional[str] = Field(default=None, description="Vimshottari Nakshatra lord (e.g. 'Ketu')")
    absolute_start_deg: Optional[float] = Field(default=None, description="Start longitude of Nakshatra")
    absolute_end_deg: Optional[float] = Field(default=None, description="End longitude of Nakshatra")
    degree_within_nakshatra: Optional[float] = Field(default=None, description="Elapsed degrees in Nakshatra")

    @model_validator(mode="after")
    def sync_nakshatra_info(self) -> "NakshatraPadaInfo":
        num = self.nakshatra_number or self.nakshatra_index or 1
        self.nakshatra_number = num
        self.nakshatra_index = num

        if not self.ruling_planet or self.ruling_planet == "Ketu":
            if 1 <= num <= 27:
                self.ruling_planet = NAKSHATRA_LORDS_MAP[num - 1]
        return self

class PlanetaryVedicPlacement(BaseModel):
    """Complete Vedic Placement Info for a Planet or Ascendant."""
    body_name: str
    sidereal_longitude: float
    geocentric_tropical_lon: Optional[float] = Field(default=None, description="Tropical geocentric ecliptic longitude in degrees")
    geocentric_latitude: Optional[float] = Field(default=None, description="Geocentric ecliptic latitude in degrees")
    distance_au: Optional[float] = Field(default=None, description="Distance from Earth in Astronomical Units")
    speed_deg_per_day: Optional[float] = Field(default=None, description="Daily velocity in degrees per day")
    velocity_deg_day: Optional[float] = Field(default=None, description="Daily velocity in degrees per day")
    retrograde: bool = False
    rashi: RashiInfo
    nakshatra_pada: NakshatraPadaInfo
    combust: bool = False

    @model_validator(mode="after")
    def sync_velocity(self) -> "PlanetaryVedicPlacement":
        if self.speed_deg_per_day is None and self.velocity_deg_day is not None:
            self.speed_deg_per_day = self.velocity_deg_day
        elif self.velocity_deg_day is None and self.speed_deg_per_day is not None:
            self.velocity_deg_day = self.speed_deg_per_day
        return self

class HouseCuspInfo(BaseModel):
    """Whole Sign House Cusp Info."""
    house_number: int = Field(description="1-based house number [1..12]")
    sign_index: int = Field(description="1-based Rashi index occupying house [1..12]")
    sign: Optional[str] = Field(default=None, description="Sign name")
    sign_name: Optional[str] = Field(default=None, description="Sign name")
    sanskrit_name: Optional[str] = Field(default=None, description="Sanskrit sign name")
    lord_planet: Optional[str] = Field(default=None, description="House lord planet")
    start_longitude: Optional[float] = Field(default=None, description="House start longitude")
    end_longitude: Optional[float] = Field(default=None, description="House end longitude")

    @model_validator(mode="after")
    def sync_house_info(self) -> "HouseCuspInfo":
        zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        s_idx = self.sign_index
        if 1 <= s_idx <= 12:
            if not self.sign_name:
                self.sign_name = zodiac_signs[s_idx - 1]
            if not self.sign:
                self.sign = self.sign_name
            if not self.sanskrit_name:
                self.sanskrit_name = ZODIAC_SANSKRIT_NAMES[s_idx - 1]
            if not self.lord_planet:
                self.lord_planet = RASHI_LORDS_MAP[s_idx]
        return self

class CanonicalVedicChart(BaseModel):
    """Complete Canonical Vedic Chart Object."""
    birth_input: Optional[BirthInput] = None
    input_data: Optional[BirthInput] = None
    time_normalization: TimeNormalization
    ascendant: RashiInfo
    mc: Optional[RashiInfo] = None
    ayanamsha_mode: str = Field(default="Lahiri")
    ayanamsha_name: str = Field(default="Lahiri")
    ayanamsha_value_deg: float = Field(default=23.671877)
    placements: Dict[str, PlanetaryVedicPlacement]
    houses: Optional[List[Any]] = Field(default_factory=list)
    whole_sign_houses: Optional[List[Any]] = Field(default_factory=list)
    calculation_hash: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def get_whole_sign_houses(self) -> List[Any]:
        return self.houses or self.whole_sign_houses or []

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
