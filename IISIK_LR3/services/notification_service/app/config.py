from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NOTIFICATION_", extra="ignore")

    service_name: str = "notification"
    port: int = 8008
    database_url: str = f"sqlite:///{(BASE_DIR / 'data' / 'notification.db').as_posix()}"


settings = Settings()
