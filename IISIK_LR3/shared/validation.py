from __future__ import annotations

from decimal import Decimal

from shared.errors import InvalidInputError


def validate_non_empty(value: str | None, field: str) -> str:
    if value is None or not value.strip():
        raise InvalidInputError(f"Поле {field} не может быть пустым")
    return value.strip()


def validate_positive_price(value: Decimal | float | str | None, field: str) -> Decimal:
    if value is None:
        raise InvalidInputError(f"Поле {field} не может быть пустым")
    price = Decimal(str(value))
    if price <= 0:
        raise InvalidInputError(f"Поле {field} должно быть положительным числом")
    return price
