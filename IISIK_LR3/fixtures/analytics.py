from __future__ import annotations

from fixtures.ids import ANALYTICS, PRODUCT, RECOMMENDATION, uid
from fixtures.models import AnalyticsResult, dt

ANALYTICS_RESULTS: list[AnalyticsResult] = [
    AnalyticsResult(
        id=uid(ANALYTICS, 1),
        product_id=uid(PRODUCT, 1),
        recommendation_id=None,
        analysis_type="PRICE_HISTORY",
        metrics={"avg_price": 1257.33, "min_price": 1199.0, "max_price": 1299.0},
        created_at=dt(2026, 10, 16, 9),
    ),
    AnalyticsResult(
        id=uid(ANALYTICS, 2),
        product_id=uid(PRODUCT, 2),
        recommendation_id=None,
        analysis_type="SALES_SUMMARY",
        metrics={"total_quantity": 11, "revenue": 37357.0},
        created_at=dt(2026, 10, 16, 10),
    ),
    AnalyticsResult(
        id=uid(ANALYTICS, 3),
        product_id=uid(PRODUCT, 1),
        recommendation_id=uid(RECOMMENDATION, 1),
        analysis_type="FORECAST_VS_FACT",
        metrics={"predicted_demand": 42.5, "fact_demand": 39.0, "deviation": -8.2},
        created_at=dt(2026, 10, 17, 11),
    ),
]
