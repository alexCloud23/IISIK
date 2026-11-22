from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Protocol

import grpc

import shared.protogen
import forecast_pb2
import forecast_pb2_grpc
from fixtures.forecast import FORECASTS
from shared.errors import UpstreamUnavailableError
from shared.resilience import call_with_retry

from .config import settings
from .schemas import ForecastRefDTO


class ForecastProvider(Protocol):
    def get_forecast(self, forecast_id: str) -> ForecastRefDTO | None: ...


class MockForecastProvider:
    def __init__(self) -> None:
        self._forecasts = {item.id: item for item in FORECASTS}

    def get_forecast(self, forecast_id: str) -> ForecastRefDTO | None:
        item = self._forecasts.get(forecast_id)
        if item is None:
            return None
        return ForecastRefDTO(
            id=item.id,
            product_id=item.product_id,
            period_start=item.period_start,
            period_end=item.period_end,
            predicted_demand=item.predicted_demand,
            confidence=item.confidence,
            model_version=item.model_version,
        )


class GrpcForecastProvider:
    def __init__(self, addr: str) -> None:
        self._addr = addr
        self._channel = grpc.insecure_channel(addr)
        self._stub = forecast_pb2_grpc.ForecastServiceStub(self._channel)

    def get_forecast(self, forecast_id: str) -> ForecastRefDTO | None:
        try:
            response = call_with_retry(
                lambda: self._stub.GetForecast(
                    forecast_pb2.GetForecastRequest(id=forecast_id),
                    timeout=settings.forecast_timeout,
                ),
                label=f"{self._addr} GetForecast",
                attempts=settings.forecast_retry_attempts,
                backoff=settings.retry_backoff,
            )
        except grpc.RpcError as exc:
            if exc.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise UpstreamUnavailableError(
                f"Сервис прогнозов {self._addr} недоступен: {exc.code().name}"
            ) from exc
        if not response.HasField("forecast"):
            return None
        msg = response.forecast
        return ForecastRefDTO(
            id=msg.id,
            product_id=msg.product_id,
            period_start=datetime.fromisoformat(msg.period_start),
            period_end=datetime.fromisoformat(msg.period_end),
            predicted_demand=Decimal(msg.predicted_demand),
            confidence=(
                Decimal(msg.confidence) if msg.HasField("confidence") else None
            ),
            model_version=msg.model_version,
        )


def _build_default_provider() -> ForecastProvider:
    if settings.forecast_provider.lower() == "grpc":
        return GrpcForecastProvider(settings.forecast_grpc_addr)
    return MockForecastProvider()


default_forecast_provider: ForecastProvider = _build_default_provider()


def get_forecast_provider() -> ForecastProvider:
    return default_forecast_provider
