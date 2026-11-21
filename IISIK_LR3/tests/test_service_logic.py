from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest

from fixtures.ids import FORECAST, NOTIFICATION, PRODUCT, RECOMMENDATION, uid

P1 = uid(PRODUCT, 1)
P5 = uid(PRODUCT, 5)
F1 = uid(FORECAST, 1)
F_UNKNOWN = uid(FORECAST, 999)
R1 = uid(RECOMMENDATION, 1)
R3 = uid(RECOMMENDATION, 3)
N1 = uid(NOTIFICATION, 1)


@pytest.fixture()
def product_session():
    from services.product_service.app import seed as seed_module
    from services.product_service.app.db import SessionLocal

    with SessionLocal() as session:
        seed_module.seed(session)
        yield session


class TestProductService:
    def test_create_product(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductCreateDTO

        dto = service.create_product(
            product_session,
            ProductCreateDTO(
                name="Тестовый товар", category="Электроника", base_price=Decimal("123.45")
            ),
        )
        assert dto.is_active is True
        assert dto.base_price == Decimal("123.45")
        assert dto.currency == "BYN"
        assert UUID(dto.id)

    def test_create_duplicate_name_rejected(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductCreateDTO
        from shared.errors import InvalidOperationError

        payload = ProductCreateDTO(name="Смартфон X200", category="Электроника", base_price=Decimal("10"))
        with pytest.raises(InvalidOperationError):
            service.create_product(product_session, payload)

    def test_create_non_positive_price_rejected(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductCreateDTO
        from shared.errors import InvalidInputError

        payload = ProductCreateDTO(name="Дешёвый", category="Прочее", base_price=Decimal("0"))
        with pytest.raises(InvalidInputError):
            service.create_product(product_session, payload)

    def test_create_empty_name_rejected(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductCreateDTO
        from shared.errors import InvalidInputError

        payload = ProductCreateDTO(name="   ", category="Прочее", base_price=Decimal("10"))
        with pytest.raises(InvalidInputError):
            service.create_product(product_session, payload)

    def test_update_price(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductUpdateDTO

        dto = service.update_product(
            product_session, P1, ProductUpdateDTO(base_price=Decimal("999.99"))
        )
        assert dto.base_price == Decimal("999.99")

    def test_update_price_of_inactive_product_rejected(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductUpdateDTO
        from shared.errors import InvalidOperationError

        with pytest.raises(InvalidOperationError):
            service.update_product(
                product_session, P5, ProductUpdateDTO(base_price=Decimal("999.99"))
            )

    def test_deactivate_inactive_product_allowed(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductUpdateDTO

        dto = service.update_product(product_session, P5, ProductUpdateDTO(is_active=True))
        assert dto.is_active is True

    def test_update_unknown_product_rejected(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductUpdateDTO
        from shared.errors import NotFoundError

        with pytest.raises(NotFoundError):
            service.update_product(
                product_session, uid(PRODUCT, 999), ProductUpdateDTO(is_active=False)
            )

    def test_update_price_writes_history(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductUpdateDTO

        before = service.list_price_history(product_session, P1)
        service.update_product(
            product_session, P1, ProductUpdateDTO(base_price=Decimal("999.99"))
        )
        history = service.list_price_history(product_session, P1)
        assert len(history) == len(before) + 1
        assert history[0].old_price == Decimal("1299.00")
        assert history[0].new_price == Decimal("999.99")
        assert history[0].currency == "BYN"

    def test_update_same_price_skips_history(self, product_session):
        from services.product_service.app import service
        from services.product_service.app.schemas import ProductUpdateDTO

        before = service.list_price_history(product_session, P1)
        service.update_product(
            product_session, P1, ProductUpdateDTO(base_price=Decimal("1299.00"))
        )
        assert len(service.list_price_history(product_session, P1)) == len(before)


@pytest.fixture()
def pricing_session():
    from services.pricing_service.app import seed as seed_module
    from services.pricing_service.app.db import SessionLocal

    with SessionLocal() as session:
        seed_module.seed(session)
        yield session


class TestPricingService:
    def test_create_recommendation_computes_price(self, pricing_session):
        from services.pricing_service.app import service
        from services.pricing_service.app.schemas import RecommendationCreateDTO

        dto = service.create_recommendation(
            pricing_session,
            RecommendationCreateDTO(
                product_id=P1,
                forecast_id=F1,
                current_price=Decimal("1299.00"),
                strategy_type="UNDERCUT",
                competitor_price=Decimal("1149.00"),
            ),
        )
        assert dto.status == "NEW"
        assert dto.recommended_price == Decimal("1137.51")
        assert "UNDERCUT" in dto.reason

    def test_create_recommendation_unknown_strategy_rejected(self, pricing_session):
        from services.pricing_service.app import service
        from services.pricing_service.app.schemas import RecommendationCreateDTO
        from shared.errors import InvalidInputError

        payload = RecommendationCreateDTO(
            product_id=P1,
            forecast_id=F1,
            current_price=Decimal("1299.00"),
            strategy_type="AGGRESSIVE",
            competitor_price=Decimal("999.00"),
        )
        with pytest.raises(InvalidInputError):
            service.create_recommendation(pricing_session, payload)

    def test_create_recommendation_unknown_forecast_rejected(self, pricing_session):
        from services.pricing_service.app import service
        from services.pricing_service.app.schemas import RecommendationCreateDTO
        from shared.errors import NotFoundError

        payload = RecommendationCreateDTO(
            product_id=P1,
            forecast_id=F_UNKNOWN,
            current_price=Decimal("1299.00"),
        )
        with pytest.raises(NotFoundError):
            service.create_recommendation(pricing_session, payload)

    def test_decide_recommendation(self, pricing_session):
        from services.pricing_service.app import service

        dto = service.decide_recommendation(pricing_session, R1, "ACCEPTED")
        assert dto.status == "ACCEPTED"

    def test_decide_twice_rejected(self, pricing_session):
        from services.pricing_service.app import service
        from shared.errors import InvalidOperationError

        service.decide_recommendation(pricing_session, R1, "ACCEPTED")
        with pytest.raises(InvalidOperationError):
            service.decide_recommendation(pricing_session, R1, "REJECTED")

    def test_decide_already_processed_rejected(self, pricing_session):
        from services.pricing_service.app import service
        from shared.errors import InvalidOperationError

        with pytest.raises(InvalidOperationError):
            service.decide_recommendation(pricing_session, R3, "REJECTED")

    def test_decide_unknown_decision_rejected(self, pricing_session):
        from services.pricing_service.app import service
        from shared.errors import InvalidInputError

        with pytest.raises(InvalidInputError):
            service.decide_recommendation(pricing_session, R1, "MAYBE")

    def test_summary_counts(self, pricing_session):
        from services.pricing_service.app import service

        service.decide_recommendation(pricing_session, R1, "ACCEPTED")
        summary = service.recommendations_summary(pricing_session)
        assert summary == {"total": 4, "new": 1, "accepted": 2, "rejected": 1}


@pytest.fixture()
def notification_session():
    from services.notification_service.app import seed as seed_module
    from services.notification_service.app.db import SessionLocal

    with SessionLocal() as session:
        seed_module.seed(session)
        yield session


class TestNotificationService:
    def test_create_notification(self, notification_session):
        from services.notification_service.app import service
        from services.notification_service.app.schemas import NotificationCreateDTO

        dto = service.create_notification(
            notification_session,
            NotificationCreateDTO(
                notification_type="RECOMMENDATION_CREATED",
                title="Заголовок",
                message="Сообщение",
                related_entity_id=R1,
            ),
        )
        assert dto.status == "SENT"
        assert dto.is_read is False
        assert dto.sent_at is not None
        assert dto.user_id == "10000000-0000-4000-8000-000000000001"

    def test_create_notification_empty_type_rejected(self, notification_session):
        from services.notification_service.app import service
        from services.notification_service.app.schemas import NotificationCreateDTO
        from shared.errors import InvalidInputError

        payload = NotificationCreateDTO(notification_type="", title="t", message="m")
        with pytest.raises(InvalidInputError):
            service.create_notification(notification_session, payload)

    def test_mark_notification_read_idempotent(self, notification_session):
        from services.notification_service.app import service

        first = service.mark_notification_read(notification_session, N1)
        assert first.is_read is True
        second = service.mark_notification_read(notification_session, N1)
        assert second.is_read is True

    def test_mark_notification_read_unknown_rejected(self, notification_session):
        from services.notification_service.app import service
        from shared.errors import NotFoundError

        with pytest.raises(NotFoundError):
            service.mark_notification_read(notification_session, uid(NOTIFICATION, 999))

    def test_mark_all_read_counts_new_only(self, notification_session):
        from services.notification_service.app import service

        assert service.mark_all_notifications_read(notification_session) == 2
        assert service.mark_all_notifications_read(notification_session) == 0

    def test_list_with_type_filter(self, notification_session):
        from services.notification_service.app import service

        items = service.list_notifications(notification_session, None, "FORECAST_READY")
        assert len(items) == 1
        assert items[0].notification_type == "FORECAST_READY"


@pytest.fixture()
def market_session():
    from services.market_data_service.app import seed as seed_module
    from services.market_data_service.app.db import SessionLocal

    with SessionLocal() as session:
        seed_module.seed(session)
        yield session


class TestMarketDataService:
    def test_sales_summary_weighted_average(self, market_session):
        from services.market_data_service.app import service

        summary = service.get_sales_summary(market_session, P1)
        assert summary.records == 6
        assert summary.total_quantity == 39
        assert summary.average_unit_price.quantize(Decimal("0.01")) == Decimal(
            "1255.67"
        )


@pytest.fixture()
def forecast_session():
    from services.demand_forecast_service.app import seed as seed_module
    from services.demand_forecast_service.app.db import SessionLocal

    with SessionLocal() as session:
        seed_module.seed(session)
        yield session


class TestDemandForecastService:
    def test_generate_forecast_computes_and_persists(self, forecast_session):
        from services.demand_forecast_service.app import service
        from services.demand_forecast_service.app.schemas import (
            ForecastGenerateDTO,
            SalePointDTO,
        )

        dto = service.generate_forecast(
            forecast_session,
            ForecastGenerateDTO(
                product_id=P1,
                period_days=7,
                sales=[
                    SalePointDTO(quantity=10, sold_at=datetime(2026, 10, 1)),
                    SalePointDTO(quantity=20, sold_at=datetime(2026, 10, 2)),
                ],
            ),
        )
        assert dto.predicted_demand == Decimal("105.00")
        assert dto.confidence == Decimal("0.6000")
        assert dto.model_version == "sma-v1"
        stored = service.get_forecast(forecast_session, dto.id)
        assert stored.predicted_demand == Decimal("105.00")

    def test_generate_forecast_without_sales_rejected(self, forecast_session):
        from services.demand_forecast_service.app import service
        from services.demand_forecast_service.app.schemas import ForecastGenerateDTO
        from shared.errors import InvalidInputError

        with pytest.raises(InvalidInputError):
            service.generate_forecast(
                forecast_session,
                ForecastGenerateDTO(product_id=P1, period_days=7, sales=[]),
            )

    def test_generate_forecast_bad_period_rejected(self, forecast_session):
        from services.demand_forecast_service.app import service
        from services.demand_forecast_service.app.schemas import (
            ForecastGenerateDTO,
            SalePointDTO,
        )
        from shared.errors import InvalidInputError

        with pytest.raises(InvalidInputError):
            service.generate_forecast(
                forecast_session,
                ForecastGenerateDTO(
                    product_id=P1,
                    period_days=0,
                    sales=[SalePointDTO(quantity=1, sold_at=datetime(2026, 10, 1))],
                ),
            )


@pytest.fixture()
def strategy_session():
    from services.competitive_strategy_service.app import seed as seed_module
    from services.competitive_strategy_service.app.db import SessionLocal

    with SessionLocal() as session:
        seed_module.seed(session)
        yield session


class TestCompetitiveStrategyService:
    def test_analyze_strategy_computes_and_persists(self, strategy_session):
        from services.competitive_strategy_service.app import service
        from services.competitive_strategy_service.app.schemas import (
            CompetitorPricePointDTO,
            StrategyAnalyzeDTO,
        )

        dto = service.analyze_strategy(
            strategy_session,
            StrategyAnalyzeDTO(
                product_id=P1,
                current_price=Decimal("1299.00"),
                competitor_prices=[
                    CompetitorPricePointDTO(
                        competitor_name="TechnoMarket", price=Decimal("1249.00")
                    ),
                    CompetitorPricePointDTO(
                        competitor_name="GadgetShop", price=Decimal("1149.00")
                    ),
                ],
            ),
        )
        assert dto.strategy_type == "UNDERCUT"
        assert dto.competitor_price == Decimal("1149.00")
        assert dto.competitor_name == "GadgetShop"
        stored = service.list_strategies(strategy_session, P1)
        assert any(item.id == dto.id for item in stored)

    def test_analyze_strategy_without_competitors_rejected(self, strategy_session):
        from services.competitive_strategy_service.app import service
        from services.competitive_strategy_service.app.schemas import (
            StrategyAnalyzeDTO,
        )
        from shared.errors import InvalidInputError

        with pytest.raises(InvalidInputError):
            service.analyze_strategy(
                strategy_session,
                StrategyAnalyzeDTO(
                    product_id=P1,
                    current_price=Decimal("1299.00"),
                    competitor_prices=[],
                ),
            )


@pytest.fixture()
def analytics_session():
    from services.analytics_service.app import seed as seed_module
    from services.analytics_service.app.db import SessionLocal

    with SessionLocal() as session:
        seed_module.seed(session)
        yield session


class TestAnalyticsService:
    def test_run_analysis_computes_and_persists(self, analytics_session):
        from services.analytics_service.app import service
        from services.analytics_service.app.schemas import AnalyticsRunDTO

        dto = service.run_analysis(
            analytics_session,
            AnalyticsRunDTO(
                product_id=P1,
                records=6,
                total_quantity=39,
                average_unit_price=Decimal("1255.67"),
                predicted_demand=Decimal("42.50"),
                current_price=Decimal("1299.00"),
                recommended_price=Decimal("1249.00"),
                recommendation_id=R1,
            ),
        )
        assert dto.analysis_type == "SALES_SUMMARY"
        assert dto.metrics["total_quantity"] == 39
        assert dto.metrics["revenue"] == pytest.approx(1255.67 * 39)
        assert dto.metrics["predicted_demand"] == 42.5
        assert dto.metrics["price_change_percent"] == pytest.approx(-3.85, abs=0.01)
        stored = service.list_results(analytics_session, "SALES_SUMMARY")
        assert any(item.id == dto.id for item in stored)
