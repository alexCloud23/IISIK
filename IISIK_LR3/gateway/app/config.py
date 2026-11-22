from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GATEWAY_", extra="ignore")

    port: int = 8000
    client_mode: str = "mock"

    identity_service_url: str = "http://127.0.0.1:8001"
    product_service_url: str = "http://127.0.0.1:8002"
    market_data_service_url: str = "http://127.0.0.1:8003"
    forecast_service_url: str = "http://127.0.0.1:8004"
    strategy_service_url: str = "http://127.0.0.1:8005"
    pricing_service_url: str = "http://127.0.0.1:8006"
    analytics_service_url: str = "http://127.0.0.1:8007"
    notification_service_url: str = "http://127.0.0.1:8008"

    identity_grpc_addr: str = "127.0.0.1:50051"
    product_grpc_addr: str = "127.0.0.1:50052"
    market_data_grpc_addr: str = "127.0.0.1:50053"
    forecast_grpc_addr: str = "127.0.0.1:50054"
    strategy_grpc_addr: str = "127.0.0.1:50055"
    pricing_grpc_addr: str = "127.0.0.1:50056"
    analytics_grpc_addr: str = "127.0.0.1:50057"
    notification_grpc_addr: str = "127.0.0.1:50058"

    events_backend: str = "kafka"
    kafka_bootstrap_servers: str = "127.0.0.1:9092"

    request_timeout: float = 2.0


settings = Settings()
