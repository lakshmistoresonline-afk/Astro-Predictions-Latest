"""
Data Models for Predictive Timing Window Engine.
Defines schemas for timing windows, indicator convergence, and domain timing suites.
Section 1 Compliance:
- Unambiguous evidence_status (CONVERGENT, PARTIAL, UNAVAILABLE).
- Nullable end_datetime_iso (zero manufactured 180-day windows!).
- All 5 Vimshottari Dasha hierarchy levels represented accurately.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class TimingWindow(BaseModel):
    """Structured predictive timing window where multiple astrological indicators converge."""
    window_id: str
    domain: str = Field(description="CAREER, FINANCE, MARRIAGE, EDUCATION, PROPERTY, WELLBEING, etc.")
    start_datetime_iso: str
    end_datetime_iso: Optional[str] = Field(default=None, description="None if Dasha sub-period end is unavailable")
    mahadasha_lord: str
    antardasha_lord: Optional[str] = None
    pratyantardasha_lord: Optional[str] = None
    sookshma_lord: Optional[str] = None
    prana_lord: Optional[str] = None
    relevant_planets: List[str] = Field(description="Planets actually active in this timing event")
    relevant_houses: List[int] = Field(description="1-based natal houses affected")
    supporting_vargas: List[str] = Field(description="Configured relevant Varga codes e.g. ['D9', 'D10']")
    supporting_yogas: List[str] = Field(description="Detected domain-relevant Yogas")
    active_transits_summary: str
    ashtakavarga_support: str
    evidence_status: str = Field(description="CONVERGENT, PARTIAL, UNAVAILABLE")
    evidence_strength_class: Optional[str] = Field(default=None, description="HIGH, MODERATE, or None")
    description: str

class TimingSuiteResult(BaseModel):
    """Suite of timing windows for a natal chart."""
    chart_hash: str
    query_datetime_iso: Optional[str] = Field(default=None, description="UTC query datetime ISO string, or None if unavailable")
    evidence_status: str = Field(default="AVAILABLE", description="AVAILABLE or UNAVAILABLE")
    active_mahadasha: str
    active_antardasha: Optional[str] = None
    ruleset_version: str = "2026.1_PARASHARI_CONVERGENCE_V1"
    timing_windows: List[TimingWindow] = Field(default_factory=list)
    calculation_hash: str
