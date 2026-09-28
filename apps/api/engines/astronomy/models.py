"""
Canonical Data Schema Models for Astrovision Astronomy Provider.
Distinguishes Raw Ephemeris Data, Derived Astronomical State, and Sidereal State.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class PlanetPosition(BaseModel):
    """Raw geocentric planetary position and orbital dynamics."""
    geocentric_longitude: float = Field(description="Geocentric ecliptic longitude in degrees [0, 360)")
    geocentric_latitude: float = Field(description="Geocentric ecliptic latitude in degrees")
    distance_au: float = Field(description="Distance from Earth barycenter in Astronomical Units")
    velocity_lon_deg_day: float = Field(description="Longitudinal velocity in degrees per day")
    retrograde: bool = Field(description="True if longitudinal velocity is negative (apparent retrograde motion)")

class RawEphemerisData(BaseModel):
    """Raw geocentric ephemeris state directly from JPL kernel."""
    timestamp_utc: str
    julian_day_tt: float
    time_scale: str = "UTC/TT"
    observer_latitude: float
    observer_longitude: float
    observer_elevation_m: float = 0.0
    ephemeris_identifier: str
    reference_frame: str = "ICRF / J2000"
    bodies: Dict[str, PlanetPosition]

class DerivedAstronomicalState(BaseModel):
    """Derived astronomical angles and coordinate transformations."""
    local_sidereal_time_deg: float = Field(description="Local Sidereal Time in degrees")
    ramc_deg: float = Field(description="Right Ascension of Midheaven in degrees")
    true_obliquity_deg: float = Field(description="True obliquity of ecliptic in degrees")
    mean_obliquity_deg: float = Field(description="Mean obliquity of ecliptic in degrees")
    ascendant_tropical_deg: float = Field(description="Tropical Ascendant longitude in degrees")
    mc_tropical_deg: float = Field(description="Tropical Midheaven (MC) longitude in degrees")

class SiderealState(BaseModel):
    """Deterministic Sidereal conversion layer outputs."""
    ayanamsha_mode: str = "Lahiri"
    ayanamsha_value_deg: float = Field(description="Calculated Ayanamsha in degrees")
    sidereal_longitudes: Dict[str, float] = Field(description="Sidereal planetary longitudes in degrees [0, 360)")
    ascendant_sidereal_deg: float = Field(description="Sidereal Ascendant in degrees")
    mc_sidereal_deg: float = Field(description="Sidereal Midheaven (MC) in degrees")

class EphemerisMetadata(BaseModel):
    """Audit metadata for calculation reproducibility."""
    provider: str
    provider_version: str
    ephemeris_kernel: str
    kernel_checksum: str
    calculation_timestamp_utc: str
    input_timestamp_utc: str
    observer_coordinates: Dict[str, float]
    coordinate_system: str = "Ecliptic Geocentric J2000 / ICRF"
    ayanamsha_mode: str = "Lahiri"
    calculation_hash: str

class CalculationResult(BaseModel):
    """Canonical complete output schema from the astronomy provider."""
    raw_ephemeris: RawEphemerisData
    derived_astronomy: DerivedAstronomicalState
    sidereal_state: SiderealState
    metadata: EphemerisMetadata
