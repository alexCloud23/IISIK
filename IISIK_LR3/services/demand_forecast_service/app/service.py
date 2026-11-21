from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from shared.errors import NotFoundError, parse_uuid
from shared.forecasting import (
    MODEL_VERSION,
    compute_demand_forecast,
    validate_period_days,
)

from . import repository
from .models import DemandForecast
from .schemas import ForecastDTO, ForecastGenerateDTO


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


def generate_forecast(session: Session, data: ForecastGenerateDTO) -> ForecastDTO:
    product_id = str(parse_uuid(data.product_id, "product_id"))
    period_days = validate_period_days(data.period_days)
    predicted, confidence = compute_demand_forecast(
        [(point.sold_at, point.quantity) for point in data.sales], period_days
    )
    period_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    forecast = repository.add_forecast(
        session,
        DemandForecast(
            id=str(uuid4()),
            product_id=product_id,
            period_start=period_start,
            period_end=period_start + timedelta(days=period_days),
            predicted_demand=predicted,
            confidence=confidence,
            model_version=MODEL_VERSION,
            created_at=datetime.utcnow(),
        ),
    )
    return ForecastDTO.model_validate(forecast)
