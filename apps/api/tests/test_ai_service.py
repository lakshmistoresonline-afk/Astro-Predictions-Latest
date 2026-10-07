"""
Test Suite for AI Service Provider Policy, Retries, Timeouts, and Fail-Closed Error Handling.
"""
import pytest
from unittest.mock import patch, MagicMock
import requests

from apps.api.config import settings
from apps.api.services.ai_service import AIService

SAMPLE_EVIDENCE = {
    "master_evidence_hash": "test_hash_12345",
    "native_name": "Test Native",
    "domain_evidence": {"domain_title": "Career"}
}

def test_ollama_unavailable_fails_closed():
    """When Ollama provider is unavailable, AIService must return explicit unavailable status."""
    with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Ollama Connection Refused")):
        result = AIService.synthesize_interpretation("Explain career", SAMPLE_EVIDENCE, domain="CAREER")

        assert "AI interpretation service unavailable" in result["interpretation"]
        assert result["validation_status"] == "UNAVAILABLE"
        assert result["provider"] == "ollama"

def test_generation_timeout_handled():
    """When generation request times out, AIService must fail closed safely."""
    with patch("requests.post", side_effect=requests.exceptions.Timeout("Request Timed Out")):
        text = AIService.generate_interpretation("Explain career", SAMPLE_EVIDENCE)
        assert text is None

def test_empty_generation_handled():
    """When Ollama returns HTTP 200 with empty text response, AIService must return None/unavailable message."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"response": "  "}

    with patch("requests.post", return_value=mock_resp):
        result = AIService.synthesize_interpretation("Explain career", SAMPLE_EVIDENCE, domain="CAREER")
        assert "AI interpretation service unavailable" in result["interpretation"]
        assert result["validation_status"] == "UNAVAILABLE"

def test_validator_unavailable_returns_unavailable():
    """When validator provider encounters connection error, validation_status must be UNAVAILABLE."""
    mock_gen_resp = MagicMock()
    mock_gen_resp.status_code = 200
    mock_gen_resp.json.return_value = {"response": "Valid Parashari interpretation for career."}

    def side_effect(url, **kwargs):
        if "generate" in url:
            if kwargs.get("json", {}).get("model") == settings.ai_model_generation:
                return mock_gen_resp
            else:
                raise requests.exceptions.ConnectionError("Validator Connection Failed")
        raise requests.exceptions.ConnectionError("Connection Refused")

    with patch("requests.post", side_effect=side_effect):
        result = AIService.synthesize_interpretation("Explain career", SAMPLE_EVIDENCE, domain="CAREER")
        assert "Valid Parashari interpretation" in result["interpretation"]
        assert result["validation_status"] in ["UNAVAILABLE", "NOT_VALIDATED"]

def test_validator_malformed_result_returns_unavailable():
    """When validator returns malformed response text (not PASS or REPAIR), status must be NOT_VALIDATED."""
    mock_gen_resp = MagicMock()
    mock_gen_resp.status_code = 200
    mock_gen_resp.json.return_value = {"response": "Valid Parashari interpretation for career."}

    mock_val_resp = MagicMock()
    mock_val_resp.status_code = 200
    mock_val_resp.json.return_value = {"response": "SOMETHING_RANDOM_MALFORMED"}

    def side_effect(url, **kwargs):
        if kwargs.get("json", {}).get("model") == settings.ai_model_generation:
            return mock_gen_resp
        return mock_val_resp

    with patch("requests.post", side_effect=side_effect):
        result = AIService.synthesize_interpretation("Explain career", SAMPLE_EVIDENCE, domain="CAREER")
        assert result["validation_status"] in ["UNAVAILABLE", "NOT_VALIDATED"]
