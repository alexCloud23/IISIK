from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import CompetitorPrice, SalesRecord


def list_competitor_prices(
    session: Session,
    product_id: str | None = None,
    limit: int = 100,
) -> list[CompetitorPrice]:
    stmt = select(CompetitorPrice).order_by(CompetitorPrice.observed_at.desc())
    if product_id is not None:
        stmt = stmt.where(CompetitorPrice.product_id == product_id)
    stmt = stmt.limit(limit)
    return list(session.scalars(stmt))


def list_sales(
    session: Session,
    product_id: str | None = None,
    limit: int = 100,
) -> list[SalesRecord]:
    stmt = select(SalesRecord).order_by(SalesRecord.sold_at.desc())
    if product_id is not None:
        stmt = stmt.where(SalesRecord.product_id == product_id)
    stmt = stmt.limit(limit)
    return list(session.scalars(stmt))


def sales_summary(session: Session, product_id: str) -> tuple[int, int, Decimal]:
    stmt = select(
        func.count(SalesRecord.id),
        func.coalesce(func.sum(SalesRecord.quantity), 0),
        func.coalesce(func.avg(SalesRecord.unit_price), 0),
    ).where(SalesRecord.product_id == product_id)
    records, total_quantity, average_price = session.execute(stmt).one()
    return int(records), int(total_quantity), Decimal(str(average_price))
