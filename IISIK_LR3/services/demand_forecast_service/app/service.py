from __future__ import annotations

from sqlalchemy.orm import Session

from shared.errors import NotFoundError, parse_uuid

from . import repository
from .schemas import ForecastDTO


def get_forecast(session: Session, forecast_id: str) -> ForecastDTO:
    parsed = parse_uuid(forecast_id, "forecast_id")
    forecast = repository.get_forecast(session, str(parsed))
    if forecast is None:
        raise NotFoundError(f"Прогноз {forecast_id} не найден")
    return ForecastDTO.model_validate(forecast)


def list_forecasts(
    session: Session, product_id: str | None = None
) -> list[ForecastDTO]:
    normalized = str(parse_uuid(product_id, "product_id")) if product_id else None
    return [
        ForecastDTO.model_validate(row)
        for row in repository.list_forecasts(session, normalized)
    ]


def latest_forecast(session: Session, product_id: str) -> ForecastDTO | None:
    normalized = str(parse_uuid(product_id, "product_id"))
    forecast = repository.latest_forecast(session, normalized)
    return ForecastDTO.model_validate(forecast) if forecast else None
