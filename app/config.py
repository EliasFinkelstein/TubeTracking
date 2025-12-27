from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    tfl_base_url: str = Field("https://api.tfl.gov.uk", env="TFL_BASE_URL")
    tfl_app_id: str | None = Field(default=None, env="TFL_APP_ID")
    tfl_app_key: str | None = Field(default=None, env="TFL_APP_KEY")
    request_timeout_seconds: float = Field(10.0, env="REQUEST_TIMEOUT_SECONDS")


@lru_cache
def get_settings() -> Settings:
    return Settings()
