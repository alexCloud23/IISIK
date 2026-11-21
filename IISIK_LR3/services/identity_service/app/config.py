from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="IDENTITY_", extra="ignore")

    service_name: str = "identity"
    port: int = 8001
    database_url: str = f"sqlite:///{(BASE_DIR / 'data' / 'identity.db').as_posix()}"

    jwt_secret: str = "dev-secret-change-me"
    jwt_ttl_seconds: int = 3600
    session_ttl_seconds: int = 1800
    redis_url: str = "redis://127.0.0.1:6379/0"


settings = Settings()
