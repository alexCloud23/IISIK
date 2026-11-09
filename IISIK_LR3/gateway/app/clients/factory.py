from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from fixtures.analytics import ANALYTICS_RESULTS
from fixtures.forecast import FORECASTS
from fixtures.market_data import SALES
from fixtures.notification import NOTIFICATIONS
from fixtures.pricing import RECOMMENDATIONS
from fixtures.product import PRODUCTS
from fixtures.strategy import STRATEGIES

from ..config import Settings
from ..dto import (
    AnalyticsResultData,
    ForecastData,
    NotificationData,
    ProductData,
    RecommendationData,
    SalesRecordData,
    StrategyData,
)
from .base import (
    AnalyticsClient,
    ForecastClient,
    MarketDataClient,
    NotificationClient,
    ProductClient,
    RecommendationClient,
    StrategyClient,
)
from .http import (
    HttpAnalyticsClient,
    HttpForecastClient,
    HttpMarketDataClient,
    HttpNotificationClient,
    HttpProductClient,
    HttpRecommendationClient,
    HttpStrategyClient,
)
from .mock import (
    MockAnalyticsClient,
    MockForecastClient,
    MockMarketDataClient,
    MockNotificationClient,
    MockProductClient,
    MockRecommendationClient,
    MockStrategyClient,
)


@dataclass
class ClientBundle:
    product: ProductClient
    forecast: ForecastClient
    strategy: StrategyClient
    recommendation: RecommendationClient
    analytics: AnalyticsClient
    notification: NotificationClient
    market_data: MarketDataClient

    def close(self) -> None:
        for client in (
            self.product,
            self.forecast,
            self.strategy,
            self.recommendation,
            self.analytics,
            self.notification,
            self.market_data,
        ):
            close = getattr(client, "close", None)
            if callable(close):
                close()


def build_mock_bundle() -> ClientBundle:
    forecasts = [ForecastData.model_validate(item) for item in FORECASTS]
    return ClientBundle(
        product=MockProductClient(
            [ProductData.model_validate(item) for item in PRODUCTS]
        ),
        forecast=MockForecastClient(forecasts),
        strategy=MockStrategyClient(
            [StrategyData.model_validate(item) for item in STRATEGIES]
        ),
        recommendation=MockRecommendationClient(
            [RecommendationData.model_validate(item) for item in RECOMMENDATIONS],
            forecasts,
        ),
        analytics=MockAnalyticsClient(
            [AnalyticsResultData.model_validate(item) for item in ANALYTICS_RESULTS]
        ),
        notification=MockNotificationClient(
            [NotificationData.model_validate(item) for item in NOTIFICATIONS]
        ),
        market_data=MockMarketDataClient(
            [SalesRecordData.model_validate(item) for item in SALES]
        ),
    )


def build_http_bundle(
    settings: Settings,
    transports: dict[str, httpx.BaseTransport] | None = None,
) -> ClientBundle:
    transports = transports or {}

    def transport(name: str) -> Any:
        return transports.get(name)

    common = {"timeout": settings.request_timeout}
    return ClientBundle(
        product=HttpProductClient(
            settings.product_service_url, transport=transport("product"), **common
        ),
        forecast=HttpForecastClient(
            settings.forecast_service_url, transport=transport("forecast"), **common
        ),
        strategy=HttpStrategyClient(
            settings.strategy_service_url, transport=transport("strategy"), **common
        ),
        recommendation=HttpRecommendationClient(
            settings.pricing_service_url,
            transport=transport("recommendation"),
            **common,
        ),
        analytics=HttpAnalyticsClient(
            settings.analytics_service_url, transport=transport("analytics"), **common
        ),
        notification=HttpNotificationClient(
            settings.notification_service_url,
            transport=transport("notification"),
            **common,
        ),
        market_data=HttpMarketDataClient(
            settings.market_data_service_url,
            transport=transport("market_data"),
            **common,
        ),
    )


def build_clients(
    settings: Settings,
    transports: dict[str, httpx.BaseTransport] | None = None,
) -> ClientBundle:
    mode = settings.client_mode.lower()
    if mode == "mock":
        return build_mock_bundle()
    if mode == "http":
        return build_http_bundle(settings, transports)
    raise ValueError(
        f"Неизвестный режим GATEWAY_CLIENT_MODE={settings.client_mode!r}; "
        "ожидается 'mock' или 'http'"
    )
