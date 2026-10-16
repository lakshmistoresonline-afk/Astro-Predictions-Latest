"""
Unit Test Suite for PDFReportEngine 30-Section Master PDF Treatise Generation with PDF Text Extraction.
"""
import io
import pytest
import pypdf
from apps.api.engines.pdf_report_engine import PDFReportEngine
from apps.api.engines.report_engine import ReportGeneratorEngine

PROFILE_A_DATA = {
    "name": "Subramanian T S",
    "birth_date": "1986-09-28",
    "birth_time": "16:30:00",
    "timezone": "Asia/Kolkata",
    "location": {"place": "Palakkad, Kerala", "country": "India", "latitude": 10.7867, "longitude": 76.6548},
    "master_evidence_hash": "subramanian_hash_11111111111111111111",
    "canonical_chart": {
        "ascendant": {"sign": "Aquarius", "degree": 12, "minute": 40},
        "placements": {
            "Sun": {"rashi": {"sign": "Virgo", "degree": 11, "minute": 21}, "nakshatra_pada": {"nakshatra": "Hasta", "pada": 1}, "retrograde": False},
            "Moon": {"rashi": {"sign": "Cancer", "degree": 7, "minute": 12}, "nakshatra_pada": {"nakshatra": "Pushya", "pada": 2}, "retrograde": False}
        },
        "whole_sign_houses": [
            {"house_number": 1, "sign": "Aquarius", "start_longitude": 300.0, "end_longitude": 330.0}
        ]
    },
    "planetary_positions": {
        "Sun": {"sign": "Virgo", "degree": 11.35, "speed": 0.98, "retrograde": False},
        "Moon": {"sign": "Cancer", "degree": 7.20, "speed": 12.25, "retrograde": False}
    },
    "dashas": {
        "birth_balance": {"mahadasha_lord": "Saturn", "remaining_years": 12.5}
    }
}

PROFILE_B_DATA = {
    "name": "John Doe",
    "birth_date": "1995-01-01",
    "birth_time": "12:00:00",
    "timezone": "America/New_York",
    "location": {"place": "New York", "country": "United States", "latitude": 40.7128, "longitude": -74.0060},
    "master_evidence_hash": "john_doe_hash_22222222222222222222",
    "canonical_chart": {
        "ascendant": {"sign": "Aries", "degree": 15, "minute": 30},
        "placements": {
            "Sun": {"rashi": {"sign": "Sagittarius", "degree": 16, "minute": 45}, "nakshatra_pada": {"nakshatra": "Purva Ashadha", "pada": 2}, "retrograde": False},
            "Moon": {"rashi": {"sign": "Taurus", "degree": 22, "minute": 10}, "nakshatra_pada": {"nakshatra": "Rohini", "pada": 4}, "retrograde": False}
        },
        "whole_sign_houses": [
            {"house_number": 1, "sign": "Aries", "start_longitude": 0.0, "end_longitude": 30.0}
        ]
    },
    "planetary_positions": {
        "Sun": {"sign": "Sagittarius", "degree": 16.75, "speed": 1.02, "retrograde": False},
        "Moon": {"sign": "Taurus", "degree": 22.16, "speed": 13.10, "retrograde": False}
    },
    "dashas": {
        "birth_balance": {"mahadasha_lord": "Venus", "remaining_years": 8.2}
    }
}

def test_pdf_report_engine_fails_closed_on_missing_required_data():
    """PDFReportEngine must raise ValueError when required birth data is missing."""
    with pytest.raises(ValueError) as exc_info:
        PDFReportEngine.generate_pdf_report({})
    assert "report_data" in str(exc_info.value) or "Missing" in str(exc_info.value)

def test_pdf_report_engine_bytes_and_extracted_text_content():
    """generate_pdf_report must return valid PDF bytes and render all 30 sections & Appendices A-D in extracted PDF text."""
    pdf_bytes = PDFReportEngine.generate_pdf_report(PROFILE_A_DATA)

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 5000
    assert pdf_bytes.startswith(b"%PDF-1.4")

    # Extract PDF text using pypdf
    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # Verify Native Name, Birth Date, and Hashes in PDF
    assert "SUBRAMANIAN T S" in full_text
    assert "1986-09-28" in full_text
    assert "Palakkad" in full_text

    # Verify 30 Section Headings in Extracted PDF Text
    for sec_num in range(1, 31):
        assert f"{sec_num}. " in full_text

    # Verify Appendices A-D in Extracted PDF Text
    assert "Appendix A - Raw Longitudes" in full_text
    assert "Appendix B - House Cusps" in full_text
    assert "Appendix C - Source & Method Notes" in full_text
    assert "Appendix D - Important Limitations" in full_text

def test_comparative_profiles_produce_different_pdf_extracted_text():
    """Generating reports for Profile A vs Profile B must yield different, profile-specific extracted PDF text."""
    pdf_a = PDFReportEngine.generate_pdf_report(PROFILE_A_DATA)
    pdf_b = PDFReportEngine.generate_pdf_report(PROFILE_B_DATA)

    assert pdf_a != pdf_b

    text_a = "".join(page.extract_text() for page in pypdf.PdfReader(io.BytesIO(pdf_a)).pages)
    text_b = "".join(page.extract_text() for page in pypdf.PdfReader(io.BytesIO(pdf_b)).pages)

    assert "SUBRAMANIAN T S" in text_a
    assert "JOHN DOE" in text_b
    assert "Aquarius" in text_a
    assert "Aries" in text_b

def test_pdf_report_engine_renders_all_30_sections_from_report_generator():
    """ReportGeneratorEngine must assemble all 30 sections in the treatise dictionary."""
    report_dict = ReportGeneratorEngine.generate_comprehensive_report(
        name="John Doe",
        year=1995, month=1, day=1,
        hour=12, minute=0,
        latitude=28.6139, longitude=77.2090,
        place_name="New Delhi", country="India",
        timezone_str="Asia/Kolkata"
    )

    assert "treatise" in report_dict
    sections = report_dict["treatise"].get("sections_list", [])
    assert len(sections) == 30
    assert sections[0]["title"].startswith("1. Calculation Standard")
    assert sections[29]["title"].startswith("30. Final Integrated Reading")
