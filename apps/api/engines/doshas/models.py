"""
Canonical Data Schema Models for Dosha Evaluation Engine.
Exposes machine-readable evidence for satisfied/failed conditions and exception checks.
Section 1..10 Compliance: Canonical field vocabulary with structured evidence contracts and explicit property aliases.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class DoshaConditionEvidence(BaseModel):
    """Evidence for a single condition within a Dosha rule."""
    condition_id: str
    condition_description: str
    status: bool = Field(description="True if condition is satisfied")
    evidence_details: Dict[str, Any] = Field(default_factory=dict)

class DoshaResult(BaseModel):
    """Machine-readable evidence output for a single Dosha rule."""
    rule_id: str
    name: str
    sanskrit_name: Optional[str] = None
    status: str = Field(description="'DETECTED', 'NOT_DETECTED', 'CANCELLED', 'INDETERMINATE'")
    chart: str = "D1"
    conditions: List[DoshaConditionEvidence]
    cancellation_exceptions: List[DoshaConditionEvidence] = Field(default_factory=list)
    participating_planets: List[str]
    participating_houses: List[int]
    convention: str = "Parashari Canonical Convention"
    provenance: str = "Brihat Parasara Hora Sastra"

    @property
    def affected_planets(self) -> List[str]:
        """Backward-compatibility alias for participating_planets."""
        return self.participating_planets

    @property
    def affected_houses(self) -> List[int]:
        """Backward-compatibility alias for participating_houses."""
        return self.participating_houses

    @property
    def cancellation_reasons(self) -> List[str]:
        """Backward-compatibility alias converting structured cancellation_exceptions to string list."""
        return [ce.condition_description for ce in self.cancellation_exceptions]

class DoshaSuiteResult(BaseModel):
    """Complete Output Contract for Dosha Evaluation Engine."""
    chart_hash: str
    detected_doshas: List[DoshaResult]
    all_evaluated_doshas: List[DoshaResult]
    summary_counts: Dict[str, Any]
    rule_set_version: str = "dosha_rules_v1"
