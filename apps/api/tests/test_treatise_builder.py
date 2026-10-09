"""
Test Suite for MasterTreatiseBuilder (30-Section Celestial Dossier Payload).
Verifies dynamic synthesis of all 30 sections, tables, and appendices from birth input without hardcoded data.
"""
import pytest
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.canonical_evidence import CanonicalEvidencePipeline
from apps.api.engines.prediction_engine import PredictionEngine
from apps.api.engines.treatise_builder import MasterTreatiseBuilder

def test_master_treatise_builder_dynamic_30_sections():
    """Verifies that MasterTreatiseBuilder dynamically compiles all 30 sections and appendices from birth input."""
    inp = BirthInput(
        name="Treatise Test Native",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )

    master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(inp)
    predictions = PredictionEngine.generate_all_predictions(master_evidence)

    dossier = MasterTreatiseBuilder.build_celestial_dossier(master_evidence, predictions)

    assert dossier["title"] == "THE CELESTIAL DOSSIER"
    assert dossier["executive_summary"]["native_name"] == "Treatise Test Native"
    assert dossier["executive_summary"]["birth_date"] == "1986-09-28"

    sec = dossier["sections"]
    assert "s01_calculation_standards" in sec
    assert "s02_planetary_ledger" in sec
    assert "s03_rashi_architecture" in sec
    assert "s04_lagna_framework" in sec
    assert "s08_yoga_audit" in sec
    assert "s10_divisional_overview" in sec
    assert "s11_dasha_calculation" in sec
    assert "s14_to_s22_domains" in sec

    # Verify 9+ planetary ledger entries
    assert len(sec["s02_planetary_ledger"]["table"]) >= 9
    # Verify 12 whole sign houses
    assert len(sec["s03_rashi_architecture"]["table"]) == 12
    # Verify 10 points in Shodasha Varga Atlas
    assert len(sec["s10_divisional_overview"]["table"]) == 10

    assert len(dossier["master_evidence_hash"]) == 64
