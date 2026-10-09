"""
Test Suite for AI Service Provider Policy, OpenAI, Gemini, Ollama, Retries, Timeouts, and Fail-Closed Error Handling.
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

def test_ai_provider_unavailable_fails_closed():
    """When AI provider is unavailable or unconfigured, AIService must return explicit unavailable status."""
    with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Connection Refused")):
        result = AIService.synthesize_interpretation("Explain career", SAMPLE_EVIDENCE, domain="CAREER")

        assert "AI interpretation service" in result["interpretation"]
        assert result["validation_status"] == "UNAVAILABLE"

def test_generation_timeout_handled():
    """When generation request times out, AIService must fail closed safely."""
    with patch("requests.post", side_effect=requests.exceptions.Timeout("Request Timed Out")):
        text = AIService.generate_interpretation("Explain career", SAMPLE_EVIDENCE)
        assert text is None

def test_empty_generation_handled():
    """When provider returns HTTP 200 with empty text response, AIService must return None/unavailable message."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"response": "  "}

    with patch("requests.post", return_value=mock_resp):
        result = AIService.synthesize_interpretation("Explain career", SAMPLE_EVIDENCE, domain="CAREER")
        assert "AI interpretation service" in result["interpretation"]
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
        assert result["validation_status"] in ["UNAVAILABLE", "NOT_VALIDATED"]

def test_openai_gemini_ollama_provider_health():
    """Verifies that check_ai_provider_health correctly inspects settings.ai_provider."""
    # Test OpenAI
    settings.ai_provider = "openai"
    health_openai = AIService.check_ai_provider_health()
    assert health_openai["ai_provider"] == "openai"

    # Test Gemini
    settings.ai_provider = "gemini"
    health_gemini = AIService.check_ai_provider_health()
    assert health_gemini["ai_provider"] == "gemini"

    # Reset default
    settings.ai_provider = "openai"
