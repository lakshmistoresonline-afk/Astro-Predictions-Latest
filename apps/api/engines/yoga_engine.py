"""
Legacy Adapter Wrapper for Yoga Engine.
Delegates directly to Authoritative YogaEvaluator and DoshaEvaluator (apps.api.engines.yogas & doshas).
Preserves API contract for existing report generation, evidence aggregation, and prediction consumers.
"""
from typing import Dict, List, Any, Optional

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.yogas import YogaEvaluator
from apps.api.engines.doshas import DoshaEvaluator


class YogaEngine:
    """
    Adapter wrapper ensuring single source of truth delegation to YogaEvaluator and DoshaEvaluator.
    """

    @classmethod
    def detect_yogas(
        cls,
        planetary_positions: dict,
        birth_input: Optional[BirthInput] = None
    ) -> List[Dict[str, Any]]:
        """
        Detects traditional Vedic yogas and doshas using Authoritative Yoga and Dosha Engines.
        Fails closed if birth_input is missing.
        """
        if not birth_input:
            raise ValueError("birth_input is required for Yoga and Dosha detection.")

        chart = build_canonical_vedic_chart(birth_input)
        yoga_suite = YogaEvaluator.evaluate_all_yogas(chart)
        dosha_suite = DoshaEvaluator.evaluate_all_doshas(chart)

        yogas_list = []

        # 1. Add detected Yogas
        for y in yoga_suite.detected_yogas:
            yogas_list.append({
                "id": y.rule_id,
                "name": y.name,
                "description": f"{y.sanskrit_name or y.name} ({y.category} Category): Conditions satisfied."
            })

        # 2. Add detected Doshas
        for d in dosha_suite.detected_doshas:
            yogas_list.append({
                "id": d.rule_id,
                "name": d.name,
                "description": f"{d.sanskrit_name or d.name}: Condition detected."
            })

        return yogas_list
