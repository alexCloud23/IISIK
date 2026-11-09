from __future__ import annotations

from typing import Protocol

from fixtures.forecast import FORECASTS

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


default_forecast_provider: ForecastProvider = MockForecastProvider()


def get_forecast_provider() -> ForecastProvider:
    return default_forecast_provider
