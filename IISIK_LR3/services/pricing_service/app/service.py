from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from shared.errors import (
    InvalidFilterError,
    InvalidInputError,
    InvalidOperationError,
    NotFoundError,
    parse_uuid,
)
from shared.pricing_rules import (
    STRATEGY_TYPES,
    VALID_DECISIONS,
    compute_recommendation,
    round_money,
)
from shared.validation import validate_positive_price

from . import repository
from .models import PriceRecommendation
from .providers import ForecastProvider, default_forecast_provider
from .schemas import (
    RecommendationCreateDTO,
    RecommendationDTO,
    RecommendationWithForecastDTO,
)

VALID_SORT_FIELDS = ("created", "price")
VALID_ORDERS = ("asc", "desc")


def get_recommendation(session: Session, recommendation_id: str) -> RecommendationDTO:
    parsed = parse_uuid(recommendation_id, "recommendation_id")
    recommendation = repository.get_recommendation(session, str(parsed))
    if recommendation is None:
        raise NotFoundError(f"Рекомендация {recommendation_id} не найдена")
    return RecommendationDTO.model_validate(recommendation)


def list_recommendations(
    session: Session,
    product_id: str | None = None,
    status: str | None = None,
    sort: str = "created",
    order: str = "desc",
) -> list[RecommendationDTO]:
    if sort not in VALID_SORT_FIELDS:
        raise InvalidFilterError(
            f"Неизвестное поле сортировки: {sort!r}; "
            f"допустимо: {', '.join(VALID_SORT_FIELDS)}"
        )
    if order not in VALID_ORDERS:
        raise InvalidFilterError(
            f"Неизвестное направление сортировки: {order!r}; "
            f"допустимо: {', '.join(VALID_ORDERS)}"
        )
    normalized = str(parse_uuid(product_id, "product_id")) if product_id else None
    return [
        RecommendationDTO.model_validate(row)
        for row in repository.list_recommendations(
            session,
            normalized,
            status,
            sort_column=repository.SORT_FIELDS[sort],
            descending=order == "desc",
        )
    ]


def recommendations_summary(session: Session) -> dict[str, int]:
    return repository.status_counts(session)


def create_recommendation(
    session: Session,
    data: RecommendationCreateDTO,
    provider: ForecastProvider | None = None,
) -> RecommendationDTO:
    provider = provider or default_forecast_provider
    product_id = parse_uuid(data.product_id, "product_id")
    forecast_id = parse_uuid(data.forecast_id, "forecast_id")
    strategy_id = (
        str(parse_uuid(data.strategy_id, "strategy_id"))
        if data.strategy_id
        else None
    )
    current_price = validate_positive_price(data.current_price, "current_price")

    strategy_type = data.strategy_type
    competitor_price = data.competitor_price
    if strategy_type is not None:
        if strategy_type not in STRATEGY_TYPES:
            raise InvalidInputError(f"Неизвестный тип стратегии: {strategy_type}")
        if competitor_price is None:
            raise InvalidInputError(
                "Для стратегии требуется цена конкурента (competitor_price)"
            )
        validate_positive_price(competitor_price, "competitor_price")

    forecast_ref = provider.get_forecast(str(forecast_id))
    if forecast_ref is None:
        raise NotFoundError(f"Прогноз спроса {data.forecast_id} не найден")

    recommended_price, reason = compute_recommendation(
        current_price, strategy_type, competitor_price, forecast_ref.predicted_demand
    )

    recommendation = repository.add_recommendation(
        session,
        PriceRecommendation(
            id=str(uuid4()),
            product_id=str(product_id),
            forecast_id=str(forecast_id),
            strategy_id=strategy_id,
            current_price=round_money(current_price),
            recommended_price=recommended_price,
            currency="BYN",
            reason=reason,
            status="NEW",
            created_at=datetime.utcnow(),
        ),
    )
    return RecommendationDTO.model_validate(recommendation)


def decide_recommendation(
    session: Session, recommendation_id: str, decision: str
) -> RecommendationDTO:
    if decision not in VALID_DECISIONS:
        raise InvalidInputError(
            f"Неизвестное решение: {decision!r}; допустимо: {', '.join(VALID_DECISIONS)}"
        )
    parsed = parse_uuid(recommendation_id, "recommendation_id")
    recommendation = repository.get_recommendation(session, str(parsed))
    if recommendation is None:
        raise NotFoundError(f"Рекомендация {recommendation_id} не найдена")
    if recommendation.status != "NEW":
        raise InvalidOperationError("Решение по рекомендации уже принято")

    recommendation.status = decision
    session.commit()
    session.refresh(recommendation)
    return RecommendationDTO.model_validate(recommendation)


def get_recommendation_with_forecast(
    session: Session,
    recommendation_id: str,
    provider: ForecastProvider | None = None,
) -> RecommendationWithForecastDTO:
    provider = provider or default_forecast_provider
    parsed = parse_uuid(recommendation_id, "recommendation_id")
    recommendation = repository.get_recommendation(session, str(parsed))
    if recommendation is None:
        raise NotFoundError(f"Рекомендация {recommendation_id} не найдена")

    base = RecommendationDTO.model_validate(recommendation)
    forecast = provider.get_forecast(recommendation.forecast_id)
    return RecommendationWithForecastDTO(**base.model_dump(), forecast=forecast)
