from apps.api.engines.evidence_aggregator import EvidenceAggregator

class PredictionEngine:
    """
    PredictionEngine produces structured prediction evidence across domains
    (Career, Finance, Marriage, Education, Family, Travel, Wellbeing).
    """

    DOMAINS = [
        "CAREER", "FINANCE", "BUSINESS", "MARRIAGE", "RELATIONSHIP",
        "EDUCATION", "FAMILY", "CHILDREN", "PROPERTY", "TRAVEL",
        "RELOCATION", "SPIRITUALITY", "PERSONAL_DEVELOPMENT", "WELLBEING"
    ]

    @classmethod
    def generate_all_predictions(cls, vedic_data: dict, yogas: list, dasha_info: dict) -> list:
        predictions = []
        for domain in cls.DOMAINS:
            evidence = EvidenceAggregator.aggregate_evidence(domain, vedic_data, yogas, dasha_info)
            predictions.append(evidence)
        return predictions
