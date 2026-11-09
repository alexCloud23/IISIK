from __future__ import annotations

from decimal import Decimal

from fixtures.ids import FORECAST, PRODUCT, RECOMMENDATION, STRATEGY, uid
from fixtures.models import PriceRecommendation, dt

RECOMMENDATIONS: list[PriceRecommendation] = [
    PriceRecommendation(
        id=uid(RECOMMENDATION, 1),
        product_id=uid(PRODUCT, 1),
        forecast_id=uid(FORECAST, 1),
        strategy_id=uid(STRATEGY, 1),
        current_price=Decimal("1299.00"),
        recommended_price=Decimal("1249.00"),
        currency="BYN",
        reason=(
            "Прогноз спроса 42,5 ед. и цена конкурента 1249,00 BYN поддерживают "
            "снижение цены для удержания объёма продаж."
        ),
        status="NEW",
        created_at=dt(2026, 10, 13, 9),
    ),
    PriceRecommendation(
        id=uid(RECOMMENDATION, 2),
        product_id=uid(PRODUCT, 2),
        forecast_id=uid(FORECAST, 2),
        strategy_id=uid(STRATEGY, 3),
        current_price=Decimal("3499.00"),
        recommended_price=Decimal("3599.00"),
        currency="BYN",
        reason=(
            "Ожидаемый спрос 18 ед. и стратегия PREMIUM позволяют повысить цену "
            "на 2,9% без существенного снижения объёма."
        ),
        status="NEW",
        created_at=dt(2026, 10, 13, 10),
    ),
    PriceRecommendation(
        id=uid(RECOMMENDATION, 3),
        product_id=uid(PRODUCT, 3),
        forecast_id=uid(FORECAST, 3),
        strategy_id=None,
        current_price=Decimal("249.00"),
        recommended_price=Decimal("239.00"),
        currency="BYN",
        reason=(
            "Снижение цены до 239,00 BYN соответствует ценам конкурентов "
            "и прогнозу спроса 95 ед."
        ),
        status="ACCEPTED",
        created_at=dt(2026, 10, 14, 9),
    ),
    PriceRecommendation(
        id=uid(RECOMMENDATION, 4),
        product_id=uid(PRODUCT, 4),
        forecast_id=uid(FORECAST, 4),
        strategy_id=uid(STRATEGY, 4),
        current_price=Decimal("2799.00"),
        recommended_price=Decimal("2699.00"),
        currency="BYN",
        reason=(
            "Снижение на 3,6% не компенсируется прогнозируемым спросом 12,5 ед., "
            "рекомендация отклонена."
        ),
        status="REJECTED",
        created_at=dt(2026, 10, 15, 11),
    ),
]
