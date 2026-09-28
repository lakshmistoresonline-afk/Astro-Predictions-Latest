"""
Canonical Data Schema Models for Vimshottari Dasha Engine (Phase 2C).
Supports 5-level nested hierarchy (Mahadasha, Antardasha, Pratyantardasha, Sookshma, Prana) and query responses.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class BirthNakshatraInfo(BaseModel):
    """Full precision Birth Nakshatra and Progress Details."""
    nakshatra_index: int = Field(description="1-based Nakshatra index [1, 27]")
    nakshatra_name: str = Field(description="Nakshatra name")
    nakshatra_lord: str = Field(description="Planetary lord governing the Nakshatra")
    pada: int = Field(description="Pada number [1, 4]")
    start_longitude_deg: float = Field(description="Absolute start longitude of Nakshatra [0, 360)")
    end_longitude_deg: float = Field(description="Absolute end longitude of Nakshatra [0, 360)")
    moon_sidereal_longitude_deg: float = Field(description="Moon's canonical sidereal longitude [0, 360)")
    elapsed_degrees: float = Field(description="Elapsed degrees within Nakshatra [0, 13.3333)")
    remaining_degrees: float = Field(description="Remaining degrees within Nakshatra [0, 13.3333)")
    elapsed_fraction: float = Field(description="Fraction of Nakshatra elapsed at birth [0.0, 1.0]")
    remaining_fraction: float = Field(description="Fraction of Nakshatra remaining at birth [0.0, 1.0]")

class BirthDashaBalance(BaseModel):
    """Remaining Birth Mahadasha Balance."""
    mahadasha_lord: str
    total_mahadasha_years: float
    remaining_years: float
    remaining_days: float
    birth_utc_datetime_iso: str
    first_mahadasha_end_utc_iso: str

class DashaPeriodNode(BaseModel):
    """A single period node in the Vimshottari timeline hierarchy."""
    level: int = Field(description="Hierarchy level: 1=MD, 2=AD, 3=PD, 4=Sookshma, 5=Prana")
    level_name: str = Field(description="Level name ('Mahadasha', 'Antardasha', etc.)")
    lord: str = Field(description="Planetary lord governing this period")
    sequence_index: int = Field(description="1-based sequence index within parent [1, 9]")
    start_utc_iso: str = Field(description="UTC start datetime (ISO-8601, inclusive)")
    end_utc_iso: str = Field(description="UTC end datetime (ISO-8601, exclusive)")
    duration_days: float = Field(description="Exact duration in days (365.25 d/yr)")
    duration_years: float = Field(description="Duration in Vimshottari years")

class ActiveDashaHierarchy(BaseModel):
    """Active Dasha levels for an arbitrary query datetime."""
    query_utc_iso: str
    active_mahadasha: DashaPeriodNode
    active_antardasha: DashaPeriodNode
    active_pratyantardasha: DashaPeriodNode
    active_sookshma: DashaPeriodNode
    active_prana: DashaPeriodNode
    elapsed_days_in_prana: float
    remaining_days_in_prana: float
    percentage_elapsed_in_prana: float
    percentage_remaining_in_prana: float

class FullVimshottariDashaResult(BaseModel):
    """Complete Output Contract for Vimshottari Dasha Engine."""
    birth_utc_datetime_iso: str
    moon_sidereal_longitude_deg: float
    nakshatra_info: BirthNakshatraInfo
    birth_balance: BirthDashaBalance
    mahadashas: List[DashaPeriodNode]
    active_dasha_at_birth: ActiveDashaHierarchy
    dasha_convention: str = "Parashari Vimshottari (120 Years)"
    time_convention: str = "Tropical Solar Year (365.25 Days/Year)"
    calculation_hash: str
    astronomy_state_hash: str
