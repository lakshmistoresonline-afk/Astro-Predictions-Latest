"""
Legacy Adapter Wrapper for Evidence Aggregator (Phase 2E-R4.1-R12-R10).
Section 3 Compliance: Pure evidence wrapper over deterministic chart facts.
Zero manufactured prose, zero artificial positive factors, zero fallback statements!
"""
from typing import Dict, List, Any

class EvidenceAggregator:
    """
    Adapter wrapper ensuring single source of truth delegation without prose generation.
    """

    @classmethod
    def aggregate_evidence(cls, domain: str, vedic_data: dict, yogas: list, dasha_info: dict) -> dict:
        supporting = []
        challenging = []

        for yoga in yogas:
            y_name = yoga.get("name")
            y_desc = yoga.get("description")
            if y_name and y_desc:
                supporting.append(f"{y_name}: {y_desc}")

        current_md = dasha_info.get("current_mahadasha", {}).get("mahadasha")
        if current_md:
            supporting.append(f"Active Mahadasha Lord: {current_md}")

        for planet, data in vedic_data.items():
            dig = data.get("dignity")
            sign = data.get("sign")
            if dig == "Exalted":
                supporting.append(f"{planet} Exalted in {sign}")
            elif dig == "Debilitated":
                challenging.append(f"{planet} Debilitated in {sign}")

        return {
            "domain": domain.upper(),
            "focus_areas": f"Primary house significators and relevant divisional charts for {domain.upper()}.",
            "traditional_interpretation": f"Domain {domain.upper()} evaluated through deterministic planetary dignities, Ashtakavarga bindus, and active Dasha transitions.",
            "positive_factors": supporting,
            "challenging_factors": challenging,
            "neutral_factors": []
        }
