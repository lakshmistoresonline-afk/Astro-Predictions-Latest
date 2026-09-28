"""
Data Models for Astrovision 16-Varga Divisional Engine.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from apps.api.engines.vedic.models import RashiPosition

class VargaPlacement(BaseModel):
    """Varga placement for a single celestial body or point."""
    body_name: str
    d1_sidereal_longitude: float = Field(description="Full precision canonical sidereal longitude in [0, 360)")
    varga_sign: str = Field(description="Rashi sign in divisional chart")
    varga_sign_index: int = Field(description="1-based sign index in divisional chart [1, 12]")
    varga_division_index: int = Field(description="1-based division index within sign [1, N]")
    varga_degree_in_sign: float = Field(description="Effective degree within Divisional sign [0.0, 30.0)")
    is_vargottama: bool = Field(default=False, description="True if D1 sign matches D9 sign")

class VargaChart(BaseModel):
    """Complete Divisional Chart for a specific division (e.g., D9, D10)."""
    division: str = Field(description="Division identifier (e.g. 'D1', 'D9', 'D60')")
    division_number: int = Field(description="Division number N (e.g., 9 for D9)")
    division_name: str = Field(description="Traditional name (e.g., 'Navamsa')")
    ascendant: VargaPlacement
    placements: Dict[str, VargaPlacement]
    convention: str = Field(description="Canonical rule provenance convention identifier")
    source: str = Field(description="Traditional literature reference")
    calculation_hash: str = Field(description="Input chart calculation hash")

class Full16VargaSuite(BaseModel):
    """Container for all 16 Parashari Divisional Charts."""
    chart_hash: str
    vargas: Dict[str, VargaChart]
    vargottama_bodies: List[str] = Field(description="List of bodies whose D9 sign equals their D1 sign")
