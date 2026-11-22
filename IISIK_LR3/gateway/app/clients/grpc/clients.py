from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from typing import Callable, TypeVar

import grpc
from google.protobuf.empty_pb2 import Empty

import shared.protogen
import analytics_pb2
import analytics_pb2_grpc
import forecast_pb2
import forecast_pb2_grpc
import identity_pb2
import identity_pb2_grpc
import market_data_pb2
import market_data_pb2_grpc
import notification_pb2
import notification_pb2_grpc
import pricing_pb2
import pricing_pb2_grpc
import product_pb2
import product_pb2_grpc
import strategy_pb2
import strategy_pb2_grpc
from shared.grpc_errors import raise_domain_error

from ...dto import (
    AnalyticsResultData,
    AuthPayloadData,
    AuthUserData,
    CompetitorPriceData,
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

T = TypeVar("T")


class GrpcServiceClient:
    def __init__(self, addr: str) -> None:
        self._addr = addr
        self._channel = grpc.insecure_channel(addr)

    def close(self) -> None:
        self._channel.close()

    def _call(self, method: Callable[..., T], request) -> T:
        try:
            return method(request)
        except grpc.RpcError as exc:
            raise_domain_error(exc, self._addr)

    def _call_optional(self, method: Callable[..., T], request) -> T | None:
        try:
            return method(request)
        except grpc.RpcError as exc:
            if exc.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise_domain_error(exc, self._addr)


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _product(msg) -> ProductData:
    return ProductData(
        id=msg.id,
        name=msg.name,
        description=msg.description if msg.HasField("description") else None,
        category=msg.category,
        base_price=Decimal(msg.base_price),
        currency=msg.currency,
        is_active=msg.is_active,
        created_at=_dt(msg.created_at),
        updated_at=_dt(msg.updated_at),
    )


def _forecast(msg) -> ForecastData:
    return ForecastData(
        id=msg.id,
        product_id=msg.product_id,
        period_start=_dt(msg.period_start),
        period_end=_dt(msg.period_end),
        predicted_demand=Decimal(msg.predicted_demand),
        confidence=Decimal(msg.confidence) if msg.HasField("confidence") else None,
        model_version=msg.model_version,
        created_at=_dt(msg.created_at),
    )


def _strategy(msg) -> StrategyData:
    return StrategyData(
        id=msg.id,
        product_id=msg.product_id,
        competitor_name=msg.competitor_name,
        strategy_type=msg.strategy_type,
        competitor_price=Decimal(msg.competitor_price),
        price_change_percent=(
            Decimal(msg.price_change_percent)
            if msg.HasField("price_change_percent")
            else None
        ),
        estimated_probability=(
            Decimal(msg.estimated_probability)
            if msg.HasField("estimated_probability")
            else None
        ),
        created_at=_dt(msg.created_at),
    )


def _recommendation(msg) -> RecommendationData:
    return RecommendationData(
        id=msg.id,
        product_id=msg.product_id,
        forecast_id=msg.forecast_id,
        strategy_id=msg.strategy_id if msg.HasField("strategy_id") else None,
        current_price=Decimal(msg.current_price),
        recommended_price=Decimal(msg.recommended_price),
        currency=msg.currency,
        reason=msg.reason,
        status=msg.status,
        created_at=_dt(msg.created_at),
    )


def _sales_record(msg) -> SalesRecordData:
    return SalesRecordData(
        id=msg.id,
        product_id=msg.product_id,
        quantity=msg.quantity,
        unit_price=Decimal(msg.unit_price),
        currency=msg.currency,
        sold_at=_dt(msg.sold_at),
    )


def _competitor_price(msg) -> CompetitorPriceData:
    return CompetitorPriceData(
        id=msg.id,
        product_id=msg.product_id,
        competitor_name=msg.competitor_name,
        price=Decimal(msg.price),
        currency=msg.currency,
        source=msg.source,
        observed_at=_dt(msg.observed_at),
    )


def _analytics_result(msg) -> AnalyticsResultData:
    return AnalyticsResultData(
        id=msg.id,
        product_id=msg.product_id if msg.HasField("product_id") else None,
        recommendation_id=(
            msg.recommendation_id if msg.HasField("recommendation_id") else None
        ),
        analysis_type=msg.analysis_type,
        metrics=json.loads(msg.metrics_json),
        created_at=_dt(msg.created_at),
    )


def _notification(msg) -> NotificationData:
    return NotificationData(
        id=msg.id,
        user_id=msg.user_id,
        notification_type=msg.notification_type,
        title=msg.title,
        message=msg.message,
        related_entity_id=(
            msg.related_entity_id if msg.HasField("related_entity_id") else None
        ),
        status=msg.status,
        is_read=msg.is_read,
        created_at=_dt(msg.created_at),
        sent_at=_dt(msg.sent_at) if msg.HasField("sent_at") else None,
    )


def _money(value: Decimal | None) -> str | None:
    return None if value is None else str(value)


class GrpcProductClient(GrpcServiceClient):
    def __init__(self, addr: str) -> None:
        super().__init__(addr)
        self._stub = product_pb2_grpc.ProductServiceStub(self._channel)

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
        request = product_pb2.ListProductsRequest(
            category=category,
            is_active=is_active,
            search=search,
            min_price=_money(min_price),
            max_price=_money(max_price),
            sort=sort,
            order=order,
        )
        response = self._call(self._stub.ListProducts, request)
        return [_product(item) for item in response.products]

    def get_product(self, product_id: str) -> ProductData | None:
        response = self._call_optional(
            self._stub.GetProduct, product_pb2.GetProductRequest(id=product_id)
        )
        if response is None or not response.HasField("product"):
            return None
        return _product(response.product)

    def create_product(
        self,
        *,
        name: str,
        description: str | None,
        category: str,
        base_price: Decimal,
        currency: str,
    ) -> ProductData:
        request = product_pb2.CreateProductRequest(
            name=name,
            description=description,
            category=category,
            base_price=str(base_price),
            currency=currency,
        )
        return _product(self._call(self._stub.CreateProduct, request))

    def update_product(
        self,
        product_id: str,
        *,
        base_price: Decimal | None = UNSET,
        description: str | None = UNSET,
        is_active: bool | None = UNSET,
    ) -> ProductData:
        request = product_pb2.UpdateProductRequest(id=product_id)
        if base_price is not UNSET:
            request.base_price = str(base_price)
        if description is not UNSET:
            if description is None:
                request.description = ""
            else:
                request.description = description
        if is_active is not UNSET:
            request.is_active = is_active
        return _product(self._call(self._stub.UpdateProduct, request))


class GrpcForecastClient(GrpcServiceClient):
    def __init__(self, addr: str) -> None:
        super().__init__(addr)
        self._stub = forecast_pb2_grpc.ForecastServiceStub(self._channel)

    def list_forecasts(self, product_id: str | None = None) -> list[ForecastData]:
        response = self._call(
            self._stub.ListForecasts,
            forecast_pb2.ListForecastsRequest(product_id=product_id),
        )
        return [_forecast(item) for item in response.forecasts]

    def generate_forecast(
        self,
        *,
        product_id: str,
        period_days: int,
        sales: list[SalesRecordData],
    ) -> ForecastData:
        request = forecast_pb2.GenerateForecastRequest(
            product_id=product_id,
            period_days=period_days,
            sales=[
                forecast_pb2.SalePoint(
                    quantity=item.quantity, sold_at=item.sold_at.isoformat()
                )
                for item in sales
            ],
        )
        return _forecast(self._call(self._stub.GenerateForecast, request))


class GrpcStrategyClient(GrpcServiceClient):
    def __init__(self, addr: str) -> None:
        super().__init__(addr)
        self._stub = strategy_pb2_grpc.StrategyServiceStub(self._channel)

    def list_strategies(self, product_id: str | None = None) -> list[StrategyData]:
        response = self._call(
            self._stub.ListStrategies,
            strategy_pb2.ListStrategiesRequest(product_id=product_id),
        )
        return [_strategy(item) for item in response.strategies]

    def analyze_strategy(
        self,
        *,
        product_id: str,
        current_price: Decimal,
        competitor_prices: list[CompetitorPriceData],
    ) -> StrategyData:
        request = strategy_pb2.AnalyzeStrategyRequest(
            product_id=product_id,
            current_price=str(current_price),
            competitor_prices=[
                strategy_pb2.CompetitorPricePoint(
                    competitor_name=item.competitor_name,
                    price=str(item.price),
                    observed_at=item.observed_at.isoformat(),
                )
                for item in competitor_prices
            ],
        )
        return _strategy(self._call(self._stub.AnalyzeStrategy, request))


class GrpcRecommendationClient(GrpcServiceClient):
    def __init__(self, addr: str) -> None:
        super().__init__(addr)
        self._stub = pricing_pb2_grpc.PricingServiceStub(self._channel)

    def list_recommendations(
        self,
        product_id: str | None = None,
        status: str | None = None,
        sort: str = "created",
        order: str = "desc",
    ) -> list[RecommendationData]:
        response = self._call(
            self._stub.ListRecommendations,
            pricing_pb2.ListRecommendationsRequest(
                product_id=product_id, status=status, sort=sort, order=order
            ),
        )
        return [_recommendation(item) for item in response.recommendations]

    def get_recommendation(
        self, recommendation_id: str
    ) -> RecommendationData | None:
        response = self._call_optional(
            self._stub.GetRecommendation,
            pricing_pb2.GetRecommendationRequest(id=recommendation_id),
        )
        if response is None or not response.HasField("recommendation"):
            return None
        return _recommendation(response.recommendation)

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
        request = pricing_pb2.CreateRecommendationRequest(
            product_id=product_id,
            forecast_id=forecast_id,
            current_price=str(current_price),
            strategy_type=strategy_type,
            competitor_price=_money(competitor_price),
            strategy_id=strategy_id,
        )
        return _recommendation(self._call(self._stub.CreateRecommendation, request))

    def decide_recommendation(
        self, recommendation_id: str, decision: str
    ) -> RecommendationData:
        return _recommendation(
            self._call(
                self._stub.DecideRecommendation,
                pricing_pb2.DecideRecommendationRequest(
                    id=recommendation_id, decision=decision
                ),
            )
        )

    def recommendations_summary(self) -> RecommendationsSummaryData:
        response = self._call(self._stub.RecommendationsSummary, Empty())
        return RecommendationsSummaryData(
            total=response.total,
            new=response.new,
            accepted=response.accepted,
            rejected=response.rejected,
        )


class GrpcAnalyticsClient(GrpcServiceClient):
    def __init__(self, addr: str) -> None:
        super().__init__(addr)
        self._stub = analytics_pb2_grpc.AnalyticsServiceStub(self._channel)

    def list_results(
        self, analysis_type: str | None = None
    ) -> list[AnalyticsResultData]:
        response = self._call(
            self._stub.ListResults,
            analytics_pb2.ListResultsRequest(analysis_type=analysis_type),
        )
        return [_analytics_result(item) for item in response.results]

    def run_analysis(
        self,
        *,
        product_id: str,
        analysis_type: str,
        summary: SalesSummaryData,
        predicted_demand: Decimal | None = None,
        current_price: Decimal | None = None,
        recommended_price: Decimal | None = None,
        recommendation_id: str | None = None,
    ) -> AnalyticsResultData:
        request = analytics_pb2.RunAnalysisRequest(
            product_id=product_id,
            analysis_type=analysis_type,
            records=summary.records,
            total_quantity=summary.total_quantity,
            average_unit_price=str(summary.average_unit_price),
            predicted_demand=_money(predicted_demand),
            current_price=_money(current_price),
            recommended_price=_money(recommended_price),
            recommendation_id=recommendation_id,
        )
        return _analytics_result(self._call(self._stub.RunAnalysis, request))


class GrpcNotificationClient(GrpcServiceClient):
    def __init__(self, addr: str) -> None:
        super().__init__(addr)
        self._stub = notification_pb2_grpc.NotificationServiceStub(self._channel)

    def list_notifications(
        self,
        is_read: bool | None = None,
        notification_type: str | None = None,
    ) -> list[NotificationData]:
        response = self._call(
            self._stub.ListNotifications,
            notification_pb2.ListNotificationsRequest(
                is_read=is_read, notification_type=notification_type
            ),
        )
        return [_notification(item) for item in response.notifications]

    def get_unread_count(self) -> int:
        return self._call(self._stub.GetUnreadCount, Empty()).unread

    def create_notification(
        self,
        *,
        notification_type: str,
        title: str,
        message: str,
        related_entity_id: str | None = None,
        user_id: str | None = None,
    ) -> NotificationData:
        return _notification(
            self._call(
                self._stub.CreateNotification,
                notification_pb2.CreateNotificationRequest(
                    notification_type=notification_type,
                    title=title,
                    message=message,
                    related_entity_id=related_entity_id,
                    user_id=user_id,
                ),
            )
        )

    def mark_notification_read(self, notification_id: str) -> NotificationData:
        return _notification(
            self._call(
                self._stub.MarkNotificationRead,
                notification_pb2.MarkNotificationReadRequest(id=notification_id),
            )
        )

    def mark_all_notifications_read(self) -> int:
        return self._call(self._stub.MarkAllNotificationsRead, Empty()).updated


class GrpcMarketDataClient(GrpcServiceClient):
    def __init__(self, addr: str) -> None:
        super().__init__(addr)
        self._stub = market_data_pb2_grpc.MarketDataServiceStub(self._channel)

    def sales_summary(self, product_id: str) -> SalesSummaryData:
        response = self._call(
            self._stub.SalesSummary,
            market_data_pb2.SalesSummaryRequest(product_id=product_id),
        )
        return SalesSummaryData(
            product_id=response.product_id,
            records=response.records,
            total_quantity=response.total_quantity,
            average_unit_price=Decimal(response.average_unit_price),
        )

    def list_sales(
        self, product_id: str | None = None, limit: int = 1000
    ) -> list[SalesRecordData]:
        response = self._call(
            self._stub.ListSales,
            market_data_pb2.ListSalesRequest(product_id=product_id, limit=limit),
        )
        return [_sales_record(item) for item in response.sales]

    def list_competitor_prices(
        self, product_id: str | None = None, limit: int = 1000
    ) -> list[CompetitorPriceData]:
        response = self._call(
            self._stub.ListCompetitorPrices,
            market_data_pb2.ListCompetitorPricesRequest(
                product_id=product_id, limit=limit
            ),
        )
        return [_competitor_price(item) for item in response.prices]


class GrpcAuthClient(GrpcServiceClient):
    def __init__(self, addr: str) -> None:
        super().__init__(addr)
        self._stub = identity_pb2_grpc.IdentityServiceStub(self._channel)

    def login(self, email: str, password: str) -> AuthPayloadData:
        response = self._call(
            self._stub.Login, identity_pb2.LoginRequest(email=email, password=password)
        )
        return _auth_payload(response)

    def register(
        self, email: str, password: str, full_name: str
    ) -> AuthPayloadData:
        response = self._call(
            self._stub.Register,
            identity_pb2.RegisterRequest(
                email=email, password=password, full_name=full_name
            ),
        )
        return _auth_payload(response)

    def logout(self, token: str) -> None:
        self._call(self._stub.Logout, identity_pb2.LogoutRequest(token=token))

    def introspect(self, token: str) -> AuthUserData:
        response = self._call(
            self._stub.Introspect, identity_pb2.IntrospectRequest(token=token)
        )
        return AuthUserData(
            id=response.user_id,
            email=response.email,
            full_name=response.full_name,
            roles=list(response.roles),
        )


def _auth_payload(msg) -> AuthPayloadData:
    return AuthPayloadData(
        token=msg.token,
        user=AuthUserData(
            id=msg.user.id,
            email=msg.user.email,
            full_name=msg.user.full_name,
            roles=list(msg.roles),
        ),
    )
