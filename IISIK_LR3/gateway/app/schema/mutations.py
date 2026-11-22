from __future__ import annotations

from decimal import Decimal

import strawberry
from strawberry.types import Info

from shared.errors import DomainError, InvalidInputError, InvalidOperationError, NotFoundError

from ..clients.base import UNSET
from ..context import get_clients, require_role, require_user
from ..resolvers import translate_errors
from .types import (
    AnalyticsResultType,
    AuthPayloadType,
    CompetitorStrategyType,
    DemandForecastType,
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


def _notify(info: Info, clients, **kwargs) -> None:
    try:
        publisher = (
            info.context.get("publisher")
            if isinstance(info.context, dict)
            else None
        )
        if publisher is not None:
            try:
                publisher.publish(kwargs)
                return
            except Exception:
                pass
        clients.notification.create_notification(**kwargs)
    except DomainError:
        pass


@strawberry.type
class Mutation:
    @strawberry.mutation
    def login(self, info: Info, email: str, password: str) -> AuthPayloadType:
        with translate_errors():
            payload = get_clients(info).auth.login(email, password)
        return AuthPayloadType.from_dto(payload)

    @strawberry.mutation
    def register(
        self, info: Info, email: str, password: str, full_name: str
    ) -> AuthPayloadType:
        with translate_errors():
            payload = get_clients(info).auth.register(email, password, full_name)
        return AuthPayloadType.from_dto(payload)

    @strawberry.mutation
    def logout(self, info: Info) -> bool:
        with translate_errors():
            require_user(info)
            token = info.context.get("token")
            if token:
                get_clients(info).auth.logout(token)
        return True

    @strawberry.mutation
    def create_product(
        self, info: Info, input: ProductInput
    ) -> ProductType:
        with translate_errors():
            require_role(info, "PRICING_MANAGER")
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
            require_role(info, "PRICING_MANAGER")
            if input.price is None:
                raise InvalidInputError("Поле price не может быть пустым")
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
            require_role(info, "PRICING_MANAGER")
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
            _notify(
                info, clients,
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
            require_role(info, "PRICING_MANAGER")
            clients = get_clients(info)
            dto = clients.recommendation.decide_recommendation(str(id), decision.value)

            accepted = decision == RecommendationDecision.ACCEPTED
            product = clients.product.get_product(dto.product_id)
            if accepted:
                if product is None:
                    raise NotFoundError(f"Товар {dto.product_id} не найден")
                clients.product.update_product(
                    dto.product_id, base_price=dto.recommended_price
                )
            product_text = (
                f"по товару «{product.name}»"
                if product
                else f"по товару {dto.product_id}"
            )
            _notify(
                info, clients,
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
    def generate_demand_forecast(
        self, info: Info, product_id: strawberry.ID, period_days: int = 7
    ) -> DemandForecastType:
        with translate_errors():
            require_role(info, "ANALYST")
            clients = get_clients(info)
            normalized = str(product_id)

            product = clients.product.get_product(normalized)
            if product is None:
                raise NotFoundError(f"Товар {product_id} не найден")

            sales = clients.market_data.list_sales(normalized)
            dto = clients.forecast.generate_forecast(
                product_id=normalized, period_days=period_days, sales=sales
            )
            _notify(
                info, clients,
                notification_type="FORECAST_READY",
                title="Прогноз спроса готов",
                message=(
                    f"Сформирован прогноз спроса по товару «{product.name}» "
                    f"на {period_days} дн.: {dto.predicted_demand} ед."
                ),
                related_entity_id=dto.id,
            )
        return DemandForecastType.from_dto(dto)

    @strawberry.mutation
    def analyze_competitor_strategy(
        self, info: Info, product_id: strawberry.ID
    ) -> CompetitorStrategyType:
        with translate_errors():
            require_role(info, "ANALYST")
            clients = get_clients(info)
            normalized = str(product_id)

            product = clients.product.get_product(normalized)
            if product is None:
                raise NotFoundError(f"Товар {product_id} не найден")

            competitor_prices = clients.market_data.list_competitor_prices(normalized)
            dto = clients.strategy.analyze_strategy(
                product_id=normalized,
                current_price=product.base_price,
                competitor_prices=competitor_prices,
            )
            _notify(
                info, clients,
                notification_type="STRATEGY_ANALYZED",
                title="Стратегия конкурентов проанализирована",
                message=(
                    f"По товару «{product.name}» определена стратегия "
                    f"{dto.strategy_type} (цена конкурента "
                    f"{_money_text(dto.competitor_price)} BYN)."
                ),
                related_entity_id=dto.id,
            )
        return CompetitorStrategyType.from_dto(dto)

    @strawberry.mutation
    def run_analytics(
        self, info: Info, product_id: strawberry.ID
    ) -> AnalyticsResultType:
        with translate_errors():
            require_role(info, "ANALYST")
            clients = get_clients(info)
            normalized = str(product_id)

            product = clients.product.get_product(normalized)
            if product is None:
                raise NotFoundError(f"Товар {product_id} не найден")

            summary = clients.market_data.sales_summary(normalized)
            forecasts = clients.forecast.list_forecasts(normalized)
            recommendations = clients.recommendation.list_recommendations(normalized)
            latest = recommendations[0] if recommendations else None

            dto = clients.analytics.run_analysis(
                product_id=normalized,
                analysis_type="SALES_SUMMARY",
                summary=summary,
                predicted_demand=(
                    forecasts[0].predicted_demand if forecasts else None
                ),
                current_price=latest.current_price if latest else None,
                recommended_price=latest.recommended_price if latest else None,
                recommendation_id=latest.id if latest else None,
            )
            _notify(
                info, clients,
                notification_type="ANALYTICS_READY",
                title="Аналитика готова",
                message=(
                    f"Сформирован аналитический отчёт по товару "
                    f"«{product.name}» ({dto.analysis_type})."
                ),
                related_entity_id=dto.id,
            )
        return AnalyticsResultType.from_dto(dto)

    @strawberry.mutation
    def mark_notification_read(
        self, info: Info, id: strawberry.ID
    ) -> NotificationType:
        with translate_errors():
            require_user(info)
            dto = get_clients(info).notification.mark_notification_read(str(id))
        return NotificationType.from_dto(dto)

    @strawberry.mutation
    def mark_all_notifications_read(self, info: Info) -> int:
        with translate_errors():
            require_user(info)
            require_user(info)
            return get_clients(info).notification.mark_all_notifications_read()
