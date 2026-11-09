from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import PriceRecommendation

SORT_FIELDS: dict[str, object] = {
    "created": PriceRecommendation.created_at,
    "price": PriceRecommendation.recommended_price,
}


def get_recommendation(
    session: Session, recommendation_id: str
) -> PriceRecommendation | None:
    return session.get(PriceRecommendation, recommendation_id)


def add_recommendation(
    session: Session, recommendation: PriceRecommendation
) -> PriceRecommendation:
    session.add(recommendation)
    session.commit()
    session.refresh(recommendation)
    return recommendation


def list_recommendations(
    session: Session,
    product_id: str | None = None,
    status: str | None = None,
    sort_column: object = PriceRecommendation.created_at,
    descending: bool = True,
) -> list[PriceRecommendation]:
    stmt = select(PriceRecommendation)
    if product_id is not None:
        stmt = stmt.where(PriceRecommendation.product_id == product_id)
    if status is not None:
        stmt = stmt.where(PriceRecommendation.status == status)
    stmt = stmt.order_by(
        sort_column.desc() if descending else sort_column.asc(), PriceRecommendation.id
    )
    return list(session.scalars(stmt))


def status_counts(session: Session) -> dict[str, int]:
    stmt = select(
        PriceRecommendation.status, func.count(PriceRecommendation.id)
    ).group_by(PriceRecommendation.status)
    counts = {status: int(total) for status, total in session.execute(stmt)}
    return {
        "total": sum(counts.values()),
        "new": counts.get("NEW", 0),
        "accepted": counts.get("ACCEPTED", 0),
        "rejected": counts.get("REJECTED", 0),
    }
