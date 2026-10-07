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
    Validates environment secrets and database configuration.
    Refuses to start in production if ADMIN_API_KEY or JWT_SECRET_KEY is missing or set to default secret,
    or if DATABASE_URL is missing or uses local SQLite.
    """
    env = os.environ.get("ENVIRONMENT", settings.environment).lower().strip()

    admin_key = os.environ.get("ADMIN_API_KEY", settings.admin_api_key)
    jwt_key = os.environ.get("JWT_SECRET_KEY", settings.jwt_secret_key)
    db_url = os.environ.get("DATABASE_URL", settings.database_url)

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
                "Production deployment requires a persistent PostgreSQL database connection string (e.g. postgresql://user:pass@host:5432/dbname)."
            )
        settings.admin_api_key = admin_key.strip()
        settings.jwt_secret_key = jwt_key.strip()
        settings.database_url = db_url.strip()
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
