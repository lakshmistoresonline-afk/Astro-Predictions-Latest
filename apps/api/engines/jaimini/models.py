"""
Data Models for Jaimini Engine.
Defines schemas for Chara Karakas, Rashi Aspects, Arudha Lagna, Upapada Lagna, and Karakamsha.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class CharaKarakaInfo(BaseModel):
    """Jaimini 7-Chara Karaka assignment for a planet."""
    karaka_code: str = Field(description="AK, AmK, BK, MK, PK, GK, DK")
    karaka_name: str = Field(description="Atmakaraka, Amatyakaraka, Bhratrukaraka, Matrukaraka, Putrakaraka, Gnatikaraka, Darakaraka")
    planet: str
    degree_in_sign: float = Field(description="Degrees within sign [0.0, 30.0)")

class RashiAspectInfo(BaseModel):
    """Jaimini Rashi Aspect relationship."""
    source_rashi_index: int = Field(description="1-based Rashi index (1=Aries)")
    source_rashi_name: str
    aspected_rashi_indices: List[int]
    aspected_rashi_names: List[str]

class JaiminiSuiteResult(BaseModel):
    """Complete Jaimini Calculation Result."""
    chart_hash: str
    chara_karakas: Dict[str, CharaKarakaInfo] = Field(description="Map from karaka code e.g. 'AK' to info")
    arudha_lagna_rashi_index: int
    arudha_lagna_rashi_name: str
    upapada_lagna_rashi_index: int
    upapada_lagna_rashi_name: str
    atmakaraka_planet: str
    karakamsha_rashi_index: int = Field(description="D9 sign of Atmakaraka")
    karakamsha_rashi_name: str
    rashi_aspects: List[RashiAspectInfo]
    calculation_hash: str
