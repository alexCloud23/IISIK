from __future__ import annotations

from decimal import Decimal
from typing import Any, NoReturn

import httpx

from shared.errors import (
    DomainError,
    InvalidFilterError,
    InvalidIdError,
    InvalidInputError,
    InvalidOperationError,
    NotFoundError,
    UpstreamUnavailableError,
)

from ...dto import (
    AnalyticsResultData,
    ForecastData,
    NotificationData,
    ProductData,
    RecommendationData,
    RecommendationsSummaryData,
    SalesSummaryData,
    StrategyData,
)
from ..base import UNSET

_ERROR_CLASSES: dict[str, type[DomainError]] = {
    NotFoundError.code: NotFoundError,
    InvalidIdError.code: InvalidIdError,
    InvalidFilterError.code: InvalidFilterError,
    InvalidInputError.code: InvalidInputError,
    InvalidOperationError.code: InvalidOperationError,
}

_DEFAULT_MESSAGES: dict[type[DomainError], str] = {
    NotFoundError: "Объект не найден",
    InvalidIdError: "Некорректный идентификатор",
    InvalidFilterError: "Некорректный параметр фильтрации",
    InvalidInputError: "Некорректные данные запроса",
    InvalidOperationError: "Операция недопустима",
}


def _payload(response: httpx.Response) -> dict[str, Any] | None:
    try:
        data = response.json()
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def _message(response: httpx.Response) -> str | None:
    payload = _payload(response)
    if payload:
        message = payload.get("message")
        return str(message) if message else None
    return None


def _code(response: httpx.Response) -> str | None:
    payload = _payload(response)
    if payload:
        code = payload.get("code")
        return str(code) if code else None
    return None


def _raise_domain_error(response: httpx.Response, base_url: Any) -> NoReturn:
    message = _message(response)
    code = _code(response)
    error_cls = _ERROR_CLASSES.get(code) if code else None
    if error_cls is None:
        status = response.status_code
        if status == 422:
            error_cls = InvalidIdError
        elif status == 400:
            error_cls = InvalidInputError
        elif status == 409:
            error_cls = InvalidOperationError
        elif status == 404:
            error_cls = NotFoundError
        else:
            raise UpstreamUnavailableError(
                message
                or f"Сервис {base_url} вернул ошибку {status}"
            )
    if message is None:
        message = _DEFAULT_MESSAGES.get(error_cls, "Ошибка сервиса")
    raise error_cls(message)


class HttpServiceClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 2.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url, timeout=timeout, transport=transport
        )

    def close(self) -> None:
        self._client.close()

    def _get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> httpx.Response | None:
        filtered = {key: value for key, value in (params or {}).items() if value is not None}
        try:
            response = self._client.get(path, params=filtered or None)
        except httpx.HTTPError as exc:
            raise UpstreamUnavailableError(
                f"Сервис {self._client.base_url} недоступен: {exc.__class__.__name__}"
            ) from exc

        if response.status_code == 404:
            return None
        if response.status_code >= 500:
            raise UpstreamUnavailableError(
                _message(response)
                or f"Сервис {self._client.base_url} вернул ошибку {response.status_code}"
            )
        if response.status_code >= 400:
            _raise_domain_error(response, self._client.base_url)
        response.raise_for_status()
        return response

    def _send(
        self,
        method: str,
        path: str,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        filtered = {key: value for key, value in (params or {}).items() if value is not None}
        try:
            response = self._client.request(
                method, path, json=json_body, params=filtered or None
            )
        except httpx.HTTPError as exc:
            raise UpstreamUnavailableError(
                f"Сервис {self._client.base_url} недоступен: {exc.__class__.__name__}"
            ) from exc

        if response.status_code == 404:
            raise NotFoundError(
                _message(response) or f"Объект не найден: {path}"
            )
        if response.status_code >= 500:
            raise UpstreamUnavailableError(
                _message(response)
                or f"Сервис {self._client.base_url} вернул ошибку {response.status_code}"
            )
        if response.status_code >= 400:
            _raise_domain_error(response, self._client.base_url)
        response.raise_for_status()
        return response

    @staticmethod
    def _money(value: Decimal | None) -> str | None:
        return None if value is None else str(value)


class HttpProductClient(HttpServiceClient):
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
        response = self._get(
            "/products",
            {
                "category": category,
                "is_active": is_active,
                "search": search,
                "min_price": self._money(min_price),
                "max_price": self._money(max_price),
                "sort": sort,
                "order": order,
            },
        )
        assert response is not None
        return [ProductData.model_validate(item) for item in response.json()]

    def get_product(self, product_id: str) -> ProductData | None:
        response = self._get(f"/products/{product_id}")
        return ProductData.model_validate(response.json()) if response else None

    def create_product(
        self,
        *,
        name: str,
        description: str | None,
        category: str,
        base_price: Decimal,
        currency: str,
    ) -> ProductData:
        response = self._send(
            "POST",
            "/products",
            {
                "name": name,
                "description": description,
                "category": category,
                "base_price": self._money(base_price),
                "currency": currency,
            },
        )
        return ProductData.model_validate(response.json())

    def update_product(
        self,
        product_id: str,
        *,
        base_price: Decimal | None = UNSET,
        description: str | None = UNSET,
        is_active: bool | None = UNSET,
    ) -> ProductData:
        body: dict[str, Any] = {}
        if base_price is not UNSET:
            body["base_price"] = self._money(base_price)
        if description is not UNSET:
            body["description"] = description
        if is_active is not UNSET:
            body["is_active"] = is_active
        response = self._send("PATCH", f"/products/{product_id}", body)
        return ProductData.model_validate(response.json())


class HttpForecastClient(HttpServiceClient):
    def list_forecasts(self, product_id: str | None = None) -> list[ForecastData]:
        response = self._get("/forecasts", {"product_id": product_id})
        assert response is not None
        return [ForecastData.model_validate(item) for item in response.json()]


class HttpStrategyClient(HttpServiceClient):
    def list_strategies(self, product_id: str | None = None) -> list[StrategyData]:
        response = self._get("/strategies", {"product_id": product_id})
        assert response is not None
        return [StrategyData.model_validate(item) for item in response.json()]


class HttpRecommendationClient(HttpServiceClient):
    def list_recommendations(
        self,
        product_id: str | None = None,
        status: str | None = None,
        sort: str = "created",
        order: str = "desc",
    ) -> list[RecommendationData]:
        response = self._get(
            "/recommendations",
            {
                "product_id": product_id,
                "status": status,
                "sort": sort,
                "order": order,
            },
        )
        assert response is not None
        return [RecommendationData.model_validate(item) for item in response.json()]

    def get_recommendation(
        self, recommendation_id: str
    ) -> RecommendationData | None:
        response = self._get(f"/recommendations/{recommendation_id}")
        if response is None:
            return None
        return RecommendationData.model_validate(response.json())

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
        response = self._send(
            "POST",
            "/recommendations",
            {
                "product_id": product_id,
                "forecast_id": forecast_id,
                "current_price": self._money(current_price),
                "strategy_type": strategy_type,
                "competitor_price": self._money(competitor_price),
                "strategy_id": strategy_id,
            },
        )
        return RecommendationData.model_validate(response.json())

    def decide_recommendation(
        self, recommendation_id: str, decision: str
    ) -> RecommendationData:
        response = self._send(
            "PATCH",
            f"/recommendations/{recommendation_id}/decision",
            {"decision": decision},
        )
        return RecommendationData.model_validate(response.json())

    def recommendations_summary(self) -> RecommendationsSummaryData:
        response = self._send("GET", "/recommendations/summary")
        return RecommendationsSummaryData.model_validate(response.json())


class HttpAnalyticsClient(HttpServiceClient):
    def list_results(
        self, analysis_type: str | None = None
    ) -> list[AnalyticsResultData]:
        response = self._get(
            "/analytics-results", {"analysis_type": analysis_type}
        )
        assert response is not None
        return [AnalyticsResultData.model_validate(item) for item in response.json()]


class HttpNotificationClient(HttpServiceClient):
    def list_notifications(
        self,
        is_read: bool | None = None,
        notification_type: str | None = None,
    ) -> list[NotificationData]:
        response = self._get(
            "/notifications",
            {"is_read": is_read, "notification_type": notification_type},
        )
        assert response is not None
        return [NotificationData.model_validate(item) for item in response.json()]

    def get_unread_count(self) -> int:
        response = self._send("GET", "/notifications/unread-count")
        payload = response.json()
        return int(payload.get("unread", 0))

    def create_notification(
        self,
        *,
        notification_type: str,
        title: str,
        message: str,
        related_entity_id: str | None = None,
        user_id: str | None = None,
    ) -> NotificationData:
        response = self._send(
            "POST",
            "/notifications",
            {
                "notification_type": notification_type,
                "title": title,
                "message": message,
                "related_entity_id": related_entity_id,
                "user_id": user_id,
            },
        )
        return NotificationData.model_validate(response.json())

    def mark_notification_read(self, notification_id: str) -> NotificationData:
        response = self._send(
            "PATCH", f"/notifications/{notification_id}/read"
        )
        return NotificationData.model_validate(response.json())

    def mark_all_notifications_read(self) -> int:
        response = self._send("POST", "/notifications/read-all")
        payload = response.json()
        return int(payload.get("updated", 0))


class HttpMarketDataClient(HttpServiceClient):
    def sales_summary(self, product_id: str) -> SalesSummaryData:
        response = self._send(
            "GET", "/sales-summary", params={"product_id": product_id}
        )
        return SalesSummaryData.model_validate(response.json())
