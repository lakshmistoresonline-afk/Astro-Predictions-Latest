"""
Canonical Data Schema Models for Ashtakavarga and Shadbala Evaluation Engine.
Exposes machine-readable evidence for strength calculations.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class BhinnashtakavargaResult(BaseModel):
    """BAV result for a single planet."""
    planet: str
    bindus: List[int] = Field(description="Bindus for signs 1-12 (Aries-Pisces)")
    total: int = Field(description="Total bindus for the planet across all signs")
    convention: str = "Parashari Canonical Convention"

class SarvashtakavargaResult(BaseModel):
    """SAV result across all 12 signs."""
    bindus: List[int] = Field(description="Aggregated SAV bindus for signs 1-12 (Aries-Pisces)")
    total: int = Field(description="Total SAV bindus across all signs (Canonical = 337)")
    convention: str = "Parashari Canonical Convention"

class AshtakavargaSuiteResult(BaseModel):
    """Complete Output Contract for Ashtakavarga Engine."""
    chart_hash: str
    bav: Dict[str, BhinnashtakavargaResult]
    sav: SarvashtakavargaResult
    calculation_hash: str

class ShadbalaComponent(BaseModel):
    """A specific component of Shadbala (e.g., Sthana, Dig)."""
    name: str
    value_rupas: float
    value_shashtiamsas: float = Field(description="Raw points (1 rupa = 60 shashtiamsas)")
    sub_components: Dict[str, float] = Field(default_factory=dict, description="Granular breakdown of the component in Shashtiamsas")

class PlanetShadbala(BaseModel):
    """Total Shadbala calculation for a single planet."""
    planet: str
    sthana_bala: ShadbalaComponent
    dig_bala: ShadbalaComponent
    kala_bala: ShadbalaComponent
    cheshta_bala: ShadbalaComponent
    naisargika_bala: ShadbalaComponent
    drik_bala: ShadbalaComponent
    total_shashtiamsas: float
    total_rupas: float
    strength_percentage: float = Field(description="Percentage relative to required minimums")

class ShadbalaSuiteResult(BaseModel):
    """Complete Output Contract for Shadbala Engine."""
    chart_hash: str
    planets: Dict[str, PlanetShadbala]
    calculation_hash: str
    convention: str = "Parashari Canonical Convention"
