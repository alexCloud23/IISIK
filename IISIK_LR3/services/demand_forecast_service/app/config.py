from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DEMAND_FORECAST_", extra="ignore")

    service_name: str = "demand_forecast"
    port: int = 8004
    database_url: str = (
        f"sqlite:///{(BASE_DIR / 'data' / 'demand_forecast.db').as_posix()}"
    )


settings = Settings()
