from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from shared.competitive import analyze_competitor_strategy
from shared.errors import parse_uuid

from . import repository
from .models import CompetitorStrategy
from .schemas import StrategyAnalyzeDTO, StrategyDTO


def list_strategies(
    session: Session, product_id: str | None = None
) -> list[StrategyDTO]:
    normalized = str(parse_uuid(product_id, "product_id")) if product_id else None
    return [
        StrategyDTO.model_validate(row)
        for row in repository.list_strategies(session, normalized)
    ]


def analyze_strategy(session: Session, data: StrategyAnalyzeDTO) -> StrategyDTO:
    product_id = str(parse_uuid(data.product_id, "product_id"))
    strategy_type, reference_price, change_percent, probability = (
        analyze_competitor_strategy(
            data.current_price, [point.price for point in data.competitor_prices]
        )
    )
    cheapest = min(data.competitor_prices, key=lambda point: point.price)
    strategy = repository.add_strategy(
        session,
        CompetitorStrategy(
            id=str(uuid4()),
            product_id=product_id,
            competitor_name=cheapest.competitor_name,
            strategy_type=strategy_type,
            competitor_price=reference_price,
            price_change_percent=change_percent,
            estimated_probability=probability,
            created_at=datetime.utcnow(),
        ),
    )
    return StrategyDTO.model_validate(strategy)
