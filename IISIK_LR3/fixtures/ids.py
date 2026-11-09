from __future__ import annotations


def uid(prefix: str, n: int) -> str:
    if len(prefix) != 8:
        raise ValueError("prefix должен состоять из 8 символов")
    if not 0 <= n <= 999_999_999_999:
        raise ValueError("n вне диапазона")
    return f"{prefix}-0000-4000-8000-{n:012d}"


USER = "10000000"
ROLE = "11000000"
PRODUCT = "20000000"
COMPETITOR_PRICE = "30000000"
SALES = "40000000"
FORECAST = "50000000"
STRATEGY = "60000000"
RECOMMENDATION = "70000000"
ANALYTICS = "80000000"
NOTIFICATION = "90000000"
