from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GATEWAY_", extra="ignore")

    port: int = 8000
    client_mode: str = "mock"

    product_service_url: str = "http://127.0.0.1:8002"
    market_data_service_url: str = "http://127.0.0.1:8003"
    forecast_service_url: str = "http://127.0.0.1:8004"
    strategy_service_url: str = "http://127.0.0.1:8005"
    pricing_service_url: str = "http://127.0.0.1:8006"
    analytics_service_url: str = "http://127.0.0.1:8007"
    notification_service_url: str = "http://127.0.0.1:8008"

    request_timeout: float = 2.0


settings = Settings()
