"""
Canonical Data Schema Models for Yoga Evaluation Engine.
Exposes machine-readable evidence for satisfied/failed conditions and exception checks.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class RuleConditionEvidence(BaseModel):
    """Evidence for a single condition within a Yoga or Dosha rule."""
    condition_id: str
    condition_description: str
    status: bool = Field(description="True if condition is satisfied")
    evidence_details: Dict[str, Any] = Field(default_factory=dict)

class YogaResult(BaseModel):
    """Machine-readable evidence output for a single Yoga rule."""
    rule_id: str
    name: str
    sanskrit_name: Optional[str] = None
    category: str = Field(description="'Mahapurusha', 'Raja', 'Dhana', 'Chandra', 'Surya', 'Viparita', 'Parivartana', 'NeechaBhanga', 'Auspicious'")
    status: str = Field(description="'DETECTED', 'NOT_DETECTED', 'INDETERMINATE'")
    chart: str = "D1"
    conditions: List[RuleConditionEvidence]
    exceptions_checked: List[RuleConditionEvidence] = Field(default_factory=list)
    participating_planets: List[str]
    participating_houses: List[int]
    convention: str = "Parashari Canonical Convention"
    provenance: str = "Brihat Parasara Hora Sastra"

class YogaSuiteResult(BaseModel):
    """Complete Output Contract for Yoga Evaluation Engine."""
    chart_hash: str
    detected_yogas: List[YogaResult]
    all_evaluated_yogas: List[YogaResult]
    summary_counts: Dict[str, int]
    rule_set_version: str = "yoga_rules_v1"
