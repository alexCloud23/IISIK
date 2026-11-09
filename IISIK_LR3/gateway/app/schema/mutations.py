from __future__ import annotations

from decimal import Decimal

import strawberry
from strawberry.types import Info

from shared.errors import InvalidOperationError, NotFoundError

from ..clients.base import UNSET
from ..context import get_clients
from ..resolvers import translate_errors
from .types import (
    NotificationType,
    PriceRecommendationType,
    ProductType,
    RecommendationDecision,
)


@strawberry.input
class ProductInput:
    name: str
    description: str | None = None
    category: str
    price: float
    currency: str = "BYN"


@strawberry.input
class ProductUpdateInput:
    price: float | None = UNSET
    description: str | None = UNSET
    is_active: bool | None = UNSET


def _money_text(value: Decimal) -> str:
    return f"{value:.2f}"


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product(
        self, info: Info, input: ProductInput
    ) -> ProductType:
        with translate_errors():
            dto = get_clients(info).product.create_product(
                name=input.name,
                description=input.description,
                category=input.category,
                base_price=Decimal(str(input.price)),
                currency=input.currency,
            )
        return ProductType.from_dto(dto)

    @strawberry.mutation
    def update_product(
        self, info: Info, id: strawberry.ID, input: ProductUpdateInput
    ) -> ProductType:
        with translate_errors():
            dto = get_clients(info).product.update_product(
                str(id),
                base_price=(
                    Decimal(str(input.price))
                    if input.price is not UNSET
                    else UNSET
                ),
                description=(
                    input.description
                    if input.description is not UNSET
                    else UNSET
                ),
                is_active=(
                    input.is_active if input.is_active is not UNSET else UNSET
                ),
            )
        return ProductType.from_dto(dto)

    @strawberry.mutation
    def generate_price_recommendation(
        self, info: Info, product_id: strawberry.ID
    ) -> PriceRecommendationType:
        with translate_errors():
            clients = get_clients(info)
            normalized = str(product_id)

            product = clients.product.get_product(normalized)
            if product is None:
                raise NotFoundError(f"Товар {product_id} не найден")
            if not product.is_active:
                raise InvalidOperationError(
                    "Нельзя формировать рекомендацию для неактивного товара"
                )

            forecasts = clients.forecast.list_forecasts(normalized)
            if not forecasts:
                raise InvalidOperationError(
                    f"Нет прогноза спроса для товара {product_id}"
                )
            forecast = forecasts[0]

            strategies = clients.strategy.list_strategies(normalized)
            strategy = strategies[0] if strategies else None

            dto = clients.recommendation.create_recommendation(
                product_id=normalized,
                forecast_id=forecast.id,
                current_price=product.base_price,
                strategy_type=strategy.strategy_type if strategy else None,
                competitor_price=strategy.competitor_price if strategy else None,
                strategy_id=strategy.id if strategy else None,
            )
            clients.notification.create_notification(
                notification_type="RECOMMENDATION_CREATED",
                title="Новая ценовая рекомендация",
                message=(
                    f"Сформирована рекомендация по товару «{product.name}»: "
                    f"{_money_text(dto.recommended_price)} BYN вместо "
                    f"{_money_text(dto.current_price)} BYN."
                ),
                related_entity_id=dto.id,
            )
        return PriceRecommendationType.from_dto(dto)

    @strawberry.mutation
    def decide_recommendation(
        self,
        info: Info,
        id: strawberry.ID,
        decision: RecommendationDecision,
    ) -> PriceRecommendationType:
        with translate_errors():
            clients = get_clients(info)
            dto = clients.recommendation.decide_recommendation(str(id), decision.value)

            product = clients.product.get_product(dto.product_id)
            product_text = (
                f"по товару «{product.name}»"
                if product
                else f"по товару {dto.product_id}"
            )
            accepted = decision == RecommendationDecision.ACCEPTED
            clients.notification.create_notification(
                notification_type=(
                    "DECISION_ACCEPTED" if accepted else "RECOMMENDATION_REJECTED"
                ),
                title=(
                    "Ценовое решение принято"
                    if accepted
                    else "Ценовое решение отклонено"
                ),
                message=(
                    f"Рекомендация {product_text} "
                    f"{'принята' if accepted else 'отклонена'}: "
                    f"цена {_money_text(dto.recommended_price)} BYN."
                ),
                related_entity_id=dto.id,
            )
        return PriceRecommendationType.from_dto(dto)

    @strawberry.mutation
    def mark_notification_read(
        self, info: Info, id: strawberry.ID
    ) -> NotificationType:
        with translate_errors():
            dto = get_clients(info).notification.mark_notification_read(str(id))
        return NotificationType.from_dto(dto)

    @strawberry.mutation
    def mark_all_notifications_read(self, info: Info) -> int:
        with translate_errors():
            return get_clients(info).notification.mark_all_notifications_read()
