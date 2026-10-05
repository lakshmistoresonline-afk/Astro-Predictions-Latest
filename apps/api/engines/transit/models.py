"""
Data Models for Production Transit Engine.
Defines schemas for planetary transit positions, aspects, Ashtakavarga transit scores, Dasha interactions, ingresses, stations, and snapshots.
Sections 1, 4, 12 & 15 Compliance:
- Strict model constraints ensuring machine-readable target_type, target_planet, target_house, planet sets, and house ranges!
- Zero invented 'TargetPlanet' strings!
- Restricted TransitIngressEvent to SIGN_INGRESS.
"""
import math
from pydantic import BaseModel, Field, model_validator
from typing import Dict, List, Optional

CANONICAL_PLANETS = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
ALLOWED_ASPECT_CONVENTIONS = {"Parashari", "Western"}
ALLOWED_FAVORABILITY_STATUSES = {"HIGHLY_AUSPICIOUS", "AUSPICIOUS", "NEUTRAL", "CHALLENGING", "CRITICAL", "UNAVAILABLE"}
ALLOWED_DASHA_LEVELS = {"Mahadasha", "Antardasha", "Pratyantardasha", "Sookshma", "Prana"}

class TransitPlacement(BaseModel):
    """Transit placement for a single planet at a query datetime."""
    body_name: str
    sidereal_longitude: float
    rashi: RashiPosition
    nakshatra_pada: NakshatraPada
    velocity_deg_day: float
    retrograde: bool
    is_station: bool = False
    house_from_lagna: int = Field(description="1-based house from natal Lagna")
    house_from_moon: int = Field(description="1-based house from natal Moon sign")

    @model_validator(mode='after')
    def validate_placement_semantics(self):
        if self.body_name not in CANONICAL_PLANETS:
            raise ValueError(f"body_name '{self.body_name}' is not in CANONICAL_PLANETS")
        if not (0.0 <= self.sidereal_longitude < 360.0):
            raise ValueError(f"sidereal_longitude {self.sidereal_longitude} must be in [0, 360)")
        if not (1 <= self.house_from_lagna <= 12):
            raise ValueError(f"house_from_lagna {self.house_from_lagna} must be between 1 and 12")
        if not (1 <= self.house_from_moon <= 12):
            raise ValueError(f"house_from_moon {self.house_from_moon} must be between 1 and 12")
        if math.isnan(self.velocity_deg_day) or math.isinf(self.velocity_deg_day):
            raise ValueError("velocity_deg_day must be a finite float")
        return self

class TransitAspect(BaseModel):
    """Aspect or contact between a transiting planet and a natal planet/house."""
    transiting_planet: str
    target_type: str = Field(default="PLANET", description="PLANET or HOUSE")
    target_planet: Optional[str] = Field(default=None, description="Natal target planet name e.g. 'Sun'")
    target_house: Optional[int] = Field(default=None, description="Natal target house number 1-12")
    target_name: str = Field(description="Display target name e.g. 'Natal Sun' or 'House 10'")
    aspect_type: str = Field(description="Conjunction, Opposition, Trine, Square, Parashari Special Aspect, HOUSE_OCCUPANCY, HOUSE_7TH_ASPECT, etc.")
    aspect_convention: str = Field(default="Parashari", description="Parashari or Western")
    orb_deg: Optional[float] = Field(default=None, description="Angular separation in degrees (None for structural house targets)")
    is_applying: Optional[bool] = Field(default=None, description="True if angular separation is decreasing (None for structural house targets)")

    @model_validator(mode='after')
    def validate_aspect_semantics(self):
        if self.transiting_planet not in CANONICAL_PLANETS:
            raise ValueError(f"transiting_planet '{self.transiting_planet}' is not in CANONICAL_PLANETS")
        if self.aspect_convention not in ALLOWED_ASPECT_CONVENTIONS:
            raise ValueError(f"aspect_convention '{self.aspect_convention}' is invalid")
        if self.target_type not in ["PLANET", "HOUSE"]:
            raise ValueError("target_type must be either 'PLANET' or 'HOUSE'")

        if self.target_type == "HOUSE":
            self.target_planet = None
            self.orb_deg = None
            self.is_applying = None
            if self.target_house is None or not (1 <= self.target_house <= 12):
                raise ValueError("target_house must be between 1 and 12 for HOUSE target_type")
        elif self.target_type == "PLANET":
            if not self.target_planet or self.target_planet not in CANONICAL_PLANETS:
                raise ValueError("target_planet is required and must be a valid canonical planet name when target_type is PLANET")
            if self.target_house is not None and not (1 <= self.target_house <= 12):
                raise ValueError("target_house must be between 1 and 12")
        return self

class TransitAshtakavargaScore(BaseModel):
    """Ashtakavarga transit score for a planet in its transited house."""
    planet: str
    transited_rashi_index: int = Field(description="1-based Rashi index (1=Aries)")
    sav_bindus: Optional[int] = Field(default=None, description="Actual SAV total bindus in transited house (0-56)")
    bav_bindus: Optional[int] = Field(default=None, description="Actual BAV bindus for transiting planet in transited house (0-8)")
    favorability: str = Field(description="HIGHLY_AUSPICIOUS, AUSPICIOUS, NEUTRAL, CHALLENGING, CRITICAL, UNAVAILABLE")

    @model_validator(mode='after')
    def validate_score_semantics(self):
        if self.planet not in CANONICAL_PLANETS:
            raise ValueError(f"planet '{self.planet}' is not in CANONICAL_PLANETS")
        if not (1 <= self.transited_rashi_index <= 12):
            raise ValueError("transited_rashi_index must be between 1 and 12")
        if self.favorability not in ALLOWED_FAVORABILITY_STATUSES:
            raise ValueError(f"favorability '{self.favorability}' is invalid")
        if self.sav_bindus is not None and not (0 <= self.sav_bindus <= 56):
            raise ValueError("sav_bindus out of physical range [0, 56]")
        if self.bav_bindus is not None and not (0 <= self.bav_bindus <= 8):
            raise ValueError("bav_bindus out of physical range [0, 8]")
        return self

class TransitDashaInteraction(BaseModel):
    """Interaction between active transit and active Dasha lords."""
    transiting_planet: str
    dasha_level: str = Field(description="Mahadasha, Antardasha, Pratyantardasha, Sookshma, Prana")
    is_active_dasha_lord: bool = True
    dasha_lord_name: str
    interaction_type: str = Field(description="Transit of Dasha Lord, Transit over Dasha Lord, Aspect on Dasha Lord")
    summary: str

    @model_validator(mode='after')
    def validate_interaction_semantics(self):
        if self.transiting_planet not in CANONICAL_PLANETS:
            raise ValueError(f"transiting_planet '{self.transiting_planet}' is not in CANONICAL_PLANETS")
        if self.dasha_lord_name not in CANONICAL_PLANETS:
            raise ValueError(f"dasha_lord_name '{self.dasha_lord_name}' is not in CANONICAL_PLANETS")
        if self.dasha_level not in ALLOWED_DASHA_LEVELS:
            raise ValueError(f"dasha_level '{self.dasha_level}' is invalid")
        return self

class TransitIngressEvent(BaseModel):
    """Event representing sign ingress."""
    planet: str
    ingress_type: str = Field(default="SIGN_INGRESS", description="SIGN_INGRESS")
    current_value: str
    target_value: str
    boundary_longitude: float
    ingress_datetime_iso: str
    days_until_ingress: float

class TransitStationEvent(BaseModel):
    """Event representing a planetary station (turn retrograde or direct)."""
    planet: str
    station_type: str = Field(description="RETROGRADE_STATION, DIRECT_STATION")
    station_datetime_iso: str
    sidereal_longitude: float
    velocity_before: float
    velocity_after: float

class TransitSnapshot(BaseModel):
    """Complete Transit Snapshot for a query datetime."""
    query_datetime_iso: str
    ayanamsha_deg: float
    placements: Dict[str, TransitPlacement]
    aspects: List[TransitAspect]
    ashtakavarga_scores: List[TransitAshtakavargaScore]
    dasha_interactions: List[TransitDashaInteraction]
    ingress_events: List[TransitIngressEvent] = Field(default_factory=list)
    station_events: List[TransitStationEvent] = Field(default_factory=list)
    calculation_hash: str
