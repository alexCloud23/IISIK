from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from fixtures.ids import USER, uid
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
from shared.validation import validate_non_empty, validate_positive_price

from ...dto import (
    AnalyticsResultData,
    ForecastData,
    NotificationData,
    ProductData,
    RecommendationData,
    RecommendationsSummaryData,
    SalesRecordData,
    SalesSummaryData,
    StrategyData,
)
from ..base import UNSET

PRODUCT_SORT_FIELDS = {
    "name": lambda item: item.name,
    "price": lambda item: item.base_price,
    "created": lambda item: item.created_at,
}
RECOMMENDATION_SORT_FIELDS = {
    "created": lambda item: item.created_at,
    "price": lambda item: item.recommended_price,
}
ORDERS = ("asc", "desc")

DEFAULT_NOTIFICATION_USER_ID = uid(USER, 1)


def _normalize_id(value: str, field: str) -> str | None:
    if value is None:
        return None
    return str(parse_uuid(value, field))


def _sorted(
    items: list,
    sort: str,
    order: str,
    fields: dict,
) -> list:
    if sort not in fields:
        raise InvalidFilterError(
            f"Неизвестное поле сортировки: {sort!r}; "
            f"допустимо: {', '.join(fields)}"
        )
    if order not in ORDERS:
        raise InvalidFilterError(
            f"Неизвестное направление сортировки: {order!r}; "
            f"допустимо: {', '.join(ORDERS)}"
        )
    return sorted(items, key=fields[sort], reverse=order == "desc")


def _now() -> datetime:
    return datetime.utcnow().replace(microsecond=0)


class MockProductClient:
    def __init__(self, products: list[ProductData]) -> None:
        self._products = products

    def list_products(
        self,
        category: str | None = None,
        is_active: bool | None = None,
        search: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        sort: str = "name",
        order: str = "asc",
    ) -> list[ProductData]:
        lowered = search.lower() if search else None
        items = [
            item
            for item in self._products
            if (category is None or item.category == category)
            and (is_active is None or item.is_active == is_active)
            and (lowered is None or lowered in item.name.lower())
            and (min_price is None or item.base_price >= min_price)
            and (max_price is None or item.base_price <= max_price)
        ]
        return _sorted(items, sort, order, PRODUCT_SORT_FIELDS)

    def get_product(self, product_id: str) -> ProductData | None:
        normalized = _normalize_id(product_id, "product_id")
        return next((item for item in self._products if item.id == normalized), None)

    def create_product(
        self,
        *,
        name: str,
        description: str | None,
        category: str,
        base_price: Decimal,
        currency: str,
    ) -> ProductData:
        name = validate_non_empty(name, "name")
        category = validate_non_empty(category, "category")
        currency = validate_non_empty(currency, "currency")
        price = validate_positive_price(base_price, "base_price")
        if any(item.name.lower() == name.lower() for item in self._products):
            raise InvalidOperationError(f"Товар с названием «{name}» уже существует")

        now = _now()
        product = ProductData(
            id=str(uuid4()),
            name=name,
            description=description,
            category=category,
            base_price=round_money(price),
            currency=currency,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        self._products.append(product)
        return product

    def update_product(
        self,
        product_id: str,
        *,
        base_price: Decimal | None = UNSET,
        description: str | None = UNSET,
        is_active: bool | None = UNSET,
    ) -> ProductData:
        normalized = _normalize_id(product_id, "product_id")
        product = next((item for item in self._products if item.id == normalized), None)
        if product is None:
            raise NotFoundError(f"Товар {product_id} не найден")

        if base_price is not UNSET:
            if not product.is_active:
                raise InvalidOperationError("Нельзя изменять цену неактивного товара")
            price = validate_positive_price(base_price, "base_price")
            product.base_price = round_money(price)
        if description is not UNSET:
            product.description = description
        if is_active is not UNSET and is_active is not None:
            product.is_active = is_active
        product.updated_at = _now()
        return product


class MockForecastClient:
    def __init__(self, forecasts: list[ForecastData]) -> None:
        self._forecasts = forecasts

    def list_forecasts(self, product_id: str | None = None) -> list[ForecastData]:
        normalized = _normalize_id(product_id, "product_id") if product_id else None
        items = [
            item
            for item in self._forecasts
            if normalized is None or item.product_id == normalized
        ]
        return sorted(
            items,
            key=lambda item: (item.period_start, item.id),
            reverse=True,
        )


class MockStrategyClient:
    def __init__(self, strategies: list[StrategyData]) -> None:
        self._strategies = strategies

    def list_strategies(self, product_id: str | None = None) -> list[StrategyData]:
        normalized = _normalize_id(product_id, "product_id") if product_id else None
        items = [
            item
            for item in self._strategies
            if normalized is None or item.product_id == normalized
        ]
        return sorted(
            items,
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        )


class MockRecommendationClient:
    def __init__(
        self,
        recommendations: list[RecommendationData],
        forecasts: list[ForecastData],
    ) -> None:
        self._recommendations = recommendations
        self._forecasts = {item.id: item for item in forecasts}

    def list_recommendations(
        self,
        product_id: str | None = None,
        status: str | None = None,
        sort: str = "created",
        order: str = "desc",
    ) -> list[RecommendationData]:
        normalized = _normalize_id(product_id, "product_id") if product_id else None
        items = [
            item
            for item in self._recommendations
            if (normalized is None or item.product_id == normalized)
            and (status is None or item.status == status)
        ]
        return _sorted(items, sort, order, RECOMMENDATION_SORT_FIELDS)

    def get_recommendation(
        self, recommendation_id: str
    ) -> RecommendationData | None:
        normalized = _normalize_id(recommendation_id, "recommendation_id")
        return next(
            (item for item in self._recommendations if item.id == normalized), None
        )

    def create_recommendation(
        self,
        *,
        product_id: str,
        forecast_id: str,
        current_price: Decimal,
        strategy_type: str | None = None,
        competitor_price: Decimal | None = None,
        strategy_id: str | None = None,
    ) -> RecommendationData:
        normalized_product = _normalize_id(product_id, "product_id")
        normalized_forecast = _normalize_id(forecast_id, "forecast_id")
        normalized_strategy = (
            _normalize_id(strategy_id, "strategy_id") if strategy_id else None
        )
        price = validate_positive_price(current_price, "current_price")

        if strategy_type is not None:
            if strategy_type not in STRATEGY_TYPES:
                raise InvalidInputError(f"Неизвестный тип стратегии: {strategy_type}")
            if competitor_price is None:
                raise InvalidInputError(
                    "Для стратегии требуется цена конкурента (competitor_price)"
                )
            validate_positive_price(competitor_price, "competitor_price")

        forecast = self._forecasts.get(normalized_forecast)
        if forecast is None:
            raise NotFoundError(f"Прогноз спроса {forecast_id} не найден")

        recommended, reason = compute_recommendation(
            price, strategy_type, competitor_price, forecast.predicted_demand
        )
        recommendation = RecommendationData(
            id=str(uuid4()),
            product_id=normalized_product,
            forecast_id=normalized_forecast,
            strategy_id=normalized_strategy,
            current_price=round_money(price),
            recommended_price=recommended,
            currency="BYN",
            reason=reason,
            status="NEW",
            created_at=_now(),
        )
        self._recommendations.append(recommendation)
        return recommendation

    def decide_recommendation(
        self, recommendation_id: str, decision: str
    ) -> RecommendationData:
        if decision not in VALID_DECISIONS:
            raise InvalidInputError(
                f"Неизвестное решение: {decision!r}; "
                f"допустимо: {', '.join(VALID_DECISIONS)}"
            )
        normalized = _normalize_id(recommendation_id, "recommendation_id")
        recommendation = next(
            (item for item in self._recommendations if item.id == normalized), None
        )
        if recommendation is None:
            raise NotFoundError(f"Рекомендация {recommendation_id} не найдена")
        if recommendation.status != "NEW":
            raise InvalidOperationError("Решение по рекомендации уже принято")

        recommendation.status = decision
        return recommendation

    def recommendations_summary(self) -> RecommendationsSummaryData:
        counts = {"NEW": 0, "ACCEPTED": 0, "REJECTED": 0}
        for item in self._recommendations:
            if item.status in counts:
                counts[item.status] += 1
        return RecommendationsSummaryData(
            total=len(self._recommendations),
            new=counts["NEW"],
            accepted=counts["ACCEPTED"],
            rejected=counts["REJECTED"],
        )


class MockAnalyticsClient:
    def __init__(self, results: list[AnalyticsResultData]) -> None:
        self._results = results

    def list_results(
        self, analysis_type: str | None = None
    ) -> list[AnalyticsResultData]:
        items = [
            item
            for item in self._results
            if analysis_type is None or item.analysis_type == analysis_type
        ]
        return sorted(items, key=lambda item: item.created_at, reverse=True)


class MockNotificationClient:
    def __init__(self, notifications: list[NotificationData]) -> None:
        self._notifications = notifications

    def list_notifications(
        self,
        is_read: bool | None = None,
        notification_type: str | None = None,
    ) -> list[NotificationData]:
        items = [
            item
            for item in self._notifications
            if (is_read is None or item.is_read == is_read)
            and (
                notification_type is None
                or item.notification_type == notification_type
            )
        ]
        return sorted(items, key=lambda item: item.created_at, reverse=True)

    def get_unread_count(self) -> int:
        return sum(1 for item in self._notifications if not item.is_read)

    def create_notification(
        self,
        *,
        notification_type: str,
        title: str,
        message: str,
        related_entity_id: str | None = None,
        user_id: str | None = None,
    ) -> NotificationData:
        notification_type = validate_non_empty(notification_type, "notification_type")
        title = validate_non_empty(title, "title")
        message = validate_non_empty(message, "message")

        now = _now()
        notification = NotificationData(
            id=str(uuid4()),
            user_id=(
                _normalize_id(user_id, "user_id")
                if user_id
                else DEFAULT_NOTIFICATION_USER_ID
            ),
            notification_type=notification_type,
            title=title,
            message=message,
            related_entity_id=(
                _normalize_id(related_entity_id, "related_entity_id")
                if related_entity_id
                else related_entity_id
            ),
            status="SENT",
            is_read=False,
            created_at=now,
            sent_at=now,
        )
        self._notifications.append(notification)
        return notification

    def mark_notification_read(self, notification_id: str) -> NotificationData:
        normalized = _normalize_id(notification_id, "notification_id")
        notification = next(
            (item for item in self._notifications if item.id == normalized), None
        )
        if notification is None:
            raise NotFoundError(f"Уведомление {notification_id} не найдено")
        notification.is_read = True
        return notification

    def mark_all_notifications_read(self) -> int:
        updated = 0
        for item in self._notifications:
            if not item.is_read:
                item.is_read = True
                updated += 1
        return updated


class MockMarketDataClient:
    def __init__(self, sales: list[SalesRecordData]) -> None:
        self._sales = sales

    def sales_summary(self, product_id: str) -> SalesSummaryData:
        normalized = _normalize_id(product_id, "product_id")
        records = [item for item in self._sales if item.product_id == normalized]
        total_quantity = sum(item.quantity for item in records)
        total_price = sum((item.unit_price for item in records), Decimal("0"))
        average = total_price / len(records) if records else Decimal("0")
        return SalesSummaryData(
            product_id=normalized,
            records=len(records),
            total_quantity=total_quantity,
            average_unit_price=average,
        )
