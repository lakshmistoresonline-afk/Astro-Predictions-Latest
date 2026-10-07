"""
Authoritative Prediction Evidence Engine for Astrovision (Phase 2E-R4.1-R12-R10).
Sections 1, 2, 3, 4, 5, 6, 7, 8, 14, 15 & 16 Compliance:
- Structured domain transit aspect matching using target_type, target_planet, target_house (zero target_name substring searches!).
- Explicit three-state transit evidence summaries (AVAILABLE_WITH_CONTACTS | AVAILABLE_NO_CONTACTS | UNAVAILABLE).
- Strict evidence availability check (`has_live_sav = any(e.sav_bindus is not None for e in sav_house_evs)`).
- Explicit evidence_status (AVAILABLE | UNAVAILABLE) and evidence_strength_class (HIGH | MODERATE | None).
- Zero "PROVISIONAL" or "EXCEPTIONAL" strength class fallbacks.
- Ashtakavarga SAV evidence: sav_bindus = None (never 0 or 28!) when unavailable.
- Domain-scoped Yoga, Dosha, Transit, and Jaimini evidence.
- Strict fail-closed domain rule configuration lookup (`DOMAIN_RULES_CONFIG[dom]`). Zero default fallbacks!
- Prediction calculation hash calculated from complete serialized prediction evidence.
"""
import hashlib
import json
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from apps.api.engines.canonical_evidence import CanonicalAstrologyEvidence
from apps.api.engines.varga.evidence_adapter import VargaDomainEvidence
from apps.api.engines.strength.shadbala_adapter import DomainStrengthEvidence
from apps.api.engines.strength.ashtakavarga_adapter import HouseSAVEvidence
from apps.api.engines.jaimini.models import CharaKarakaInfo
from apps.api.engines.timing.models import TimingWindow

DOMAIN_RULESET_VERSION = "2026.1_PARASHARI_D10_D9_D2_D4_D7_D24_D20_D12_D1_V1"

RASHI_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

DOMAIN_RULES_CONFIG = {
    "CAREER": {
        "title": "Career, Profession & Executive Authority",
        "houses": [10, 1, 6, 11],
        "karakas": ["Sun", "Saturn", "Jupiter", "Mercury"],
        "varga": "D10",
        "description": "10th House (Karma), 1st House (Lagna), 6th House (Service), 11th House (Gains)"
    },
    "FINANCE": {
        "title": "Wealth, Accumulated Assets & Financial Gains",
        "houses": [2, 11, 5, 9],
        "karakas": ["Jupiter", "Venus", "Mercury"],
        "varga": "D2",
        "description": "2nd House (Dhana/Wealth), 11th House (Labha/Gains), 5th/9th Trikonas"
    },
    "BUSINESS": {
        "title": "Commerce, Partnerships & Enterprise",
        "houses": [7, 10, 11],
        "karakas": ["Mercury", "Mars", "Venus"],
        "varga": "D10",
        "description": "7th House (Partnerships/Trade), 10th House (Commerce), 11th House (Gains)"
    },
    "MARRIAGE": {
        "title": "Marriage, Life Partner & Marital Dharma",
        "houses": [7, 2, 5, 11],
        "karakas": ["Venus", "Jupiter"],
        "varga": "D9",
        "description": "7th House (Kalatra/Spouse), 2nd House (Family), 5th House (Romance), 11th House (Fulfillment)"
    },
    "RELATIONSHIP": {
        "title": "Interpersonal Binds & Romantic Harmony",
        "houses": [5, 7],
        "karakas": ["Venus", "Moon"],
        "varga": "D9",
        "description": "5th House (Romance/Affection), 7th House (Partnership)"
    },
    "EDUCATION": {
        "title": "Higher Intellect, Schooling & Learning",
        "houses": [4, 5, 9],
        "karakas": ["Mercury", "Jupiter"],
        "varga": "D24",
        "description": "4th House (Schooling), 5th House (Intellect), 9th House (Higher Knowledge)"
    },
    "FAMILY": {
        "title": "Domestic Harmony & Extended Family",
        "houses": [2, 4],
        "karakas": ["Moon", "Jupiter"],
        "varga": "D12",
        "description": "2nd House (Immediate Family), 4th House (Domestic Happiness)"
    },
    "CHILDREN": {
        "title": "Progeny, Offspring & Creative Lineage",
        "houses": [5, 9, 2],
        "karakas": ["Jupiter", "Mars"],
        "varga": "D7",
        "description": "5th House (Putra/Progeny), 9th House (Legacy), 2nd House (Family expansion)"
    },
    "PROPERTY": {
        "title": "Real Estate, Fixed Assets & Vehicles",
        "houses": [4, 11],
        "karakas": ["Mars", "Saturn"],
        "varga": "D4",
        "description": "4th House (Real Estate/Vehicles), 11th House (Asset Gains)"
    },
    "TRAVEL": {
        "title": "Long Journeys, Pilgrimages & Foreign Travel",
        "houses": [9, 12, 7],
        "karakas": ["Moon", "Rahu", "Jupiter"],
        "varga": "D1",
        "description": "9th House (Pilgrimage/Long Journeys), 12th House (Foreign Lands), 7th House (Travel Commerce)"
    },
    "RELOCATION": {
        "title": "Change of Domicile & Geographical Shift",
        "houses": [4, 12, 9],
        "karakas": ["Moon", "Saturn"],
        "varga": "D4",
        "description": "4th House (Residence Change), 12th House (Foreign Domicile), 9th House (Distance)"
    },
    "SPIRITUALITY": {
        "title": "Spiritual Growth, Sadhana & Liberation",
        "houses": [9, 12, 5],
        "karakas": ["Ketu", "Jupiter", "Sun"],
        "varga": "D20",
        "description": "9th House (Dharma), 12th House (Moksha/Liberation), 5th House (Sadhana/Mantra)"
    },
    "PERSONAL_DEVELOPMENT": {
        "title": "Self-Actualization, Charisma & Vitality",
        "houses": [1, 5, 9],
        "karakas": ["Sun", "Moon", "Mars"],
        "varga": "D1",
        "description": "1st House (Lagna/Self-Vitality), 5th House (Genius), 9th House (Higher Path)"
    },
    "WELLBEING": {
        "title": "Physical Immunity, Health & Longevity",
        "houses": [1, 6, 8],
        "karakas": ["Sun", "Moon", "Mars"],
        "varga": "D1",
        "description": "1st House (Vitality/Lagna), 6th House (Immunity/Disease), 8th House (Longevity)"
    }
}

class DomainRuleDefinition(BaseModel):
    """Immutable rule metadata defining what the methodology inspects for a domain."""
    domain_code: str
    domain_title: str
    rule_set_version: str = DOMAIN_RULESET_VERSION
    primary_karakas: List[str]
    relevant_houses: List[int]
    varga_code: str
    rule_description: str

class ObservedChartEvidence(BaseModel):
    """Actual observed chart facts for a domain (Strictly factual)."""
    varga_evidence: Optional[VargaDomainEvidence] = None
    detected_yogas: List[str] = Field(default_factory=list, description="Section 3: Domain-scoped Yogas")
    detected_doshas: List[str] = Field(default_factory=list, description="Section 3: Domain-scoped Doshas")
    active_dasha_summary: Optional[str] = Field(default=None, description="Section 7: 5-Level active Dasha hierarchy summary")
    active_transits_summary: Optional[str] = None
    shadbala_domain_evidence: Optional[DomainStrengthEvidence] = None
    ashtakavarga_house_evidences: List[HouseSAVEvidence] = Field(default_factory=list, description="Section 5: SAV evidence for ALL domain houses")
    jaimini_atmakaraka_info: Optional[CharaKarakaInfo] = Field(default=None, description="Section 8: Structured Jaimini AK Info")
    jaimini_amatyakaraka_info: Optional[CharaKarakaInfo] = Field(default=None, description="Section 8: Structured Jaimini AmK Info")
    jaimini_darakaraka_info: Optional[CharaKarakaInfo] = Field(default=None, description="Section 8: Structured Jaimini DK Info")
    timing_windows: List[TimingWindow] = Field(default_factory=list)

class DomainPredictionEvidence(BaseModel):
    """Structured deterministic evidence package for a single prediction domain."""
    rule_definition: DomainRuleDefinition
    observed_evidence: ObservedChartEvidence
    evidence_status: str = Field(description="AVAILABLE or UNAVAILABLE")
    evidence_strength_class: Optional[str] = Field(default=None, description="HIGH, MODERATE, or None")
    traditional_metadata: Dict[str, str]

class ComprehensivePredictionPackage(BaseModel):
    """Complete prediction package containing evidence for all 14 domains."""
    master_evidence_hash: str
    ruleset_version: str = DOMAIN_RULESET_VERSION
    domain_predictions: Dict[str, DomainPredictionEvidence]
    active_dasha_summary: Optional[str] = Field(default=None, description="None if query_dt was not provided")
    strongest_prediction_domain: Optional[str] = Field(default=None, description="None if deterministic ranking is not supported")
    calculation_hash: str

class PredictionEngine:
    """
    Authoritative Prediction Evidence Engine.
    Combines all local deterministic engine evidence into 14 domain packages.
    """

    DOMAINS = [
        "CAREER", "FINANCE", "BUSINESS", "MARRIAGE", "RELATIONSHIP",
        "EDUCATION", "FAMILY", "CHILDREN", "PROPERTY", "TRAVEL",
        "RELOCATION", "SPIRITUALITY", "PERSONAL_DEVELOPMENT", "WELLBEING"
    ]

    @classmethod
    def generate_all_predictions(cls, master_evidence: CanonicalAstrologyEvidence) -> ComprehensivePredictionPackage:
        domain_results: Dict[str, DomainPredictionEvidence] = {}

        # Section 7 Compliance: Complete 5-level Dasha hierarchy summary (None if query_dt not supplied)
        dasha_summary = None
        if master_evidence.active_dasha_hierarchy:
            active_h = master_evidence.active_dasha_hierarchy
            md = active_h.mahadasha.lord_planet
            ad = active_h.antardasha.lord_planet if active_h.antardasha else "None"
            pd = active_h.pratyantardasha.lord_planet if active_h.pratyantardasha else "None"
            sd = active_h.sookshma.lord_planet if active_h.sookshma else "None"
            pr = active_h.prana.lord_planet if active_h.prana else "None"
            dasha_summary = f"MD: {md}, AD: {ad}, PD: {pd}, SD: {sd}, Prana: {pr}"

        lagna_r_idx = master_evidence.canonical_chart.ascendant.sign_index

        for dom in cls.DOMAINS:
            if dom not in DOMAIN_RULES_CONFIG:
                raise KeyError(f"Domain configuration for '{dom}' missing from DOMAIN_RULES_CONFIG.")

            cfg = DOMAIN_RULES_CONFIG[dom]

            rule_def = DomainRuleDefinition(
                domain_code=dom,
                domain_title=cfg["title"],
                rule_set_version=DOMAIN_RULESET_VERSION,
                primary_karakas=cfg["karakas"],
                relevant_houses=cfg["houses"],
                varga_code=cfg["varga"],
                rule_description=cfg["description"]
            )

            # 1. Shadbala Domain Evidence
            shad_dom = master_evidence.shadbala_evidence.domain_strengths.get(dom) if master_evidence.shadbala_evidence else None

            # 2. Varga Evidence
            v_ev = master_evidence.varga_evidence.varga_evidences.get(cfg["varga"]) if master_evidence.varga_evidence else None

            # 3. Section 3 Compliance: Domain-Scoped Yogas & Doshas
            rel_karakas = cfg["karakas"]
            rel_houses = cfg["houses"]

            domain_yogas = [
                y.name for y in master_evidence.yoga_suite.detected_yogas
                if any(p in rel_karakas for p in y.participating_planets) or any(h in rel_houses for h in y.participating_houses)
            ] if master_evidence.yoga_suite else []

            domain_doshas = [
                d.name for d in master_evidence.dosha_suite.detected_doshas
                if any(p in rel_karakas for p in d.participating_planets) or any(h in rel_houses for h in d.participating_houses)
            ] if master_evidence.dosha_suite else []

            # 4. Section 5 Compliance: Ashtakavarga SAV Evidence across ALL domain houses with explicit unavailable state (sav_bindus = None, NOT 0!)
            sav_house_evs: List[HouseSAVEvidence] = []
            has_live_sav = False
            for h_num in cfg["houses"]:
                target_r_idx = ((lagna_r_idx + h_num - 2) % 12) + 1
                sav_ev = next((e for e in master_evidence.ashtakavarga_evidence.house_sav_evidences if e.rashi_index == target_r_idx), None) if master_evidence.ashtakavarga_evidence else None
                if sav_ev and sav_ev.sav_bindus is not None:
                    sav_house_evs.append(sav_ev)
                    has_live_sav = True
                else:
                    sav_house_evs.append(HouseSAVEvidence(
                        rashi_index=target_r_idx,
                        rashi_name=RASHI_NAMES[target_r_idx - 1],
                        sav_bindus=None, # None when unavailable (never 0!)
                        strength_category="UNAVAILABLE",
                        transit_recommendation="Ashtakavarga SAV evidence unavailable for this house"
                    ))

            # 5. Section 7 Compliance: Domain-Scoped Jaimini CharaKarakaInfo objects
            ak_info = master_evidence.jaimini_suite.chara_karakas.get("AK") if (master_evidence.jaimini_suite and dom in ["PERSONAL_DEVELOPMENT", "SPIRITUALITY"]) else None
            amk_info = master_evidence.jaimini_suite.chara_karakas.get("AmK") if (master_evidence.jaimini_suite and dom in ["CAREER", "BUSINESS", "FINANCE"]) else None
            dk_info = master_evidence.jaimini_suite.chara_karakas.get("DK") if (master_evidence.jaimini_suite and dom in ["MARRIAGE", "RELATIONSHIP"]) else None

            # 6. Section 1 & 2 Compliance: Structured Domain-Scoped Transits Evidence (Zero target_name string searching!)
            if master_evidence.transit_snapshot and master_evidence.transit_snapshot.aspects:
                dom_aspects = []
                for asp in master_evidence.transit_snapshot.aspects:
                    is_karaka_target = (asp.target_type == "PLANET" and asp.target_planet in rel_karakas)
                    is_house_target = (asp.target_type == "HOUSE" and asp.target_house in rel_houses)
                    is_transiting_karaka = (asp.transiting_planet in rel_karakas)

                    if is_karaka_target or is_house_target or is_transiting_karaka:
                        dom_aspects.append(asp)

                if dom_aspects:
                    t_summary = f"AVAILABLE_WITH_CONTACTS: {len(dom_aspects)} domain-relevant aspect contacts detected."
                else:
                    t_summary = "AVAILABLE_NO_CONTACTS"
            elif master_evidence.transit_snapshot:
                t_summary = "AVAILABLE_NO_CONTACTS"
            else:
                t_summary = "UNAVAILABLE"

            # 7. Timing Windows for this domain
            dom_windows = [tw for tw in master_evidence.timing_suite.timing_windows if tw.domain == dom] if master_evidence.timing_suite else []

            # Section 3 Compliance: Precise Evidence Availability & Strength Class
            if v_ev or shad_dom or has_live_sav or domain_yogas or dom_windows:
                ev_status = "AVAILABLE"
                if shad_dom and shad_dom.domain_strength_class in ["HIGH", "MODERATE"]:
                    str_cls = shad_dom.domain_strength_class
                elif has_live_sav or dom_windows:
                    str_cls = "MODERATE"
                else:
                    str_cls = None
            else:
                ev_status = "UNAVAILABLE"
                str_cls = None

            trad_meta = {
                "methodology": "Parashari-domain-rule-set",
                "primary_karakas": ", ".join(cfg["karakas"]),
                "rule_description": cfg["description"]
            }

            obs_evidence = ObservedChartEvidence(
                varga_evidence=v_ev,
                detected_yogas=domain_yogas,
                detected_doshas=domain_doshas,
                active_dasha_summary=dasha_summary,
                active_transits_summary=t_summary,
                shadbala_domain_evidence=shad_dom,
                ashtakavarga_house_evidences=sav_house_evs,
                jaimini_atmakaraka_info=ak_info,
                jaimini_amatyakaraka_info=amk_info,
                jaimini_darakaraka_info=dk_info,
                timing_windows=dom_windows
            )

            domain_results[dom] = DomainPredictionEvidence(
                rule_definition=rule_def,
                observed_evidence=obs_evidence,
                evidence_status=ev_status,
                evidence_strength_class=str_cls,
                traditional_metadata=trad_meta
            )

        # Complete serialized evidence hash calculation
        serialized_evidence_dict = {
            dom: domain_results[dom].model_dump()
            for dom in sorted(domain_results.keys())
        }

        payload = {
            "master_hash": master_evidence.master_evidence_hash,
            "ruleset_version": DOMAIN_RULESET_VERSION,
            "evidence": serialized_evidence_dict
        }
        calc_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()

        return ComprehensivePredictionPackage(
            master_evidence_hash=master_evidence.master_evidence_hash,
            ruleset_version=DOMAIN_RULESET_VERSION,
            domain_predictions=domain_results,
            active_dasha_summary=dasha_summary,
            strongest_prediction_domain=None, # Nullable when no deterministic ranking methodology exists
            calculation_hash=calc_hash
        )
