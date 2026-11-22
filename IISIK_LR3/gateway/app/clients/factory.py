from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from fixtures.analytics import ANALYTICS_RESULTS
from fixtures.forecast import FORECASTS
from fixtures.market_data import COMPETITOR_PRICES, SALES
from fixtures.notification import NOTIFICATIONS
from fixtures.pricing import RECOMMENDATIONS
from fixtures.product import PRODUCTS
from fixtures.strategy import STRATEGIES

from ..cache import RedisCache
from ..config import Settings
from ..dto import (
    AnalyticsResultData,
    CompetitorPriceData,
    ForecastData,
    NotificationData,
    ProductData,
    RecommendationData,
    SalesRecordData,
    StrategyData,
)
from .base import (
    AnalyticsClient,
    AuthClient,
    ForecastClient,
    MarketDataClient,
    NotificationClient,
    ProductClient,
    RecommendationClient,
    StrategyClient,
)
from .cached import CachedProductClient
from .http import (
    HttpAnalyticsClient,
    HttpAuthClient,
    HttpForecastClient,
    HttpMarketDataClient,
    HttpNotificationClient,
    HttpProductClient,
    HttpRecommendationClient,
    HttpStrategyClient,
)
from .mock import (
    MockAnalyticsClient,
    MockAuthClient,
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
    auth: AuthClient

    def close(self) -> None:
        for client in (
            self.product,
            self.forecast,
            self.strategy,
            self.recommendation,
            self.analytics,
            self.notification,
            self.market_data,
            self.auth,
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
            [SalesRecordData.model_validate(item) for item in SALES],
            [CompetitorPriceData.model_validate(item) for item in COMPETITOR_PRICES],
        ),
        auth=MockAuthClient(),
    )


def _cached_product(client: ProductClient, settings: Settings) -> ProductClient:
    return CachedProductClient(
        client, RedisCache(settings.redis_url, settings.cache_ttl_seconds)
    )


def build_http_bundle(
    settings: Settings,
    transports: dict[str, httpx.BaseTransport] | None = None,
) -> ClientBundle:
    transports = transports or {}

    def transport(name: str) -> Any:
        return transports.get(name)

    common = {
        "timeout": settings.request_timeout,
        "retry_attempts": settings.http_retry_attempts,
        "retry_backoff": settings.retry_backoff,
    }
    return ClientBundle(
        product=_cached_product(
            HttpProductClient(
                settings.product_service_url, transport=transport("product"), **common
            ),
            settings,
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
        auth=HttpAuthClient(
            settings.identity_service_url, transport=transport("auth"), **common
        ),
    )


def build_grpc_bundle(
    settings: Settings, addrs: dict[str, str] | None = None
) -> ClientBundle:
    from .grpc import (
        GrpcAnalyticsClient,
        GrpcAuthClient,
        GrpcForecastClient,
        GrpcMarketDataClient,
        GrpcNotificationClient,
        GrpcProductClient,
        GrpcRecommendationClient,
        GrpcStrategyClient,
    )

    addrs = addrs or {}

    def addr(name: str, default: str) -> str:
        return addrs.get(name, default)

    common = {
        "timeout": settings.grpc_timeout,
        "retry_attempts": settings.grpc_retry_attempts,
        "retry_backoff": settings.retry_backoff,
    }
    return ClientBundle(
        product=_cached_product(
            GrpcProductClient(addr("product", settings.product_grpc_addr), **common),
            settings,
        ),
        forecast=GrpcForecastClient(addr("forecast", settings.forecast_grpc_addr), **common),
        strategy=GrpcStrategyClient(addr("strategy", settings.strategy_grpc_addr), **common),
        recommendation=GrpcRecommendationClient(
            addr("recommendation", settings.pricing_grpc_addr), **common
        ),
        analytics=GrpcAnalyticsClient(
            addr("analytics", settings.analytics_grpc_addr), **common
        ),
        notification=GrpcNotificationClient(
            addr("notification", settings.notification_grpc_addr), **common
        ),
        market_data=GrpcMarketDataClient(
            addr("market_data", settings.market_data_grpc_addr), **common
        ),
        auth=GrpcAuthClient(addr("auth", settings.identity_grpc_addr), **common),
    )


def build_clients(
    settings: Settings,
    transports: dict[str, httpx.BaseTransport] | None = None,
    grpc_addrs: dict[str, str] | None = None,
) -> ClientBundle:
    mode = settings.client_mode.lower()
    if mode == "mock":
        return build_mock_bundle()
    if mode == "http":
        return build_http_bundle(settings, transports)
    if mode == "grpc":
        return build_grpc_bundle(settings, grpc_addrs)
    raise ValueError(
        f"Неизвестный режим GATEWAY_CLIENT_MODE={settings.client_mode!r}; "
        "ожидается 'mock', 'http' или 'grpc'"
    )
