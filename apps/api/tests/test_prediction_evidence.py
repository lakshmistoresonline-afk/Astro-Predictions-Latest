"""
Test Suite for Prediction Evidence Engine (14 Domains).
Verifies complete deterministic evidence exposure across all 14 prediction domains.
"""
import pytest
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.canonical_evidence import CanonicalEvidencePipeline
from apps.api.engines.prediction_engine import PredictionEngine, DOMAIN_RULES_CONFIG

def test_14_prediction_domains_complete_evidence():
    """Verifies that all 14 prediction domains contain complete rule definitions and evidence structures."""
    inp = BirthInput(
        name="Evidence Test Native",
        year=1992, month=8, day=15,
        hour=10, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=28.6139, longitude=77.2090
    )

    master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(inp)
    pkg = PredictionEngine.generate_all_predictions(master_evidence)

    assert len(pkg.domain_predictions) == 14
    for dom_code, dom_cfg in DOMAIN_RULES_CONFIG.items():
        assert dom_code in pkg.domain_predictions
        dom_ev = pkg.domain_predictions[dom_code]

        # Rule Definition
        assert dom_ev.rule_definition.domain_code == dom_code
        assert dom_ev.rule_definition.varga_code == dom_cfg["varga"]
        assert len(dom_ev.rule_definition.primary_karakas) > 0
        assert len(dom_ev.rule_definition.relevant_houses) > 0

        # Observed Evidence
        obs = dom_ev.observed_evidence
        assert obs.varga_evidence is not None
        assert obs.shadbala_domain_evidence is not None
        assert len(obs.ashtakavarga_house_evidences) > 0
        assert dom_ev.evidence_status in ["AVAILABLE", "UNAVAILABLE"]

        # Calculation Hashes
        assert len(dom_ev.traditional_metadata) > 0
        assert len(pkg.calculation_hash) == 64
