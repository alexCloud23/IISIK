from __future__ import annotations

from decimal import Decimal

from shared.errors import InvalidInputError
from shared.pricing_rules import STRATEGY_TYPES, round_money
from shared.validation import validate_positive_price

MATCH_TOLERANCE = Decimal("0.02")


def analyze_competitor_strategy(
    current_price: Decimal | float | str,
    competitor_prices: list[Decimal | float | str],
) -> tuple[str, Decimal, Decimal, Decimal]:
    current = validate_positive_price(current_price, "current_price")
    if not competitor_prices:
        raise InvalidInputError("Нет данных о ценах конкурентов")
    prices = [
        validate_positive_price(price, "competitor_price")
        for price in competitor_prices
    ]

    average = round_money(sum(prices) / len(prices))
    lowest = min(prices)
    deviation = (average - current) / current

    if abs(deviation) <= MATCH_TOLERANCE:
        strategy_type = "MATCH"
        reference_price = average
    elif deviation < 0:
        strategy_type = "UNDERCUT"
        reference_price = lowest
    else:
        strategy_type = "PREMIUM"
        reference_price = average

    change_percent = (deviation * 100).quantize(Decimal("0.01"))
    probability = max(
        Decimal("0.3"), Decimal("1") - abs(deviation) * 2
    ).quantize(Decimal("0.0001"))
    assert strategy_type in STRATEGY_TYPES
    return strategy_type, reference_price, change_percent, probability
