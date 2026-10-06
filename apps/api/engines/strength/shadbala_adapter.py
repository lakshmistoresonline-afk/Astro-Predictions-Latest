"""
Authoritative Shadbala Evidence Adapter for Astrovision (Phase 2E-R4.1-R12-R10).
Extracts structured interpretation evidence from ShadbalaSuiteResult.
Maps planetary strengths (Sthana, Dig, Kala, Cheshta, Naisargika, Drik Bala, Rupas) to prediction domains.
Section 1..12 Compliance:
- Unified canonical strength classification vocabulary (HIGH, MODERATE, LOW, UNAVAILABLE).
- Preserves detailed BPHS strength tier (EXCEPTIONAL, STRONG, ADEQUATE, MODERATE, CRITICAL) in detailed_strength_category.
- Preserves BPHS minimum strength status (is_sufficient_strength) separately.
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from apps.api.engines.strength.models import (
    ShadbalaSuiteResult,
    PlanetShadbala,
    StrengthClass,
    DetailedStrengthTier
)

# Mapping from prediction domain to primary karaka/lord planets
DOMAIN_SHADBALA_MAP = {
    "CAREER": (["Sun", "Saturn", "Jupiter", "Mercury"], "10th House / Authority / Discipline"),
    "FINANCE": (["Jupiter", "Venus", "Mercury"], "2nd & 11th House / Wealth / Gains"),
    "BUSINESS": (["Mercury", "Mars", "Venus"], "7th & 10th House / Commerce / Enterprise"),
    "MARRIAGE": (["Venus", "Jupiter"], "7th House / Relationship Harmony"),
    "RELATIONSHIP": (["Venus", "Moon"], "5th & 7th House / Emotional Affinity"),
    "EDUCATION": (["Mercury", "Jupiter"], "4th & 5th House / Intellect / Learning"),
    "FAMILY": (["Moon", "Jupiter"], "2nd & 4th House / Domestic Peace"),
    "CHILDREN": (["Jupiter", "Mars"], "5th House / Progeny / Legacy"),
    "PROPERTY": (["Mars", "Saturn"], "4th House / Land / Real Estate"),
    "TRAVEL": (["Moon", "Rahu", "Jupiter"], "9th & 12th House / Foreign Journeys"),
    "RELOCATION": (["Moon", "Saturn"], "4th & 12th House / Shift of Residence"),
    "SPIRITUALITY": (["Jupiter", "Ketu", "Sun"], "9th & 12th House / Higher Dharma"),
    "PERSONAL_DEVELOPMENT": (["Sun", "Moon", "Mars"], "Lagna / Soul Vitality / Willpower"),
    "WELLBEING": (["Sun", "Moon", "Mars"], "Lagna / Immunity / Vitality")
}

class PlanetStrengthEvidence(BaseModel):
    """Structured strength evidence for a single planet."""
    planet: str
    total_shashtiamsas: float
    total_rupas: float
    is_sufficient_strength: bool = Field(description="Meets BPHS minimum required Rupas benchmark")
    relative_rank: int = Field(description="1-based rank among 7 planets (1=Strongest)")
    strongest_component: str
    weakest_component: str
    summary_evidence: str

class DomainStrengthEvidence(BaseModel):
    """Strength evidence relevant to a specific prediction domain."""
    domain: str
    domain_focus: str
    relevant_planets: List[str]
    average_domain_rupas: float
    domain_strength_class: str = Field(description="Canonical strength class: HIGH, MODERATE, LOW, or UNAVAILABLE")
    detailed_strength_category: Optional[str] = Field(default=None, description="Detailed BPHS tier: EXCEPTIONAL, STRONG, ADEQUATE, MODERATE, CRITICAL")
    summary: str

class ShadbalaEvidencePackage(BaseModel):
    """Complete Shadbala interpretation evidence package."""
    planet_strengths: Dict[str, PlanetStrengthEvidence]
    domain_strengths: Dict[str, DomainStrengthEvidence]
    strongest_planet: str
    weakest_planet: str
    calculation_hash: str

class ShadbalaEvidenceAdapter:
    """
    Adapter transforming ShadbalaSuiteResult into domain-specific prediction evidence.
    """

    # BPHS Minimum Required Rupas by Planet
    BPHS_REQUIRED_RUPAS = {
        "Sun": 6.5,
        "Moon": 6.0,
        "Mars": 5.0,
        "Mercury": 7.0,
        "Jupiter": 6.5,
        "Venus": 5.5,
        "Saturn": 5.0
    }

    @classmethod
    def extract_evidence(cls, shadbala_suite: ShadbalaSuiteResult) -> ShadbalaEvidencePackage:
        planet_evidence_map: Dict[str, PlanetStrengthEvidence] = {}

        # 1. Rank planets by total Rupas
        planets_sorted = sorted(
            shadbala_suite.planets.values(),
            key=lambda p: p.total_rupas,
            reverse=True
        )

        rank_map = {p.planet: idx + 1 for idx, p in enumerate(planets_sorted)}

        strongest_p = planets_sorted[0].planet if planets_sorted else "Sun"
        weakest_p = planets_sorted[-1].planet if planets_sorted else "Saturn"

        for p_data in shadbala_suite.planets.values():
            p_name = p_data.planet
            rupas = p_data.total_rupas
            shashti = p_data.total_shashtiamsas

            req_rupas = cls.BPHS_REQUIRED_RUPAS.get(p_name, 6.0)
            is_sufficient = rupas >= req_rupas

            comps = {
                "Sthana Bala": p_data.sthana_bala.value_shashtiamsas,
                "Dig Bala": p_data.dig_bala.value_shashtiamsas,
                "Kala Bala": p_data.kala_bala.value_shashtiamsas,
                "Cheshta Bala": p_data.cheshta_bala.value_shashtiamsas,
                "Naisargika Bala": p_data.naisargika_bala.value_shashtiamsas,
                "Drik Bala": p_data.drik_bala.value_shashtiamsas
            }

            best_comp = max(comps.items(), key=lambda x: x[1])[0]
            worst_comp = min(comps.items(), key=lambda x: x[1])[0]

            summary = (
                f"{p_name} has total Shadbala of {rupas:.2f} Rupas ({shashti:.1f} Shashtiamsas) "
                f"[Rank #{rank_map[p_name]}]. BPHS Minimum ({req_rupas} Rupas) met: {is_sufficient}. "
                f"Strongest component: {best_comp} ({comps[best_comp]:.1f} pts)."
            )

            planet_evidence_map[p_name] = PlanetStrengthEvidence(
                planet=p_name,
                total_shashtiamsas=round(shashti, 2),
                total_rupas=round(rupas, 2),
                is_sufficient_strength=is_sufficient,
                relative_rank=rank_map[p_name],
                strongest_component=best_comp,
                weakest_component=worst_comp,
                summary_evidence=summary
            )

        # 2. Compute Domain Strengths using unified HIGH | MODERATE | LOW | UNAVAILABLE vocabulary
        domain_evidence_map: Dict[str, DomainStrengthEvidence] = {}
        for dom_code, (rel_planets, dom_focus) in DOMAIN_SHADBALA_MAP.items():
            valid_p = [p for p in rel_planets if p in planet_evidence_map]
            if valid_p:
                avg_rupas = sum(planet_evidence_map[p].total_rupas for p in valid_p) / len(valid_p)
                if avg_rupas >= 7.5:
                    s_class = StrengthClass.HIGH
                    sub_tier = DetailedStrengthTier.EXCEPTIONAL
                elif avg_rupas >= 6.5:
                    s_class = StrengthClass.HIGH
                    sub_tier = DetailedStrengthTier.STRONG
                elif avg_rupas >= 5.5:
                    s_class = StrengthClass.MODERATE
                    sub_tier = DetailedStrengthTier.ADEQUATE
                elif avg_rupas >= 4.5:
                    s_class = StrengthClass.MODERATE
                    sub_tier = DetailedStrengthTier.MODERATE
                else:
                    s_class = StrengthClass.LOW
                    sub_tier = DetailedStrengthTier.CRITICAL
            else:
                avg_rupas = 0.0
                s_class = StrengthClass.UNAVAILABLE
                sub_tier = DetailedStrengthTier.UNAVAILABLE

            summary = f"Domain {dom_code} supported by {', '.join(valid_p)} with average Shadbala of {avg_rupas:.2f} Rupas ({s_class} / {sub_tier})."

            domain_evidence_map[dom_code] = DomainStrengthEvidence(
                domain=dom_code,
                domain_focus=dom_focus,
                relevant_planets=valid_p,
                average_domain_rupas=round(avg_rupas, 2),
                domain_strength_class=s_class,
                detailed_strength_category=sub_tier,
                summary=summary
            )

        return ShadbalaEvidencePackage(
            planet_strengths=planet_evidence_map,
            domain_strengths=domain_evidence_map,
            strongest_planet=strongest_p,
            weakest_planet=weakest_p,
            calculation_hash=shadbala_suite.calculation_hash
        )
