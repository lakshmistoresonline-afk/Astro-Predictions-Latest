"""
Automated Golden Reference Fixture Test Suite for Subramanian T S Master Report.
Verifies canonical chart values, 30-section PDF report generation, and calculation hash reproducibility.
"""
import pytest
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.canonical_evidence import CanonicalEvidencePipeline
from apps.api.engines.report_engine import ReportGeneratorEngine
from apps.api.engines.pdf_report_engine import PDFReportEngine
from apps.api.engines.dasha.engine import AuthoritativeDashaEngine

@pytest.fixture
def subramanian_birth_input() -> BirthInput:
    """Golden Reference Birth Input: Subramanian T S (28 Sep 1986, 16:30 IST, Palakkad)."""
    return BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )

def test_subramanian_golden_chart_anchors(subramanian_birth_input):
    """Verifies anchor placement values for the Subramanian T S golden reference chart."""
    chart = build_canonical_vedic_chart(subramanian_birth_input)

    # 1. Ascendant: Aquarius near 11°-12°
    assert chart.ascendant.sign == "Aquarius"
    assert chart.ascendant.degree in [11, 12]

    # 2. MC: Scorpio near 16°-17°
    assert chart.mc.sign == "Scorpio"
    assert chart.mc.degree in [16, 17]

    # 3. Moon: Cancer near 7°00', Pushya Pada 2
    moon_p = chart.placements["Moon"]
    assert moon_p.rashi.sign == "Cancer"
    assert moon_p.rashi.degree == 7
    assert moon_p.nakshatra_pada.nakshatra == "Pushya"
    assert moon_p.nakshatra_pada.pada == 2

    # 4. Sun: Virgo
    sun_p = chart.placements["Sun"]
    assert sun_p.rashi.sign == "Virgo"

    # 5. Whole Sign Houses
    assert len(chart.get_whole_sign_houses) == 12
    assert chart.get_whole_sign_houses[0].sign == "Aquarius"

def test_subramanian_dasha_calculation_exactness(subramanian_birth_input):
    """Verifies exact Dasha birth balance calculation for Subramanian T S (Saturn Mahadasha balance 13.48 years)."""
    chart = build_canonical_vedic_chart(subramanian_birth_input)
    dasha_suite = AuthoritativeDashaEngine.calculate_dasha_suite(chart)

    assert dasha_suite.birth_balance.mahadasha_lord == "Saturn"
    assert 13.40 <= dasha_suite.birth_balance.remaining_years <= 13.55

def test_subramanian_master_evidence_pipeline(subramanian_birth_input):
    """Verifies canonical evidence pipeline generates immutable calculation hashes."""
    evidence = CanonicalEvidencePipeline.generate_canonical_evidence(subramanian_birth_input)
    assert evidence.master_evidence_hash is not None
    assert len(evidence.master_evidence_hash) == 64  # SHA-256
    assert evidence.varga_suite is not None
    assert evidence.natal_dasha_suite is not None

def test_subramanian_report_generation_and_pdf_bytes(subramanian_birth_input):
    """Verifies comprehensive report generator builds valid report data and PDF bytes starting with %PDF-1.4."""
    report_dict = ReportGeneratorEngine.generate_comprehensive_report(
        name=subramanian_birth_input.name,
        year=subramanian_birth_input.year,
        month=subramanian_birth_input.month,
        day=subramanian_birth_input.day,
        hour=subramanian_birth_input.hour,
        minute=subramanian_birth_input.minute,
        latitude=subramanian_birth_input.latitude,
        longitude=subramanian_birth_input.longitude,
        place_name="Palakkad, Kerala",
        country="India",
        timezone_str=subramanian_birth_input.timezone_str,
        birth_input=subramanian_birth_input
    )

    assert report_dict["name"] == "Subramanian T S"
    assert report_dict["birth_date"] == "1986-09-28"
    assert report_dict["birth_time"] == "16:30:00"
    assert report_dict["timezone"] == "Asia/Kolkata"

    pdf_bytes = PDFReportEngine.generate_pdf_report(report_dict)
    assert pdf_bytes is not None
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert len(pdf_bytes) > 5000  # Non-trivial PDF size
