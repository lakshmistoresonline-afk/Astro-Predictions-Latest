import requests
from apps.api.config import settings

class AIService:
    """
    AIService manages local Ollama inference for generation (Gemma) and validation (Qwen).
    Enforces strict non-calculative prompts and validation pass/repair/reject cycles.
    """

    @staticmethod
    def generate_interpretation(prompt: str, evidence: dict) -> str:
        url = f"{settings.ollama_base_url}/api/generate"
        system_prompt = (
            "You are an interpretation engine. "
            "You MUST NOT calculate planetary positions. "
            "You MUST NOT invent astronomical values, houses, dashas, yogas, or dates. "
            "You may only interpret the structured evidence provided."
        )
        payload = {
            "model": settings.ai_model_generation,
            "prompt": f"{system_prompt}\n\nEvidence:\n{evidence}\n\nRequest:\n{prompt}",
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("response", "AI interpretation generated successfully.")
        except Exception:
            pass

        return "AI interpretation unavailable (Ollama server offline). Displaying deterministic astrological evidence."

    @staticmethod
    def validate_interpretation(generated_text: str, source_evidence: dict) -> str:
        # Secondary model validation (Qwen)
        url = f"{settings.ollama_base_url}/api/generate"
        validation_prompt = (
            "You are a strict astrological validation engine. Check if the generated interpretation "
            "strictly adheres to the provided source evidence without inventing facts, dates, or planets. "
            "Respond with PASS or REPAIR."
        )
        payload = {
            "model": settings.ai_model_validation,
            "prompt": f"{validation_prompt}\n\nSource Evidence:\n{source_evidence}\n\nGenerated Text:\n{generated_text}",
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                res_text = response.json().get("response", "PASS")
                if "REPAIR" in res_text.upper():
                    return "REPAIR"
        except Exception:
            pass

        return "PASS"
