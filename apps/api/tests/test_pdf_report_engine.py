"""
Unit Test Suite for PDFReportEngine HTML/PDF Treatise Generation.
"""
import pytest
from apps.api.engines.pdf_report_engine import PDFReportEngine

SAMPLE_REPORT_DATA = {
    "name": "<script>alert('xss')</script> John Doe",
    "birth_date": "1995-01-01",
    "birth_time": "12:00:00",
    "timezone": "Asia/Kolkata",
    "location": {"place": "New Delhi", "country": "India", "latitude": 28.6139, "longitude": 77.2090},
    "master_evidence_hash": "master_hash_999999999",
    "canonical_chart": {
        "ascendant": {"sign": "Aries", "degree": 15, "minute": 30},
        "placements": {
            "Sun": {"rashi": {"sign": "Sagittarius", "degree": 16, "minute": 45}, "nakshatra_pada": {"nakshatra": "Purva Ashadha", "pada": 2}, "retrograde": False}
        },
        "whole_sign_houses": [
            {"house_number": 1, "sign": "Aries", "start_longitude": 0.0, "end_longitude": 30.0}
        ]
    },
    "vargas": {
        "D1": {"ascendant": "Aries", "placements": {"Sun": "Sagittarius", "Moon": "Cancer"}}
    },
    "dashas": {
        "birth_balance": {"mahadasha_lord": "Venus", "remaining_years": 12.5},
        "mahadashas": [
            {"lord": "Venus", "start_utc_iso": "1995-01-01T06:30:00+00:00", "end_utc_iso": "2007-07-01T06:30:00+00:00", "duration_years": 12.5}
        ]
    },
    "predictions": {
        "domain_predictions": {
            "CAREER": {
                "rule_definition": {"domain_title": "Career & Profession", "rule_description": "10th House Karma"},
                "evidence_status": "AVAILABLE"
            }
        }
    }
}

def test_pdf_report_engine_renders_all_12_chapters():
    """PDFReportEngine must render all 12 chapters explicitly."""
    html_out = PDFReportEngine.generate_html_treatise(SAMPLE_REPORT_DATA)

    for chapter_num in range(1, 13):
        assert f"Chapter {chapter_num}:" in html_out

def test_pdf_report_engine_escapes_user_input():
    """User-controlled inputs containing HTML tags must be properly escaped."""
    html_out = PDFReportEngine.generate_html_treatise(SAMPLE_REPORT_DATA)

    assert "<script>" not in html_out
    assert "&lt;script&gt;" in html_out

def test_pdf_report_engine_preserves_hashes_and_disclaimer():
    """PDFReportEngine must preserve master evidence hash and legal disclaimer."""
    html_out = PDFReportEngine.generate_html_treatise(SAMPLE_REPORT_DATA)

    assert "master_hash_999999999" in html_out
    assert "DISCLAIMER" in html_out
    assert "NASA JPL DE440s" in html_out

def test_pdf_report_engine_bytes_output():
    """generate_pdf_report must return valid binary PDF byte stream starting with %PDF-."""
    bytes_out = PDFReportEngine.generate_pdf_report(SAMPLE_REPORT_DATA)

    assert isinstance(bytes_out, bytes)
    assert len(bytes_out) > 500
    assert bytes_out.startswith(b"%PDF-")
