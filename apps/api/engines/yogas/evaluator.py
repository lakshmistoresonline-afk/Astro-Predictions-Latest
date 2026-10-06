"""
Authoritative Yoga Evaluation Engine for Astrovision.
Orchestrates rule evaluation across all supported classical Parashari Yogas.
"""
import hashlib
import json
from typing import List, Dict

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.yogas.models import YogaResult, YogaSuiteResult
from apps.api.engines.yogas.rules import (
    evaluate_pancha_mahapurusha,
    evaluate_gaja_kesari,
    evaluate_budha_aditya,
    evaluate_dharma_karma,
    evaluate_parivartana_yogas,
    evaluate_viparita_raja_yogas,
    evaluate_neecha_bhanga,
    evaluate_chandra_yogas,
    evaluate_surya_yogas
)

class YogaEvaluator:
    """
    Authoritative Yoga Evaluator Engine.
    Source Separation: Consumes Phase 2A Canonical Vedic Chart. Never calls ephemeris or recalculates positions.
    """

    @classmethod
    def evaluate_all_yogas(cls, canonical_chart: CanonicalVedicChart) -> YogaSuiteResult:
        all_results: List[YogaResult] = []

        # 1. Pancha Mahapurusha
        all_results.extend(evaluate_pancha_mahapurusha(canonical_chart))

        # 2. Gaja Kesari
        all_results.append(evaluate_gaja_kesari(canonical_chart))

        # 3. Budha Aditya
        all_results.append(evaluate_budha_aditya(canonical_chart))

        # 4. Dharma-Karma Adhipati
        all_results.append(evaluate_dharma_karma(canonical_chart))

        # 5. Parivartana Yogas
        all_results.extend(evaluate_parivartana_yogas(canonical_chart))

        # 6. Viparita Raja Yogas
        all_results.extend(evaluate_viparita_raja_yogas(canonical_chart))

        # 7. Neecha Bhanga Raja Yogas
        all_results.extend(evaluate_neecha_bhanga(canonical_chart))

        # 8. Chandra Yogas
        all_results.extend(evaluate_chandra_yogas(canonical_chart))

        # 9. Surya Yogas
        all_results.extend(evaluate_surya_yogas(canonical_chart))

        detected = [y for y in all_results if y.status == "DETECTED"]

        # Summary Counts
        summary = {
            "total_evaluated": len(all_results),
            "detected_count": len(detected),
            "mahapurusha_count": sum(1 for y in detected if y.category == "Mahapurusha"),
            "raja_count": sum(1 for y in detected if y.category in ["Raja", "Viparita", "NeechaBhanga"]),
        }

        # Calculation Hash derived from complete evaluated rule evidence (Requirement 13)
        payload = {
            "chart_hash": canonical_chart.calculation_hash,
            "evaluated_rule_states": {y.rule_id: y.status for y in sorted(all_results, key=lambda r: r.rule_id)},
            "rule_set_version": "yoga_rules_v1"
        }
        yoga_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return YogaSuiteResult(
            chart_hash=canonical_chart.calculation_hash,
            detected_yogas=detected,
            all_evaluated_yogas=all_results,
            summary_counts=summary,
            rule_set_version="yoga_rules_v1"
        )
