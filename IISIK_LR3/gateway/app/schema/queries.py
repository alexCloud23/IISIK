from __future__ import annotations

from decimal import Decimal

import strawberry
from strawberry.types import Info

from shared.errors import NotFoundError

from ..context import get_clients
from ..resolvers import translate_errors
from .types import (
    AnalyticsResultType,
    CompetitorStrategyType,
    DemandForecastType,
    NotificationType,
    PriceRecommendationType,
    ProductSortField,
    ProductType,
    RecommendationSortField,
    RecommendationStatus,
    RecommendationsSummaryType,
    SalesSummaryType,
    SortDirection,
)


def _as_decimal(value: float | None) -> Decimal | None:
    return None if value is None else Decimal(str(value))


@strawberry.type
class Query:
    @strawberry.field
    def products(
        self,
        info: Info,
        category: str | None = None,
        is_active: bool | None = None,
        search: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        order_by: ProductSortField = ProductSortField.NAME,
        order_direction: SortDirection = SortDirection.ASC,
    ) -> list[ProductType]:
        with translate_errors():
            items = get_clients(info).product.list_products(
                category=category,
                is_active=is_active,
                search=search,
                min_price=_as_decimal(min_price),
                max_price=_as_decimal(max_price),
                sort=order_by.value,
                order=order_direction.value.lower(),
            )
        return [ProductType.from_dto(item) for item in items]

    @strawberry.field
    def product(self, info: Info, id: strawberry.ID) -> ProductType | None:
        with translate_errors():
            item = get_clients(info).product.get_product(str(id))
            if item is None:
                raise NotFoundError(f"Товар {id} не найден")
        return ProductType.from_dto(item)

    @strawberry.field
    def demand_forecasts(
        self, info: Info, product_id: strawberry.ID | None = None
    ) -> list[DemandForecastType]:
        with translate_errors():
            items = get_clients(info).forecast.list_forecasts(
                str(product_id) if product_id else None
            )
        return [DemandForecastType.from_dto(item) for item in items]

    @strawberry.field
    def competitor_strategies(
        self, info: Info, product_id: strawberry.ID | None = None
    ) -> list[CompetitorStrategyType]:
        with translate_errors():
            items = get_clients(info).strategy.list_strategies(
                str(product_id) if product_id else None
            )
        return [CompetitorStrategyType.from_dto(item) for item in items]

    @strawberry.field
    def price_recommendations(
        self,
        info: Info,
        product_id: strawberry.ID | None = None,
        status: RecommendationStatus | None = None,
        order_by: RecommendationSortField = RecommendationSortField.CREATED_AT,
        order_direction: SortDirection = SortDirection.DESC,
    ) -> list[PriceRecommendationType]:
        with translate_errors():
            items = get_clients(info).recommendation.list_recommendations(
                product_id=str(product_id) if product_id else None,
                status=status.value if status else None,
                sort=order_by.value,
                order=order_direction.value.lower(),
            )
        return [PriceRecommendationType.from_dto(item) for item in items]

    @strawberry.field
    def price_recommendation(
        self, info: Info, id: strawberry.ID
    ) -> PriceRecommendationType | None:
        with translate_errors():
            item = get_clients(info).recommendation.get_recommendation(str(id))
            if item is None:
                raise NotFoundError(f"Рекомендация {id} не найдена")
        return PriceRecommendationType.from_dto(item)

    @strawberry.field
    def analytics_results(
        self, info: Info, analysis_type: str | None = None
    ) -> list[AnalyticsResultType]:
        with translate_errors():
            items = get_clients(info).analytics.list_results(analysis_type)
        return [AnalyticsResultType.from_dto(item) for item in items]

    @strawberry.field
    def notifications(
        self,
        info: Info,
        is_read: bool | None = None,
        notification_type: str | None = None,
    ) -> list[NotificationType]:
        with translate_errors():
            items = get_clients(info).notification.list_notifications(
                is_read, notification_type
            )
        return [NotificationType.from_dto(item) for item in items]

    @strawberry.field
    def sales_summary(
        self, info: Info, product_id: strawberry.ID
    ) -> SalesSummaryType:
        with translate_errors():
            summary = get_clients(info).market_data.sales_summary(str(product_id))
        return SalesSummaryType.from_dto(summary)

    @strawberry.field
    def unread_notifications_count(self, info: Info) -> int:
        with translate_errors():
            return get_clients(info).notification.get_unread_count()

    @strawberry.field
    def recommendations_summary(self, info: Info) -> RecommendationsSummaryType:
        with translate_errors():
            summary = get_clients(info).recommendation.recommendations_summary()
        return RecommendationsSummaryType.from_dto(summary)
