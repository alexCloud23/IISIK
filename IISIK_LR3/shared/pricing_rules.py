from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from shared.errors import InvalidInputError

STRATEGY_TYPES: tuple[str, ...] = ("MATCH", "UNDERCUT", "PREMIUM")
VALID_DECISIONS: tuple[str, ...] = ("ACCEPTED", "REJECTED")

UNDERCUT_FACTOR = Decimal("0.99")
PREMIUM_FACTOR = Decimal("1.02")
COST_RATIO = Decimal("0.6")

_MONEY_QUANTUM = Decimal("0.01")


def round_money(value: Decimal | float | int | str) -> Decimal:
    return Decimal(str(value)).quantize(_MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def _amount(value: Decimal | None) -> str:
    if value is None:
        return "—"
    return str(Decimal(str(value)).quantize(_MONEY_QUANTUM, rounding=ROUND_HALF_UP))


def _raw_price(
    current_price: Decimal,
    strategy_type: str | None,
    competitor_price: Decimal | None,
) -> Decimal:
    if strategy_type is None:
        return current_price
    if strategy_type == "MATCH":
        if competitor_price is None:
            raise InvalidInputError("Для стратегии MATCH требуется цена конкурента")
        return Decimal(str(competitor_price))
    if strategy_type == "UNDERCUT":
        if competitor_price is None:
            raise InvalidInputError("Для стратегии UNDERCUT требуется цена конкурента")
        return Decimal(str(competitor_price)) * UNDERCUT_FACTOR
    if strategy_type == "PREMIUM":
        return current_price * PREMIUM_FACTOR
    raise InvalidInputError(f"Неизвестный тип стратегии: {strategy_type}")


def compute_recommendation(
    current_price: Decimal | float | str,
    strategy_type: str | None = None,
    competitor_price: Decimal | float | str | None = None,
    predicted_demand: Decimal | float | str | None = None,
) -> tuple[Decimal, str]:
    current = round_money(current_price)
    raw = _raw_price(current, strategy_type, competitor_price)
    price = round_money(raw)
    cost = round_money(current * COST_RATIO)
    floored = price < cost
    if floored:
        price = current
    reason = build_recommendation_reason(
        current,
        price,
        strategy_type=strategy_type,
        competitor_price=competitor_price,
        predicted_demand=predicted_demand,
        floored=floored,
        raw_price=raw,
    )
    return price, reason


def compute_recommended_price(
    current_price: Decimal | float | str,
    strategy_type: str | None = None,
    competitor_price: Decimal | float | str | None = None,
) -> Decimal:
    price, _ = compute_recommendation(current_price, strategy_type, competitor_price)
    return price


def build_recommendation_reason(
    current_price: Decimal,
    recommended_price: Decimal,
    strategy_type: str | None = None,
    competitor_price: Decimal | float | str | None = None,
    predicted_demand: Decimal | float | str | None = None,
    *,
    floored: bool = False,
    raw_price: Decimal | None = None,
) -> str:
    demand_text = _amount(Decimal(str(predicted_demand)) if predicted_demand is not None else None)
    price_text = _amount(recommended_price)
    if floored and strategy_type is not None:
        raw_text = _amount(raw_price)
        return (
            f"Расчётная цена {raw_text} BYN ниже себестоимости; "
            f"цена оставлена без изменений ({price_text} BYN)."
        )
    if strategy_type is None:
        return (
            f"Прогноз спроса {demand_text} ед.; "
            f"цена оставлена без изменений ({price_text} BYN)."
        )
    competitor_text = _amount(competitor_price)
    return (
        f"Расчёт по стратегии {strategy_type}: цена конкурента {competitor_text} BYN; "
        f"прогноз спроса {demand_text} ед. "
        f"Рекомендуемая цена {price_text} BYN."
    )
