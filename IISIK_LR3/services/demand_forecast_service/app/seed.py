from __future__ import annotations

from sqlalchemy import delete
from sqlalchemy.orm import Session

from fixtures.forecast import FORECASTS

from .models import DemandForecast


def seed(session: Session) -> int:
    session.execute(delete(DemandForecast))
    session.add_all(
        [
            DemandForecast(
                id=item.id,
                product_id=item.product_id,
                period_start=item.period_start,
                period_end=item.period_end,
                predicted_demand=item.predicted_demand,
                confidence=item.confidence,
                model_version=item.model_version,
                created_at=item.created_at,
            )
            for item in FORECASTS
        ]
    )
    session.commit()
    return len(FORECASTS)
