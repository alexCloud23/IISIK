from __future__ import annotations

from decimal import Decimal
from typing import Protocol

import strawberry

from ..dto import (
    AnalyticsResultData,
    ForecastData,
    NotificationData,
    ProductData,
    RecommendationData,
    RecommendationsSummaryData,
    SalesSummaryData,
    StrategyData,
)

_UNSET = strawberry.UNSET
UNSET = _UNSET


class ProductClient(Protocol):
    def list_products(
        self,
        category: str | None = None,
        is_active: bool | None = None,
        search: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        sort: str = "name",
        order: str = "asc",
    ) -> list[ProductData]: ...

    def get_product(self, product_id: str) -> ProductData | None: ...

    def create_product(
        self,
        *,
        name: str,
        description: str | None,
        category: str,
        base_price: Decimal,
        currency: str,
    ) -> ProductData: ...

    def update_product(
        self,
        product_id: str,
        *,
        base_price: Decimal | None = _UNSET,
        description: str | None = _UNSET,
        is_active: bool | None = _UNSET,
    ) -> ProductData: ...


class ForecastClient(Protocol):
    def list_forecasts(self, product_id: str | None = None) -> list[ForecastData]: ...


class StrategyClient(Protocol):
    def list_strategies(self, product_id: str | None = None) -> list[StrategyData]: ...


class RecommendationClient(Protocol):
    def list_recommendations(
        self,
        product_id: str | None = None,
        status: str | None = None,
        sort: str = "created",
        order: str = "desc",
    ) -> list[RecommendationData]: ...

    def get_recommendation(
        self, recommendation_id: str
    ) -> RecommendationData | None: ...

    def create_recommendation(
        self,
        *,
        product_id: str,
        forecast_id: str,
        current_price: Decimal,
        strategy_type: str | None = None,
        competitor_price: Decimal | None = None,
        strategy_id: str | None = None,
    ) -> RecommendationData: ...

    def decide_recommendation(
        self, recommendation_id: str, decision: str
    ) -> RecommendationData: ...

    def recommendations_summary(self) -> RecommendationsSummaryData: ...


class AnalyticsClient(Protocol):
    def list_results(
        self, analysis_type: str | None = None
    ) -> list[AnalyticsResultData]: ...


class NotificationClient(Protocol):
    def list_notifications(
        self, is_read: bool | None = None, notification_type: str | None = None
    ) -> list[NotificationData]: ...

    def get_unread_count(self) -> int: ...

    def create_notification(
        self,
        *,
        notification_type: str,
        title: str,
        message: str,
        related_entity_id: str | None = None,
        user_id: str | None = None,
    ) -> NotificationData: ...

    def mark_notification_read(self, notification_id: str) -> NotificationData: ...

    def mark_all_notifications_read(self) -> int: ...


class MarketDataClient(Protocol):
    def sales_summary(self, product_id: str) -> SalesSummaryData: ...
