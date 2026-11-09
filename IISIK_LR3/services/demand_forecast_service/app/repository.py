from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import DemandForecast


def get_forecast(session: Session, forecast_id: str) -> DemandForecast | None:
    return session.get(DemandForecast, forecast_id)


def list_forecasts(
    session: Session, product_id: str | None = None
) -> list[DemandForecast]:
    stmt = select(DemandForecast).order_by(
        DemandForecast.period_start.desc(), DemandForecast.id.desc()
    )
    if product_id is not None:
        stmt = stmt.where(DemandForecast.product_id == product_id)
    return list(session.scalars(stmt))


def latest_forecast(session: Session, product_id: str) -> DemandForecast | None:
    stmt = (
        select(DemandForecast)
        .where(DemandForecast.product_id == product_id)
        .order_by(DemandForecast.created_at.desc())
        .limit(1)
    )
    return session.scalars(stmt).first()
