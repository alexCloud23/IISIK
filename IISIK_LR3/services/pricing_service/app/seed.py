from __future__ import annotations

from sqlalchemy import delete
from sqlalchemy.orm import Session

from fixtures.pricing import RECOMMENDATIONS

from .models import PriceRecommendation


def seed(session: Session) -> int:
    session.execute(delete(PriceRecommendation))
    session.add_all(
        [
            PriceRecommendation(
                id=item.id,
                product_id=item.product_id,
                forecast_id=item.forecast_id,
                strategy_id=item.strategy_id,
                current_price=item.current_price,
                recommended_price=item.recommended_price,
                currency=item.currency,
                reason=item.reason,
                status=item.status,
                created_at=item.created_at,
            )
            for item in RECOMMENDATIONS
        ]
    )
    session.commit()
    return len(RECOMMENDATIONS)
