from __future__ import annotations

from sqlalchemy import delete
from sqlalchemy.orm import Session

from fixtures.market_data import COMPETITOR_PRICES, SALES

from .models import CompetitorPrice, SalesRecord


def seed(session: Session) -> int:
    session.execute(delete(SalesRecord))
    session.execute(delete(CompetitorPrice))

    session.add_all(
        [
            CompetitorPrice(
                id=item.id,
                product_id=item.product_id,
                competitor_name=item.competitor_name,
                price=item.price,
                currency=item.currency,
                source=item.source,
                observed_at=item.observed_at,
            )
            for item in COMPETITOR_PRICES
        ]
    )
    session.add_all(
        [
            SalesRecord(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                currency=item.currency,
                sold_at=item.sold_at,
            )
            for item in SALES
        ]
    )
    session.commit()
    return len(COMPETITOR_PRICES) + len(SALES)
