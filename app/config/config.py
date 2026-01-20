from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434/v1", description="Base URL for Ollama API"
    )
    MODEL_NAME: str = Field(..., description="Name of the model to use")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields in .env that aren't defined
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    This ensures settings are only loaded once during the application lifecycle.
    """
    return Settings()
