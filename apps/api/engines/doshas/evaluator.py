"""
Authoritative Dosha Evaluation Engine for Astrovision.
Orchestrates rule evaluation across supported classical Parashari Doshas.
Section 1..12 Compliance: Suite calculation hash represents complete evaluated rule states.
"""
import hashlib
import json
from typing import List, Dict

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.doshas.models import DoshaResult, DoshaSuiteResult
from apps.api.engines.doshas.rules import (
    evaluate_manglik_dosha,
    evaluate_kemadruma_dosha,
    evaluate_kala_sarpa_dosha
)

class DoshaEvaluator:
    """
    Authoritative Dosha Evaluator Engine.
    Source Separation: Consumes Phase 2A Canonical Vedic Chart. Never calls ephemeris or recalculates positions.
    """

    @classmethod
    def evaluate_all_doshas(cls, canonical_chart: CanonicalVedicChart) -> DoshaSuiteResult:
        all_results: List[DoshaResult] = []

        # 1. Manglik / Kuja Dosha
        all_results.append(evaluate_manglik_dosha(canonical_chart))

        # 2. Kemadruma Dosha
        all_results.append(evaluate_kemadruma_dosha(canonical_chart))

        # 3. Kala Sarpa Condition
        all_results.append(evaluate_kala_sarpa_dosha(canonical_chart))

        detected = [d for d in all_results if d.status == "DETECTED"]
        cancelled = [d for d in all_results if d.status == "CANCELLED"]

        summary = {
            "total_evaluated": len(all_results),
            "detected_count": len(detected),
            "cancelled_count": len(cancelled),
            "manglik_status": next((d.status for d in all_results if d.rule_id == "DOSHA_MANGLIK"), "NOT_DETECTED"),
            "kemadruma_status": next((d.status for d in all_results if d.rule_id == "DOSHA_KEMADRUMA"), "NOT_DETECTED"),
            "kala_sarpa_status": next((d.status for d in all_results if d.rule_id == "DOSHA_KALA_SARPA"), "NOT_DETECTED"),
        }

        # Suite calculation hash derived from complete evaluated rule states
        payload = {
            "chart_hash": canonical_chart.calculation_hash,
            "evaluated_rule_states": {d.rule_id: d.status for d in sorted(all_results, key=lambda r: r.rule_id)},
            "rule_set_version": "dosha_rules_v1"
        }
        dosha_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return DoshaSuiteResult(
            chart_hash=canonical_chart.calculation_hash,
            detected_doshas=detected,
            all_evaluated_doshas=all_results,
            summary_counts=summary,
            rule_set_version="dosha_rules_v1"
        )
