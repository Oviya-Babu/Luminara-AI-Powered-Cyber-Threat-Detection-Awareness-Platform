"""
Luminara — Core Configuration
Reads all settings from the .env file.
Import 'settings' anywhere you need a config value.
"""

from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "Luminara"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    # Database
    database_url: str = Field(..., description="Async PostgreSQL URL")
    database_url_sync: str = Field(..., description="Sync URL for Alembic")

    # Supabase
    supabase_url: str = Field(..., description="Supabase project URL")
    supabase_anon_key: str = Field(..., description="Supabase anon key")
    supabase_service_role_key: str = Field(..., description="Supabase service role")

    # JWT
    jwt_secret_key: str = Field(..., min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    # Upload
    max_upload_size_mb: int = 50

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    # Rate limiting
    rate_limit_per_minute: int = 30
    rate_limit_analysis: int = 10

    # AI Models
    phishing_model_name: str = "ealvaradob/bert-finetuned-phishing"
    phishing_url_model_name: str = "pirocheto/phishing-url-detection"

    # Language
    default_language: str = "en"
    supported_languages: str = "en,ta,hi"

    @property
    def supported_language_list(self) -> List[str]:
        return [x.strip() for x in self.supported_languages.split(",")]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Use this import everywhere:
# from app.core.config import settings
settings = get_settings()