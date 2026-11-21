from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from shared.errors import InvalidInputError
from shared.pricing_rules import round_money

MIN_PERIOD_DAYS = 1
MAX_PERIOD_DAYS = 90
MODEL_VERSION = "sma-v1"

_CONFIDENCE_BASE = Decimal("0.5")
_CONFIDENCE_STEP = Decimal("0.05")
_CONFIDENCE_MAX = Decimal("0.95")


def validate_period_days(period_days: int) -> int:
    if not MIN_PERIOD_DAYS <= period_days <= MAX_PERIOD_DAYS:
        raise InvalidInputError(
            f"period_days должен быть в диапазоне "
            f"{MIN_PERIOD_DAYS}..{MAX_PERIOD_DAYS}"
        )
    return period_days


def compute_demand_forecast(
    sales: list[tuple[datetime, int]], period_days: int
) -> tuple[Decimal, Decimal]:
    if not sales:
        raise InvalidInputError("Нет данных о продажах для прогноза")
    total = sum(quantity for _, quantity in sales)
    span = (max(day for day, _ in sales) - min(day for day, _ in sales)).days + 1
    predicted = round_money(Decimal(total) / span * period_days)
    confidence = min(
        _CONFIDENCE_MAX, _CONFIDENCE_BASE + _CONFIDENCE_STEP * len(sales)
    )
    return predicted, confidence.quantize(Decimal("0.0001"))
