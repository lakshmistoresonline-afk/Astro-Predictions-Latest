# Astrovision AI Interpretation Architecture & Provider Policy

## 1. Architectural Trust Boundary
Astrovision strictly enforces a zero-trust evidence boundary:

```
[ CLIENT ]  -- (Sends BirthInput & Topic Request e.g. "CAREER") -->
                                 │
                                 ▼
[ SERVER ]  -- (Validates Input & Executes Local Engines) --------> [ CANONICAL EVIDENCE ]
                                                                             │
                                                                             ▼
[ AI INTERPRETATION ] <--- (Non-Calculative System Prompt + Evidence) --------┘
```

1. **Server Ownership**: The server owns all evidence generation via `CanonicalEvidencePipeline`. The client **cannot** supply, override, or inject arbitrary astrological evidence JSON payloads into the AI service.
2. **Non-Calculative System Prompt**: The LLM is strictly prohibited from calculating planetary positions, houses, Nakshatras, Vargas, Dashas, Yogas, or Doshas.
3. **Immutable Server Evidence**: User prompt instructions are treated strictly as an interpretation topic query and can never alter or replace server-generated evidence facts.

## 2. Canonical AI Provider Policy
The AI architecture uses explicit provider configuration without silent, unannounced fallbacks behind the scenes:

### Configuration (`.env` & `apps/api/config.py`)
- **`AI_PROVIDER`**: Canonical provider selector (`ollama` | `openai`). Defaults to `ollama`.
- **`OLLAMA_BASE_URL`**: Base URL for local Ollama service (`http://localhost:11434`).
- **`AI_MODEL_GENERATION`**: Model name for narrative generation (`gemma4`).
- **`AI_MODEL_VALIDATION`**: Model name for evidence adherence validation (`qwen3.5`).
- **`AI_REQUEST_TIMEOUT_SECONDS`**: Explicit request timeout in seconds (`20.0`).
- **`AI_MAX_RETRIES`**: Maximum connection retry attempts (`2`).

### Provider Execution Rules
- When `AI_PROVIDER=ollama`, the service executes requests strictly against the local Ollama provider using `AI_MODEL_GENERATION` and `AI_MODEL_VALIDATION`.
- When `AI_PROVIDER=openai`, the service executes requests strictly against OpenAI using `OPENAI_API_KEY` and `OPENAI_MODEL`.
- If the configured provider is unavailable, times out, or returns empty output, the service **fails closed** and returns an explicit unavailable status (`validation_status: "UNAVAILABLE"`). It **never** silently switches providers or fabricates AI output.

## 3. Response Metadata Contract (`/api/v1/interpret-evidence`)
All AI interpretation API responses return structured provider and model metadata:
```json
{
  "domain": "CAREER",
  "interpretation": "Narrative interpretation text...",
  "provider": "ollama",
  "generation_model": "gemma4",
  "validation_model": "qwen3.5",
  "validation_status": "PASS"
}
```
