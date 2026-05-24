from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "smsbridge"
    environment: str = "local"
    database_url: str = "postgresql+psycopg://smsbridge:smsbridge@postgres:5432/smsbridge"
    redis_url: str = "redis://redis:6379/0"
    secret_key: str = "change-this-secret"
    access_token_minutes: int = 60
    refresh_token_minutes: int = 60 * 24 * 14
    cors_origins: str = "http://localhost:3000"
    mock_success_rate: float = 0.85
    mock_sms_delay_seconds: int = 10
    mock_order_timeout_seconds: int = 120
    rate_limit_per_minute: int = 120

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

