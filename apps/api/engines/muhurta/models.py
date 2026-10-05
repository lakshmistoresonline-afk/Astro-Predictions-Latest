"""
Data Models for Muhurta Foundation Engine.
Defines schemas for factor-based activity suitability evaluations, timing exclusions, and recommendations.
Section 1 Compliance: Transparent factor classification models without arbitrary scoring arithmetic.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class ActivityRuleResult(BaseModel):
    """Evaluation of a specific Panchanga factor for an activity."""
    rule_id: str = Field(description="MUHURTA_RULE_TITHI, MUHURTA_RULE_NAKSHATRA, etc.")
    factor_name: str = Field(description="Tithi, Nakshatra, Nitya Yoga, Karana, Rahu Kalam, Abhijit Muhurta")
    rule_category: str = Field(description="HARD_EXCLUSION, FAVORABLE_FACTOR, UNFAVORABLE_FACTOR, NEUTRAL_FACTOR")
    status: str = Field(description="FAVORABLE, NEUTRAL, UNFAVORABLE, EXCLUDED")
    is_hard_exclusion: bool = False
    description: str

class MuhurtaEvaluation(BaseModel):
    """Muhurta suitability result for a specific activity derived from deterministic rule outcomes."""
    activity_name: str = Field(description="TRAVEL, MARRIAGE, BUSINESS, EDUCATION, PROPERTY, SPIRITUALITY")
    datetime_iso: str = Field(default="", description="ISO datetime of evaluated Panchanga instant")
    recommendation: str = Field(description="EXCLUDED, RECOMMENDED, FAVORABLE_WITH_CAUTION, NOT_RECOMMENDED")
    overall_suitability_score: Optional[float] = Field(default=None, description="Nullable rule suitability score (None when unweighted)")
    is_rahu_kalam_active: bool = False
    is_abhijit_active: bool = False
    has_hard_exclusion: bool = False
    favorable_factor_count: int = 0
    unfavorable_factor_count: int = 0
    evaluated_factors: List[ActivityRuleResult]
    summary: str = Field(default="", description="Rule-based human-readable explanation")
    calculation_hash: str

class MuhurtaSuiteResult(BaseModel):
    """Suite of Muhurta evaluations across activities."""
    panchanga_hash: str
    datetime_iso: str = Field(default="", description="ISO datetime of evaluated Panchanga instant")
    evaluations: Dict[str, MuhurtaEvaluation]
    calculation_hash: str
