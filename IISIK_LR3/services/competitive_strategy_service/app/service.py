from __future__ import annotations

from sqlalchemy.orm import Session

from shared.errors import parse_uuid

from . import repository
from .schemas import StrategyDTO


def list_strategies(
    session: Session, product_id: str | None = None
) -> list[StrategyDTO]:
    normalized = str(parse_uuid(product_id, "product_id")) if product_id else None
    return [
        StrategyDTO.model_validate(row)
        for row in repository.list_strategies(session, normalized)
    ]
