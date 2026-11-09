from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MARKET_DATA_", extra="ignore")

    service_name: str = "market_data"
    port: int = 8003
    database_url: str = f"sqlite:///{(BASE_DIR / 'data' / 'market_data.db').as_posix()}"


settings = Settings()
