from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import CompetitorStrategy


def list_strategies(
    session: Session, product_id: str | None = None
) -> list[CompetitorStrategy]:
    stmt = select(CompetitorStrategy).order_by(
        CompetitorStrategy.created_at.desc(), CompetitorStrategy.id.desc()
    )
    if product_id is not None:
        stmt = stmt.where(CompetitorStrategy.product_id == product_id)
    return list(session.scalars(stmt))
