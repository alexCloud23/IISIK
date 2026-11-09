from __future__ import annotations

from decimal import Decimal

from fixtures.ids import PRODUCT, STRATEGY, uid
from fixtures.models import CompetitorStrategy, dt

STRATEGIES: list[CompetitorStrategy] = [
    CompetitorStrategy(
        id=uid(STRATEGY, 1),
        product_id=uid(PRODUCT, 1),
        competitor_name="TechnoMarket",
        strategy_type="MATCH",
        competitor_price=Decimal("1249.00"),
        price_change_percent=Decimal("0.00"),
        estimated_probability=Decimal("0.5500"),
        created_at=dt(2026, 10, 6, 9),
    ),
    CompetitorStrategy(
        id=uid(STRATEGY, 2),
        product_id=uid(PRODUCT, 1),
        competitor_name="GadgetShop",
        strategy_type="UNDERCUT",
        competitor_price=Decimal("1149.00"),
        price_change_percent=Decimal("-8.00"),
        estimated_probability=Decimal("0.4000"),
        created_at=dt(2026, 10, 6, 9),
    ),
    CompetitorStrategy(
        id=uid(STRATEGY, 3),
        product_id=uid(PRODUCT, 2),
        competitor_name="TechnoMarket",
        strategy_type="PREMIUM",
        competitor_price=Decimal("3674.00"),
        price_change_percent=Decimal("5.00"),
        estimated_probability=Decimal("0.3500"),
        created_at=dt(2026, 10, 7, 10),
    ),
    CompetitorStrategy(
        id=uid(STRATEGY, 4),
        product_id=uid(PRODUCT, 4),
        competitor_name="HomeTech",
        strategy_type="UNDERCUT",
        competitor_price=Decimal("2599.00"),
        price_change_percent=Decimal("-4.00"),
        estimated_probability=Decimal("0.7500"),
        created_at=dt(2026, 10, 7, 10),
    ),
]
