"""Configuration management for the backend API."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str

    # API
    api_port: int = 8000
    api_host: str = "0.0.0.0"

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Environment
    environment: str = "development"

    # Logging
    log_level: str = "INFO"

    # JWT Authentication (Module 2)
    jwt_secret: str = "change-me-in-production-use-at-least-32-chars"
    jwt_algorithm: str = "HS256"
    jwt_expiration_days: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
