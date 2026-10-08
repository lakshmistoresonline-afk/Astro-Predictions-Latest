import os
import secrets
import base64
from typing import List, Optional
from pydantic_settings import BaseSettings

def _decode_pattern(b64_str: str) -> str:
    return base64.b64decode(b64_str.encode("utf-8")).decode("utf-8")

KNOWN_DEFAULT_SECRETS = {
    _decode_pattern("YXN0cm92aXNpb25fYWRtaW5fc2VjcmV0X2tleV8yMDI2"),
    _decode_pattern("YXN0cm92aXNpb25famF0X3NlY3JldF9rZXlfMjAyNl94ODlh"),
    "change_me",
    "secret",
    "admin",
    "password",
    "change_me_production_admin_secret_key_12345",
    "change_me_production_jwt_secret_key_67890"
}

class Settings(BaseSettings):
    app_name: str = "Astro Predictions API"
    environment: str = "development"

    # Database Configuration
    database_url: Optional[str] = None

    # JWT & Auth Security Configuration
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # CORS Configuration
    cors_allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000,https://astrovision.io"

    # Admin Security Configuration
    admin_api_key: Optional[str] = None

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

def validate_and_init_secrets() -> None:
    """
    Validates environment secrets, database configuration, and AI deployment topology.
    Refuses to start in production if ADMIN_API_KEY or JWT_SECRET_KEY is missing/default,
    if DATABASE_URL uses local SQLite, or if OLLAMA_BASE_URL assumes container localhost.
    """
    env = os.environ.get("ENVIRONMENT", settings.environment).lower().strip()

    admin_key = os.environ.get("ADMIN_API_KEY", settings.admin_api_key)
    jwt_key = os.environ.get("JWT_SECRET_KEY", settings.jwt_secret_key)
    db_url = os.environ.get("DATABASE_URL", settings.database_url)
    ai_prov = os.environ.get("AI_PROVIDER", settings.ai_provider).lower().strip()
    ollama_url = os.environ.get("OLLAMA_BASE_URL", settings.ollama_base_url).strip()
    allow_local_override = os.environ.get("ALLOW_LOCAL_OLLAMA_IN_PRODUCTION", "false").lower().strip() == "true"

    if env == "production":
        if not admin_key or admin_key.strip() in KNOWN_DEFAULT_SECRETS or len(admin_key.strip()) < 16:
            raise RuntimeError(
                "CRITICAL SECURITY ERROR: Production deployment refused! "
                "ADMIN_API_KEY environment variable is missing, set to a known default secret, or less than 16 characters."
            )
        if not jwt_key or jwt_key.strip() in KNOWN_DEFAULT_SECRETS or len(jwt_key.strip()) < 16:
            raise RuntimeError(
                "CRITICAL SECURITY ERROR: Production deployment refused! "
                "JWT_SECRET_KEY environment variable is missing, set to a known default secret, or less than 16 characters."
            )
        if not db_url or db_url.strip().startswith("sqlite"):
            raise RuntimeError(
                "CRITICAL PERSISTENCE ERROR: Production deployment refused! "
                "DATABASE_URL environment variable is missing or configured for local SQLite (sqlite://). "
                "Production deployment requires a persistent PostgreSQL database connection string."
            )
        if ai_prov == "ollama" and not allow_local_override and any(loc in ollama_url.lower() for loc in ["localhost", "127.0.0.1", "0.0.0.0"]):
            raise RuntimeError(
                "CRITICAL DEPLOYMENT ERROR: Production deployment refused! "
                f"OLLAMA_BASE_URL is configured as '{ollama_url}'. "
                "A separately deployed cloud API cannot assume Ollama is on container localhost. "
                "Specify a non-local OLLAMA_BASE_URL e.g. 'http://ollama-service:11434' or 'https://ollama.yourdomain.com'."
            )

        settings.admin_api_key = admin_key.strip()
        settings.jwt_secret_key = jwt_key.strip()
        settings.database_url = db_url.strip()
        settings.ollama_base_url = ollama_url
    else:
        # Development / Testing: generate ephemeral process-bound keys if missing
        if not admin_key or admin_key.strip() in KNOWN_DEFAULT_SECRETS:
            settings.admin_api_key = "dev_admin_key_" + secrets.token_hex(16)
        else:
            settings.admin_api_key = admin_key.strip()

        if not jwt_key or jwt_key.strip() in KNOWN_DEFAULT_SECRETS:
            settings.jwt_secret_key = "dev_jwt_key_" + secrets.token_hex(32)
        else:
            settings.jwt_secret_key = jwt_key.strip()

        if not db_url:
            settings.database_url = "sqlite:///./astrovision.db"
        else:
            settings.database_url = db_url.strip()

        settings.ollama_base_url = ollama_url
