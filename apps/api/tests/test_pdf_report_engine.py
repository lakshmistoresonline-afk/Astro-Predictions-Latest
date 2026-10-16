"""
Unit Test Suite for PDFReportEngine 30-Section Master PDF Treatise Generation.
"""
import pytest
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

def test_pdf_report_engine_bytes_output():
    """generate_pdf_report must return valid binary PDF byte stream starting with %PDF-1.4."""
    bytes_out = PDFReportEngine.generate_pdf_report(PROFILE_A_DATA)

    assert isinstance(bytes_out, bytes)
    assert len(bytes_out) > 5000
    assert bytes_out.startswith(b"%PDF-1.4")

def test_comparative_profiles_produce_different_pdf_payloads():
    """Generating reports for Profile A vs Profile B must yield different, profile-specific PDF bytes."""
    bytes_a = PDFReportEngine.generate_pdf_report(PROFILE_A_DATA)
    bytes_b = PDFReportEngine.generate_pdf_report(PROFILE_B_DATA)

    assert bytes_a != bytes_b
    assert len(bytes_a) > 5000
    assert len(bytes_b) > 5000

def test_pdf_report_engine_renders_all_30_sections():
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
