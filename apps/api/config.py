import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Astro Predictions API"
    environment: str = "development"

    # CORS Configuration
    cors_allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000,https://astrovision.io"

    # Admin Security Configuration
    admin_api_key: str = "astrovision_admin_secret_key_2026"

    # AI Provider Configuration (ollama | openai)
    ai_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ai_model_generation: str = "gemma4"
    ai_model_validation: str = "qwen3.5"
    ai_request_timeout_seconds: float = 20.0
    ai_max_retries: int = 2

    # Free Tier Governance Limits
    free_daily_charts: int = 10
    free_daily_ai_reports: int = 3
    free_daily_ai_messages: int = 20

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
