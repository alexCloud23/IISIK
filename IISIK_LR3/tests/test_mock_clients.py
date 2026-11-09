from __future__ import annotations

from decimal import Decimal

import pytest

from fixtures.market_data import SALES
from fixtures.notification import NOTIFICATIONS
from fixtures.pricing import RECOMMENDATIONS
from fixtures.product import PRODUCTS
from gateway.app.dto import (
    ForecastData,
    NotificationData,
    ProductData,
    RecommendationData,
    SalesRecordData,
)
from gateway.app.clients.mock.clients import (
    MockMarketDataClient,
    MockNotificationClient,
    MockProductClient,
    MockRecommendationClient,
)
from shared.errors import (
    InvalidInputError,
    InvalidOperationError,
    NotFoundError,
)

P1 = "20000000-0000-4000-8000-000000000001"
F1 = "50000000-0000-4000-8000-000000000001"


@pytest.fixture()
def product_client() -> MockProductClient:
    return MockProductClient([ProductData.model_validate(item) for item in PRODUCTS])


@pytest.fixture()
def recommendation_client() -> MockRecommendationClient:
    return MockRecommendationClient(
        [RecommendationData.model_validate(item) for item in RECOMMENDATIONS],
        [
            ForecastData.model_validate(item)
            for item in __import__("fixtures.forecast", fromlist=["FORECASTS"]).FORECASTS
        ],
    )


@pytest.fixture()
def notification_client() -> MockNotificationClient:
    return MockNotificationClient(
        [NotificationData.model_validate(item) for item in NOTIFICATIONS]
    )


class TestMockProductClient:
    def test_create_appends(self, product_client):
        created = product_client.create_product(
            name="Новый товар",
            description=None,
            category="Прочее",
            base_price=Decimal("100.00"),
            currency="BYN",
        )
        assert created.is_active is True
        assert any(item.name == "Новый товар" for item in product_client._products)

    def test_create_duplicate_name_rejected(self, product_client):
        with pytest.raises(InvalidOperationError):
            product_client.create_product(
                name="смартфон x200",
                description=None,
                category="Электроника",
                base_price=Decimal("1"),
                currency="BYN",
            )

    def test_update_price_of_inactive_rejected(self, product_client):
        inactive = next(item for item in product_client._products if not item.is_active)
        with pytest.raises(InvalidOperationError):
            product_client.update_product(inactive.id, base_price=Decimal("10"))

    def test_update_unknown_rejected(self, product_client):
        with pytest.raises(NotFoundError):
            product_client.update_product(
                "20000000-0000-4000-8000-000000000999", base_price=Decimal("10")
            )

    def test_create_bad_price_rejected(self, product_client):
        with pytest.raises(InvalidInputError):
            product_client.create_product(
                name="X", description=None, category="C", base_price=Decimal("-5"), currency="BYN"
            )

    def test_filters_and_sort(self, product_client):
        items = product_client.list_products(
            category="Электроника", sort="price", order="desc"
        )
        assert [item.base_price for item in items] == [Decimal("3499.00"), Decimal("1299.00"), Decimal("249.00")]
        assert product_client.list_products(search="pro")[0].name == "Ноутбук Pro 15"


class TestMockRecommendationClient:
    def test_create_computes_price_and_appends(self, recommendation_client):
        dto = recommendation_client.create_recommendation(
            product_id=P1,
            forecast_id=F1,
            current_price=Decimal("1299.00"),
            strategy_type="UNDERCUT",
            competitor_price=Decimal("1149.00"),
        )
        assert dto.status == "NEW"
        assert dto.recommended_price == Decimal("1137.51")
        assert dto in recommendation_client._recommendations

    def test_decide_only_new(self, recommendation_client):
        dto = recommendation_client.decide_recommendation(RECOMMENDATIONS[0].id, "ACCEPTED")
        assert dto.status == "ACCEPTED"
        with pytest.raises(InvalidOperationError):
            recommendation_client.decide_recommendation(RECOMMENDATIONS[0].id, "REJECTED")

    def test_decide_already_processed(self, recommendation_client):
        with pytest.raises(InvalidOperationError):
            recommendation_client.decide_recommendation(RECOMMENDATIONS[2].id, "REJECTED")

    def test_summary(self, recommendation_client):
        summary = recommendation_client.recommendations_summary()
        assert (summary.total, summary.new, summary.accepted, summary.rejected) == (4, 2, 1, 1)

    def test_create_unknown_forecast(self, recommendation_client):
        with pytest.raises(NotFoundError):
            recommendation_client.create_recommendation(
                product_id=P1,
                forecast_id="50000000-0000-4000-8000-000000000999",
                current_price=Decimal("1299.00"),
            )


class TestMockNotificationClient:
    def test_create_uses_default_user(self, notification_client):
        dto = notification_client.create_notification(
            notification_type="DECISION_ACCEPTED",
            title="Заголовок",
            message="Сообщение",
        )
        assert dto.user_id == "10000000-0000-4000-8000-000000000001"
        assert dto.is_read is False
        assert dto in notification_client._notifications

    def test_unread_count_and_mark_all(self, notification_client):
        assert notification_client.get_unread_count() == 2
        assert notification_client.mark_all_notifications_read() == 2
        assert notification_client.get_unread_count() == 0

    def test_mark_read_unknown(self, notification_client):
        with pytest.raises(NotFoundError):
            notification_client.mark_notification_read(
                "90000000-0000-4000-8000-000000000999"
            )

    def test_type_filter(self, notification_client):
        items = notification_client.list_notifications(notification_type="FORECAST_READY")
        assert len(items) == 1


class TestMockMarketDataClient:
    def test_sales_summary_values(self):
        client = MockMarketDataClient(
            [SalesRecordData.model_validate(item) for item in SALES]
        )
        summary = client.sales_summary(P1)
        assert summary.records == 6
        assert summary.total_quantity == 39
        assert round(summary.average_unit_price, 2) == Decimal("1262.33")

    def test_sales_summary_bad_uuid(self):
        client = MockMarketDataClient([SalesRecordData.model_validate(item) for item in SALES])
        with pytest.raises(Exception):
            client.sales_summary("не-uuid")


class TestFixturesNotMutated:
    def test_create_product_does_not_touch_fixtures(self, product_client):
        product_client.create_product(
            name="Ещё товар", description=None, category="Прочее",
            base_price=Decimal("1"), currency="BYN",
        )
        assert len(PRODUCTS) == 5
        assert all(item.name != "Ещё товар" for item in PRODUCTS)

    def test_decide_does_not_touch_fixtures(self, recommendation_client):
        recommendation_client.decide_recommendation(RECOMMENDATIONS[0].id, "ACCEPTED")
        assert RECOMMENDATIONS[0].status == "NEW"
