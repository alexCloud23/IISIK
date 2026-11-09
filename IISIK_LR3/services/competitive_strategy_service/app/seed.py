from __future__ import annotations

from sqlalchemy import delete
from sqlalchemy.orm import Session

from fixtures.strategy import STRATEGIES

from .models import CompetitorStrategy


def seed(session: Session) -> int:
    session.execute(delete(CompetitorStrategy))
    session.add_all(
        [
            CompetitorStrategy(
                id=item.id,
                product_id=item.product_id,
                competitor_name=item.competitor_name,
                strategy_type=item.strategy_type,
                competitor_price=item.competitor_price,
                price_change_percent=item.price_change_percent,
                estimated_probability=item.estimated_probability,
                created_at=item.created_at,
            )
            for item in STRATEGIES
        ]
    )
    session.commit()
    return len(STRATEGIES)
