"""
Authoritative Varga Evidence Adapter for Astrovision (Phase 2E-R4.1-R12-R10).
Extracts structured interpretation evidence from the 16-Varga Suite (D1 through D60).
Explicitly maps each Varga to its canonical Parashari domain.
Section 1..12 Compliance:
- Uses exact VargaPlacement schema properties and centralized rashi dignity rules.
- Explicit evidence_status (AVAILABLE / UNAVAILABLE) for every declared Varga division.
"""
from typing import Dict, List, Any
from pydantic import BaseModel, Field

from apps.api.engines.varga.models import Full16VargaSuite, VargaChart
from apps.api.engines.vedic.rashi import RASHI_LORDS, EXALTATION_SIGNS, DEBILITATION_SIGNS

VARGA_DOMAIN_MAP = {
    "D1": ("Physical Body & General Life Path", "Overview of physical constitution, Lagna strength, and life purpose."),
    "D2": ("Wealth & Financial Resources", "Governs accumulated wealth, family assets, and financial sustenance."),
    "D3": ("Siblings & Personal Initiative", "Governs siblings, courage, personal enterprise, and short travels."),
    "D4": ("Property & Real Estate", "Governs fixed assets, landed property, real estate, and home stability."),
    "D7": ("Progeny & Children", "Governs children, creative expression, and lineage continuity."),
    "D9": ("Marriage, Spouse & Dharma", "Governs marital harmony, spouse characteristics, dharma, and soul destiny."),
    "D10": ("Career, Profession & Commerce", "Governs profession, executive power, public authority, and career achievements."),
    "D12": ("Parents & Heritage", "Governs parents, ancestral background, and family lineage."),
    "D16": ("Vehicles, Comforts & Luxuries", "Governs conveyances, material comforts, vehicles, and general happiness."),
    "D20": ("Spirituality & Sadhana", "Governs spiritual evolution, religious practices, devotion, and inner growth."),
    "D24": ("Higher Education & Knowledge", "Governs academic achievements, learning, wisdom, and intellectual skill."),
    "D27": ("Strengths & Physical Endurance", "Governs physical stamina, intrinsic strengths, and vital endurance."),
    "D30": ("Difficulties & Enmities", "Governs health obstacles, hidden enmities, difficulties, and hazards."),
    "D40": ("Maternal Lineage & Auspicious Effects", "Governs maternal lineage, auspicious family inheritance, and grace."),
    "D45": ("Character & Paternal Lineage", "Governs moral character, ancestral ethical standing, and paternal lineage."),
    "D60": ("Deep Karmic Root & Traditional Legacy", "Governs deep karmic impressions, past-life samskaras, and Parashari root.")
}

class VargaDomainEvidence(BaseModel):
    """Structured evidence for a specific Varga divisional chart."""
    varga_code: str
    domain_title: str
    domain_description: str
    evidence_status: str = Field(default="AVAILABLE", description="AVAILABLE or UNAVAILABLE")
    lagna_rashi_name: str
    lagna_lord_planet: str
    key_placements: Dict[str, str] = Field(description="Map planet name to sign name in this Varga")
    exalted_planets: List[str]
    debilitated_planets: List[str]
    vargottama_planets: List[str] = Field(default_factory=list, description="Planets with is_vargottama == True")
    summary_evidence: str

class VargaSuiteEvidence(BaseModel):
    """Complete Varga evidence package across all 16 divisional charts."""
    varga_evidences: Dict[str, VargaDomainEvidence]
    calculation_hash: str

class VargaEvidenceAdapter:
    """
    Adapter transforming Full16VargaSuite into structured domain-specific evidence.
    """

    @classmethod
    def extract_evidence_suite(cls, varga_suite: Full16VargaSuite) -> VargaSuiteEvidence:
        evidences: Dict[str, VargaDomainEvidence] = {}

        v_dict = varga_suite.vargas # Map 'D1', 'D2', ..., 'D60' -> VargaChart

        for v_code, (title, desc) in VARGA_DOMAIN_MAP.items():
            if v_code in v_dict and v_dict[v_code] is not None:
                v_chart: VargaChart = v_dict[v_code]
                lagna_rashi = v_chart.ascendant.varga_sign
                lagna_sign_idx = v_chart.ascendant.varga_sign_index
                lagna_lord = RASHI_LORDS[lagna_sign_idx]

                placements_map: Dict[str, str] = {}
                exalted: List[str] = []
                debilitated: List[str] = []
                vargottama_list: List[str] = []

                for p_name, p_place in v_chart.placements.items():
                    placements_map[p_name] = p_place.varga_sign
                    p_sign_idx = p_place.varga_sign_index

                    if EXALTATION_SIGNS.get(p_name) == p_sign_idx:
                        exalted.append(p_name)
                    elif DEBILITATION_SIGNS.get(p_name) == p_sign_idx:
                        debilitated.append(p_name)

                    if p_place.is_vargottama:
                        vargottama_list.append(p_name)

                ex_str = f" Exalted: {', '.join(exalted)}." if exalted else ""
                deb_str = f" Debilitated: {', '.join(debilitated)}." if debilitated else ""
                varg_str = f" Vargottama: {', '.join(vargottama_list)}." if vargottama_list else ""

                summary = (
                    f"{v_code} ({title}) Lagna in {lagna_rashi} (Lord: {lagna_lord})."
                    f"{ex_str}{deb_str}{varg_str}"
                )

                evidences[v_code] = VargaDomainEvidence(
                    varga_code=v_code,
                    domain_title=title,
                    domain_description=desc,
                    evidence_status="AVAILABLE",
                    lagna_rashi_name=lagna_rashi,
                    lagna_lord_planet=lagna_lord,
                    key_placements=placements_map,
                    exalted_planets=exalted,
                    debilitated_planets=debilitated,
                    vargottama_planets=vargottama_list,
                    summary_evidence=summary
                )
            else:
                evidences[v_code] = VargaDomainEvidence(
                    varga_code=v_code,
                    domain_title=title,
                    domain_description=desc,
                    evidence_status="UNAVAILABLE",
                    lagna_rashi_name="UNAVAILABLE",
                    lagna_lord_planet="UNAVAILABLE",
                    key_placements={},
                    exalted_planets=[],
                    debilitated_planets=[],
                    vargottama_planets=[],
                    summary_evidence=f"{v_code} ({title}) evidence unavailable."
                )

        return VargaSuiteEvidence(
            varga_evidences=evidences,
            calculation_hash=varga_suite.calculation_hash
        )
