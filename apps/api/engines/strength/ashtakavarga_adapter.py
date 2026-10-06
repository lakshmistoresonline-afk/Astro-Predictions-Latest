"""
Authoritative Ashtakavarga Evidence Adapter for Astrovision (Phase 2E-R4.1-R12-R10).
Extracts structured interpretation evidence from AshtakavargaSuiteResult (BAV & SAV).
Evaluates house SAV strengths, transit scoring through high vs low bindu houses, and Dasha-Ashtakavarga interactions.
SAV total must ALWAYS be derived dynamically from BAV.
Section 1..12 Compliance:
- HouseSAVEvidence sav_bindus is Optional[int] allowing explicit None state when evidence is unavailable.
- Zero hardcoded SAV total descriptions (dynamic BAV total calculation preserved).
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from apps.api.engines.strength.models import AshtakavargaSuiteResult, AshtakavargaCategory

RASHI_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

class HouseSAVEvidence(BaseModel):
    """SAV strength evidence for a single house / sign."""
    rashi_index: int = Field(description="1-based Rashi index (1=Aries)")
    rashi_name: str
    sav_bindus: Optional[int] = Field(default=None, description="SAV bindus in this sign [0-56], or None if evidence is unavailable")
    strength_category: str = Field(description="HIGHLY_FAVORABLE (>=30), FAVORABLE (>=28), AVERAGE (>=25), LOW (<25), or UNAVAILABLE")
    transit_recommendation: str

class AshtakavargaPredictiveEvidence(BaseModel):
    """Complete Ashtakavarga predictive evidence package."""
    house_sav_evidences: List[HouseSAVEvidence]
    total_sav_bindus: Optional[int] = Field(default=None, description="Observed total SAV bindus derived dynamically from BAV, or None if unavailable")
    strongest_house_rashi: Optional[str] = Field(default=None, description="Strongest SAV house, or None if unavailable")
    weakest_house_rashi: Optional[str] = Field(default=None, description="Weakest SAV house, or None if unavailable")
    worst_house_rashi: Optional[str] = Field(default=None, description="Backward-compatibility alias for weakest_house_rashi")
    summary_evidence: str
    calculation_hash: str

class AshtakavargaEvidenceAdapter:
    """
    Adapter transforming AshtakavargaSuiteResult into predictive evidence.
    """

    @classmethod
    def extract_evidence(cls, ashtakavarga_suite: AshtakavargaSuiteResult) -> AshtakavargaPredictiveEvidence:
        sav_bindus_list = ashtakavarga_suite.sav.bindus # List of 12 integers for signs 1-12
        obs_total = ashtakavarga_suite.sav.total

        house_evidences: List[HouseSAVEvidence] = []
        best_r_idx = 1
        max_b = -1
        worst_r_idx = 1
        min_b = 999

        for r_idx_0 in range(12):
            r_idx_1 = r_idx_0 + 1
            r_name = RASHI_NAMES[r_idx_0]
            b_val = sav_bindus_list[r_idx_0]

            if b_val > max_b:
                max_b = b_val
                best_r_idx = r_idx_1
            if b_val < min_b:
                min_b = b_val
                worst_r_idx = r_idx_1

            if b_val >= 30:
                s_cat = AshtakavargaCategory.HIGHLY_FAVORABLE
                t_rec = "Transits through this house yield robust, tangible success, wealth gains, and smooth execution."
            elif b_val >= 28:
                s_cat = AshtakavargaCategory.FAVORABLE
                t_rec = "Transits through this house yield steady, positive outcomes and constructive progress."
            elif b_val >= 25:
                s_cat = AshtakavargaCategory.AVERAGE
                t_rec = "Transits through this house yield mixed, moderate outcomes requiring consistent effort."
            else:
                s_cat = AshtakavargaCategory.LOW
                t_rec = "Transits through this house require heightened caution, patience, and risk mitigation."

            house_evidences.append(HouseSAVEvidence(
                rashi_index=r_idx_1,
                rashi_name=r_name,
                sav_bindus=b_val,
                strength_category=s_cat,
                transit_recommendation=t_rec
            ))

        best_rashi = RASHI_NAMES[best_r_idx - 1]
        worst_rashi = RASHI_NAMES[worst_r_idx - 1]

        summary = (
            f"Observed SAV Total derived dynamically from BAV: {obs_total} bindus. "
            f"Strongest SAV House: {best_rashi} ({max_b} bindus). "
            f"Weakest SAV House: {worst_rashi} ({min_b} bindus)."
        )

        return AshtakavargaPredictiveEvidence(
            house_sav_evidences=house_evidences,
            total_sav_bindus=obs_total,
            strongest_house_rashi=best_rashi,
            worst_house_rashi=worst_rashi,
            weakest_house_rashi=worst_rashi,
            summary_evidence=summary,
            calculation_hash=ashtakavarga_suite.calculation_hash
        )
