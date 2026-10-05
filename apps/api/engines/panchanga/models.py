"""
Data Models for Panchanga Engine.
Defines strict schemas for Tithi, Vara, Nakshatra, Nitya Yoga, Karana, Solar/Lunar Times, and Inauspicious/Auspicious Periods.
Section 2 & 15 Compliance: Canonical 30-Tithi metadata schema with explicit Rikta, Amavasya, Purnima, and Vishti flags.
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class TithiInfo(BaseModel):
    """Tithi (Lunar Day - Canonical 30 Tithi Model)."""
    tithi_number: int = Field(description="1 to 30 global Tithi number")
    paksha_tithi_number: int = Field(default=1, description="1 to 15 index within Paksha")
    tithi_name: str = Field(description="e.g. Pratipada, Dwitiya, ..., Purnima, Amavasya")
    paksha: str = Field(description="Sukla Paksha or Krishna Paksha")
    is_rikta: bool = Field(default=False, description="True for Chaturthi, Navami, Chaturdashi")
    is_amavasya: bool = Field(default=False, description="True for Tithi 30")
    is_purnima: bool = Field(default=False, description="True for Tithi 15")
    degree_elapsed_in_tithi: float = Field(description="Degrees elapsed in current Tithi (0-12 deg)")
    percentage_elapsed: float = Field(description="Percentage elapsed (0-100%)")

class VaraInfo(BaseModel):
    """Vara (Solar Weekday)."""
    weekday_number: int = Field(description="0=Sunday, 1=Monday, ..., 6=Saturday")
    day_name_english: str
    day_name_sanskrit: str
    ruling_planet: str

class NityaYogaInfo(BaseModel):
    """Nitya Yoga (Solilunar Yoga - 27 Yogas)."""
    yoga_number: int = Field(description="1 to 27")
    yoga_name: str
    nature: str = Field(description="Auspicious or Inauspicious")

class KaranaInfo(BaseModel):
    """Karana (Half Lunar Day - 60 Karanas)."""
    karana_number: int = Field(description="1 to 60")
    karana_name: str
    type: str = Field(description="Movable or Fixed")
    nature: str = Field(description="Auspicious, Inauspicious, or Vishti/Bhadra")
    is_vishti: bool = Field(default=False, description="True for Vishti (Bhadra) Karana")

class TimingWindow(BaseModel):
    """Start and End datetime ISO window."""
    name: str
    start_time_iso: str
    end_time_iso: str
    nature: str = Field(description="Auspicious or Inauspicious")

class PanchangaResult(BaseModel):
    """Complete Panchanga Result."""
    datetime_iso: str
    location_name: str
    latitude: float
    longitude: float
    tithi: TithiInfo
    vara: VaraInfo
    nakshatra_name: str
    nakshatra_pada: int
    nitya_yoga: NityaYogaInfo
    karana: KaranaInfo
    sunrise_iso: str
    sunset_iso: str
    rahu_kalam: TimingWindow
    yamaganda: TimingWindow
    gulika_kalam: TimingWindow
    abhijit_muhurta: TimingWindow
    calculation_hash: str = Field(default="")
