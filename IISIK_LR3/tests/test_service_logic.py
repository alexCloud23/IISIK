from __future__ import annotations

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
