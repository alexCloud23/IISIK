from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PRICING_", extra="ignore")

    service_name: str = "pricing"
    port: int = 8006
    grpc_port: int = 50056
    forecast_provider: str = "grpc"
    forecast_grpc_addr: str = "127.0.0.1:50054"
    database_url: str = f"sqlite:///{(BASE_DIR / 'data' / 'pricing.db').as_posix()}"


settings = Settings()
