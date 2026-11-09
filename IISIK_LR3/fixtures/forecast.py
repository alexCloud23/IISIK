from __future__ import annotations

from decimal import Decimal

from fixtures.ids import FORECAST, PRODUCT, uid
from fixtures.models import DemandForecast, dt

FORECASTS: list[DemandForecast] = [
    DemandForecast(
        id=uid(FORECAST, 1),
        product_id=uid(PRODUCT, 1),
        period_start=dt(2026, 10, 13, 0),
        period_end=dt(2026, 10, 19, 0),
        predicted_demand=Decimal("42.50"),
        confidence=Decimal("0.8100"),
        model_version="naive-v1",
        created_at=dt(2026, 10, 12, 8),
    ),
    DemandForecast(
        id=uid(FORECAST, 2),
        product_id=uid(PRODUCT, 2),
        period_start=dt(2026, 10, 13, 0),
        period_end=dt(2026, 10, 19, 0),
        predicted_demand=Decimal("18.00"),
        confidence=Decimal("0.7400"),
        model_version="naive-v1",
        created_at=dt(2026, 10, 12, 8),
    ),
    DemandForecast(
        id=uid(FORECAST, 3),
        product_id=uid(PRODUCT, 3),
        period_start=dt(2026, 10, 13, 0),
        period_end=dt(2026, 10, 19, 0),
        predicted_demand=Decimal("95.00"),
        confidence=Decimal("0.6800"),
        model_version="naive-v1",
        created_at=dt(2026, 10, 12, 8),
    ),
    DemandForecast(
        id=uid(FORECAST, 4),
        product_id=uid(PRODUCT, 4),
        period_start=dt(2026, 10, 13, 0),
        period_end=dt(2026, 10, 19, 0),
        predicted_demand=Decimal("12.50"),
        confidence=Decimal("0.6200"),
        model_version="naive-v1",
        created_at=dt(2026, 10, 12, 8),
    ),
    DemandForecast(
        id=uid(FORECAST, 5),
        product_id=uid(PRODUCT, 1),
        period_start=dt(2026, 10, 20, 0),
        period_end=dt(2026, 10, 26, 0),
        predicted_demand=Decimal("46.00"),
        confidence=Decimal("0.9100"),
        model_version="naive-v1",
        created_at=dt(2026, 10, 19, 8),
    ),
]
