"""
Authoritative Muhurta Engine Foundation.
Evaluates Panchanga factor suitability, Rahu Kalam/Yamaganda/Gulika exclusions, Abhijit Muhurta, and activity-specific rules.
Sections 1..10 Compliance:
- Pure deterministic rule precedence architecture (MUHURTA_RULESET_VERSION = "2026.1_MUHURTA_PRECEDENCE_V2").
- Evaluates Rahu Kalam, Yamaganda, Gulika Kalam, and Abhijit Muhurta time windows via timezone-aware UTC-normalized datetime comparison.
- Outside-exclusion windows classified as CLEAR/NEUTRAL_FACTOR.
- Explicit Tithi (1..30) and Karana nature classification.
- Supports all 6 major activities (TRAVEL, MARRIAGE, BUSINESS, EDUCATION, PROPERTY, SPIRITUALITY).
- Unified canonical public API: evaluate_all_activities and calculate_muhurta_suite.
- Fails closed with ValueError for unsupported or invalid activity names!
"""
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional

from apps.api.engines.astronomy.provider import BaseAstronomyProvider
from apps.api.engines.panchanga.models import PanchangaResult
from apps.api.engines.panchanga.engine import PanchangaEngine
from apps.api.engines.muhurta.models import (
    ActivityRuleResult,
    MuhurtaEvaluation,
    MuhurtaSuiteResult
)

MUHURTA_RULESET_VERSION = "2026.1_MUHURTA_PRECEDENCE_V2"

# Traditional Activity Rules
ACTIVITY_FAVORABLE_NAKSHATRAS = {
    "TRAVEL": ["Aswini", "Rohini", "Mrigasira", "Punarvasu", "Pushya", "Hasta", "Anuradha", "Shravana", "Dhanishta", "Revati"],
    "MARRIAGE": ["Rohini", "Mrigasira", "Magha", "Uttara Phalguni", "Hasta", "Swati", "Anuradha", "Uttara Ashadha", "Uttara Bhadrapada", "Revati"],
    "BUSINESS": ["Aswini", "Rohini", "Punarvasu", "Pushya", "Hasta", "Swati", "Anuradha", "Shravana", "Dhanishta", "Satabhisha", "Revati"],
    "EDUCATION": ["Aswini", "Rohini", "Mrigasira", "Punarvasu", "Pushya", "Hasta", "Chitra", "Swati", "Anuradha", "Shravana", "Revati"],
    "PROPERTY": ["Rohini", "Uttara Phalguni", "Hasta", "Chitra", "Anuradha", "Uttara Ashadha", "Uttara Bhadrapada", "Dhanishta"],
    "SPIRITUALITY": ["Rohini", "Mrigasira", "Punarvasu", "Pushya", "Hasta", "Swati", "Anuradha", "Shravana", "Dhanishta", "Satabhisha", "Uttara Bhadrapada", "Revati"]
}

def _parse_dt(iso_str: str) -> datetime:
    """Parses ISO string into timezone-aware datetime normalized to UTC."""
    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            raise ValueError(f"ISO datetime string '{iso_str}' must be timezone-aware.")
        return dt.astimezone(timezone.utc)
    except Exception as e:
        raise ValueError(f"Invalid ISO datetime string '{iso_str}': {str(e)}")

def _is_time_in_window(eval_iso: str, start_iso: str, end_iso: str) -> bool:
    """Determines whether evaluated ISO time falls within timezone-aware start and end window."""
    e_dt = _parse_dt(eval_iso)
    s_dt = _parse_dt(start_iso)
    end_dt = _parse_dt(end_iso)
    return s_dt <= e_dt <= end_dt

class MuhurtaEngine:
    """
    Authoritative Muhurta Engine.
    Evaluates Panchanga suitability for major life activities using pure deterministic rule precedence.
    """

    @classmethod
    def evaluate_muhurta(
        cls,
        panchanga: PanchangaResult,
        activity_name: str
    ) -> MuhurtaEvaluation:
        if not activity_name or not isinstance(activity_name, str):
            raise ValueError("activity_name must be a non-empty string.")

        act = activity_name.strip().upper()
        if act not in ACTIVITY_FAVORABLE_NAKSHATRAS:
            raise ValueError(
                f"Unsupported Muhurta activity '{activity_name}'. "
                f"Supported activities: {list(ACTIVITY_FAVORABLE_NAKSHATRAS.keys())}"
            )

        factors: List[ActivityRuleResult] = []

        # 1. Tithi Check (Explicit 1..30 Rikta / Amavasya Tithi classification)
        t_num = panchanga.tithi.tithi_number
        is_rikta_or_amavasya = (t_num in [4, 9, 14, 19, 24, 29, 30])
        if is_rikta_or_amavasya:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_TITHI",
                factor_name="Tithi",
                rule_category="UNFAVORABLE_FACTOR",
                status="UNFAVORABLE",
                is_hard_exclusion=False,
                description=f"Tithi {panchanga.tithi.tithi_name} ({panchanga.tithi.paksha}) is a Rikta/Inauspicious Tithi."
            ))
        else:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_TITHI",
                factor_name="Tithi",
                rule_category="FAVORABLE_FACTOR",
                status="FAVORABLE",
                is_hard_exclusion=False,
                description=f"Tithi {panchanga.tithi.tithi_name} ({panchanga.tithi.paksha}) is auspicious for {act}."
            ))

        # 2. Nakshatra Check
        fav_naks = ACTIVITY_FAVORABLE_NAKSHATRAS[act]
        if panchanga.nakshatra_name in fav_naks:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_NAKSHATRA",
                factor_name="Nakshatra",
                rule_category="FAVORABLE_FACTOR",
                status="FAVORABLE",
                is_hard_exclusion=False,
                description=f"Nakshatra {panchanga.nakshatra_name} is listed as favorable for {act}."
            ))
        else:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_NAKSHATRA",
                factor_name="Nakshatra",
                rule_category="NEUTRAL_FACTOR",
                status="NEUTRAL",
                is_hard_exclusion=False,
                description=f"Nakshatra {panchanga.nakshatra_name} is not explicitly listed as favorable for {act}."
            ))

        # 3. Nitya Yoga Check
        if panchanga.nitya_yoga.nature == "Inauspicious":
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_NITYA_YOGA",
                factor_name="Nitya Yoga",
                rule_category="UNFAVORABLE_FACTOR",
                status="UNFAVORABLE",
                is_hard_exclusion=False,
                description=f"Nitya Yoga {panchanga.nitya_yoga.yoga_name} is inauspicious."
            ))
        else:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_NITYA_YOGA",
                factor_name="Nitya Yoga",
                rule_category="FAVORABLE_FACTOR",
                status="FAVORABLE",
                is_hard_exclusion=False,
                description=f"Nitya Yoga {panchanga.nitya_yoga.yoga_name} is auspicious."
            ))

        # 4. Karana Check (Vishti/Bhadra hard exclusion)
        is_vishti = (panchanga.karana.nature == "Vishti/Bhadra" or "Vishti" in panchanga.karana.karana_name)
        if is_vishti:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_KARANA",
                factor_name="Karana",
                rule_category="HARD_EXCLUSION",
                status="EXCLUDED",
                is_hard_exclusion=True,
                description=f"Karana Vishti (Bhadra) is active; inauspicious for initiating major ventures."
            ))
        elif panchanga.karana.nature == "Inauspicious":
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_KARANA",
                factor_name="Karana",
                rule_category="UNFAVORABLE_FACTOR",
                status="UNFAVORABLE",
                is_hard_exclusion=False,
                description=f"Karana {panchanga.karana.karana_name} is inauspicious for {act}."
            ))
        else:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_KARANA",
                factor_name="Karana",
                rule_category="FAVORABLE_FACTOR",
                status="FAVORABLE",
                is_hard_exclusion=False,
                description=f"Karana {panchanga.karana.karana_name} is favorable."
            ))

        # 5. Rahu Kalam Check (Hard exclusion window)
        rahu_active = _is_time_in_window(panchanga.datetime_iso, panchanga.rahu_kalam.start_time_iso, panchanga.rahu_kalam.end_time_iso)
        if rahu_active:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_RAHU_KALAM",
                factor_name="Rahu Kalam",
                rule_category="HARD_EXCLUSION",
                status="EXCLUDED",
                is_hard_exclusion=True,
                description="Rahu Kalam is active; auspicious initiatives are prohibited."
            ))
        else:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_RAHU_KALAM",
                factor_name="Rahu Kalam",
                rule_category="NEUTRAL_FACTOR",
                status="NEUTRAL",
                is_hard_exclusion=False,
                description="Outside Rahu Kalam window (Clear)."
            ))

        # 6. Yamaganda Check (Hard exclusion window)
        yamaganda_active = _is_time_in_window(panchanga.datetime_iso, panchanga.yamaganda.start_time_iso, panchanga.yamaganda.end_time_iso)
        if yamaganda_active:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_YAMAGANDA",
                factor_name="Yamaganda",
                rule_category="HARD_EXCLUSION",
                status="EXCLUDED",
                is_hard_exclusion=True,
                description="Yamaganda is active; inauspicious window prohibited for major initiatives."
            ))
        else:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_YAMAGANDA",
                factor_name="Yamaganda",
                rule_category="NEUTRAL_FACTOR",
                status="NEUTRAL",
                is_hard_exclusion=False,
                description="Outside Yamaganda window (Clear)."
            ))

        # 7. Gulika Kalam Check (Unfavorable factor)
        gulika_active = _is_time_in_window(panchanga.datetime_iso, panchanga.gulika_kalam.start_time_iso, panchanga.gulika_kalam.end_time_iso)
        if gulika_active:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_GULIKA",
                factor_name="Gulika Kalam",
                rule_category="UNFAVORABLE_FACTOR",
                status="UNFAVORABLE",
                is_hard_exclusion=False,
                description="Gulika Kalam is active; unfavorable period for initiating new actions."
            ))
        else:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_GULIKA",
                factor_name="Gulika Kalam",
                rule_category="NEUTRAL_FACTOR",
                status="NEUTRAL",
                is_hard_exclusion=False,
                description="Outside Gulika Kalam window (Clear)."
            ))

        # 8. Abhijit Muhurta Check (Auspicious temporal window)
        abhijit_active = _is_time_in_window(panchanga.datetime_iso, panchanga.abhijit_muhurta.start_time_iso, panchanga.abhijit_muhurta.end_time_iso)
        if abhijit_active:
            factors.append(ActivityRuleResult(
                rule_id="MUHURTA_RULE_ABHIJIT",
                factor_name="Abhijit Muhurta",
                rule_category="FAVORABLE_FACTOR",
                status="FAVORABLE",
                is_hard_exclusion=False,
                description="Abhijit Muhurta is active; auspicious temporal window for initiating major ventures."
            ))

        # Pure Rule Precedence Recommendation Derivation
        has_hard_exclusion = any(f.is_hard_exclusion for f in factors)
        has_unfavorable_factor = any(f.status == "UNFAVORABLE" for f in factors)
        has_favorable_factor = any(f.status == "FAVORABLE" for f in factors)

        if has_hard_exclusion:
            rec = "EXCLUDED"
            precedence_rule_id = "PRECEDENCE_1_HARD_EXCLUSION_ACTIVE"
        elif has_unfavorable_factor:
            rec = "NOT_RECOMMENDED"
            precedence_rule_id = "PRECEDENCE_2_UNFAVORABLE_CONDITION_ACTIVE"
        elif has_favorable_factor:
            rec = "RECOMMENDED"
            precedence_rule_id = "PRECEDENCE_3_FAVORABLE_CONDITIONS_SATISFIED"
        else:
            rec = "FAVORABLE_WITH_CAUTION"
            precedence_rule_id = "PRECEDENCE_4_NEUTRAL_CONDITIONS"

        favorable_count = sum(1 for f in factors if f.status == "FAVORABLE")
        unfavorable_count = sum(1 for f in factors if f.status == "UNFAVORABLE")

        summary_text = f"Activity {act} evaluated as {rec} via {precedence_rule_id}."
        if has_hard_exclusion:
            summary_text += " Prohibited due to active hard exclusion window (e.g. Rahu Kalam, Yamaganda, or Vishti Karana)."

        payload = {
            "panchanga_hash": panchanga.calculation_hash,
            "activity": act,
            "recommendation": rec,
            "precedence_rule_id": precedence_rule_id,
            "has_hard_exclusion": has_hard_exclusion,
            "favorable_count": favorable_count,
            "unfavorable_count": unfavorable_count,
            "evaluated_factor_ids": sorted([f.rule_id for f in factors]),
            "ruleset": MUHURTA_RULESET_VERSION
        }
        ev_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return MuhurtaEvaluation(
            activity_name=act,
            datetime_iso=panchanga.datetime_iso,
            recommendation=rec,
            overall_suitability_score=None,
            is_rahu_kalam_active=rahu_active,
            is_abhijit_active=abhijit_active,
            has_hard_exclusion=has_hard_exclusion,
            favorable_factor_count=favorable_count,
            unfavorable_factor_count=unfavorable_count,
            evaluated_factors=factors,
            summary=summary_text,
            calculation_hash=ev_hash
        )

    @classmethod
    def evaluate_all_activities(
        cls,
        panchanga: Optional[PanchangaResult] = None,
        dt: Optional[datetime] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        location_name: str = "Local Observer",
        astronomy_provider: Optional[BaseAstronomyProvider] = None
    ) -> MuhurtaSuiteResult:
        """
        Primary canonical public API for evaluating all supported Muhurta activities.
        Consumes canonical PanchangaResult evidence directly, or calculates it from observer parameters.
        """
        if not panchanga:
            if not dt or latitude is None or longitude is None:
                raise ValueError("Either panchanga or (dt, latitude, longitude) must be provided for Muhurta evaluation.")
            panchanga = PanchangaEngine.calculate_panchanga(
                dt=dt,
                latitude=latitude,
                longitude=longitude,
                location_name=location_name,
                astronomy_provider=astronomy_provider
            )
        return cls.calculate_muhurta_suite(panchanga)

    @classmethod
    def calculate_muhurta_suite(
        cls,
        panchanga: PanchangaResult
    ) -> MuhurtaSuiteResult:
        """
        Calculates complete Muhurta suite across all supported activities.
        """
        evaluations: Dict[str, MuhurtaEvaluation] = {}
        for act in ACTIVITY_FAVORABLE_NAKSHATRAS.keys():
            evaluations[act] = cls.evaluate_muhurta(panchanga, act)

        payload = {
            "panchanga_hash": panchanga.calculation_hash,
            "datetime_iso": panchanga.datetime_iso,
            "activities": sorted(list(evaluations.keys())),
            "recommendations": {k: evaluations[k].recommendation for k in evaluations},
            "evaluation_hashes": {k: evaluations[k].calculation_hash for k in evaluations},
            "ruleset": MUHURTA_RULESET_VERSION
        }
        suite_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return MuhurtaSuiteResult(
            panchanga_hash=panchanga.calculation_hash,
            datetime_iso=panchanga.datetime_iso,
            evaluations=evaluations,
            calculation_hash=suite_hash
        )
