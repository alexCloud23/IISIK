from __future__ import annotations

from sqlalchemy.orm import Session

from shared.errors import InvalidFilterError, parse_uuid

from . import repository
from .schemas import CompetitorPriceDTO, SalesRecordDTO, SalesSummaryDTO

MAX_LIMIT = 1000


def _normalize_limit(limit: int) -> int:
    if not 1 <= limit <= MAX_LIMIT:
        raise InvalidFilterError(f"limit должен быть в диапазоне 1..{MAX_LIMIT}")
    return limit


def _normalize_product_id(product_id: str | None) -> str | None:
    if product_id is None:
        return None
    return str(parse_uuid(product_id, "product_id"))


def list_competitor_prices(
    session: Session,
    product_id: str | None = None,
    limit: int = 100,
) -> list[CompetitorPriceDTO]:
    normalized = _normalize_product_id(product_id)
    rows = repository.list_competitor_prices(
        session, normalized, _normalize_limit(limit)
    )
    return [CompetitorPriceDTO.model_validate(row) for row in rows]


def list_sales(
    session: Session,
    product_id: str | None = None,
    limit: int = 100,
) -> list[SalesRecordDTO]:
    normalized = _normalize_product_id(product_id)
    rows = repository.list_sales(session, normalized, _normalize_limit(limit))
    return [SalesRecordDTO.model_validate(row) for row in rows]


def get_sales_summary(session: Session, product_id: str) -> SalesSummaryDTO:
    normalized = str(parse_uuid(product_id, "product_id"))
    records, total_quantity, average_price = repository.sales_summary(
        session, normalized
    )
    return SalesSummaryDTO(
        product_id=normalized,
        records=records,
        total_quantity=total_quantity,
        average_unit_price=average_price,
    )
