"""
Luminara Backend — Core Configuration
Reads and validates all environment variables using Pydantic Settings.
Import `settings` anywhere in the app — never read os.environ directly.
"""

from functools import lru_cache
from typing import List, Literal

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────
    app_name: str = "Luminara"
    app_version: str = "1.0.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    log_level: str = "INFO"

    # ── Server ───────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    # ── Database ─────────────────────────────────────────────
    database_url: str = Field(..., description="Async PostgreSQL connection string")
    database_url_sync: str = Field(..., description="Sync connection string for Alembic")

    # ── Supabase ─────────────────────────────────────────────
    supabase_url: str = Field(..., description="Supabase project URL")
    supabase_anon_key: str = Field(..., description="Supabase anonymous key")
    supabase_service_role_key: str = Field(..., description="Supabase service role key (server-side only)")

    # ── JWT Auth ─────────────────────────────────────────────
    jwt_secret_key: str = Field(..., min_length=32, description="JWT signing secret")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    # ── Security APIs ─────────────────────────────────────────
    virustotal_api_key: str = Field(..., description="VirusTotal API key")
    google_safe_browsing_api_key: str = Field(..., description="Google Safe Browsing API key")

    # ── AI Models ─────────────────────────────────────────────
    phishing_model_name: str = "ealvaradob/bert-finetuned-phishing"
    phishing_url_model_name: str = "pirocheto/phishing-url-detection"
    deepfake_audio_model_path: str = "ai_models/deepfake/audio/aasist_weights.pt"
    deepfake_video_model_path: str = "ai_models/deepfake/video/genconvit_weights.pt"
    hf_home: str = "./model_cache"
    torch_home: str = "./model_cache/torch"

    # ── File Upload ───────────────────────────────────────────
    max_upload_size_mb: int = 50
    allowed_audio_types: str = "audio/wav,audio/mp3,audio/mpeg,audio/ogg,audio/flac"
    allowed_video_types: str = "video/mp4,video/avi,video/quicktime,video/x-msvideo"
    allowed_image_types: str = "image/png,image/jpeg,image/webp"

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def allowed_audio_list(self) -> List[str]:
        return [t.strip() for t in self.allowed_audio_types.split(",")]

    @property
    def allowed_video_list(self) -> List[str]:
        return [t.strip() for t in self.allowed_video_types.split(",")]

    # ── Rate Limiting ─────────────────────────────────────────
    rate_limit_per_minute: int = 30
    rate_limit_analysis: int = 10
    redis_url: str = ""           # Empty = use in-memory (dev only)

    # ── Notifications ─────────────────────────────────────────
    fcm_server_key: str = ""

    # ── i18n ─────────────────────────────────────────────────
    default_language: str = "en"
    supported_languages: str = "en,ta,hi"

    @property
    def supported_language_list(self) -> List[str]:
        return [lang.strip() for lang in self.supported_languages.split(",")]

    # ── Derived flags ─────────────────────────────────────────
    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper = v.upper()
        if upper not in valid:
            raise ValueError(f"log_level must be one of {valid}")
        return upper


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    Use this function to get settings anywhere in the app:

        from app.core.config import get_settings
        settings = get_settings()
    """
    return Settings()


# Convenience singleton — import directly for most use cases
settings = get_settings()
