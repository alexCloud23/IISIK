from __future__ import annotations

from decimal import Decimal
from typing import Any

from shared.errors import InvalidInputError


def build_sales_metrics(
    records: int,
    total_quantity: int,
    average_unit_price: Decimal | float | str,
    predicted_demand: Decimal | float | str | None = None,
    current_price: Decimal | float | str | None = None,
    recommended_price: Decimal | float | str | None = None,
) -> dict[str, Any]:
    if records < 0 or total_quantity < 0:
        raise InvalidInputError("Количество продаж не может быть отрицательным")
    avg_price = Decimal(str(average_unit_price))
    metrics: dict[str, Any] = {
        "records": records,
        "total_quantity": total_quantity,
        "avg_unit_price": float(avg_price),
        "revenue": float(avg_price * total_quantity),
    }
    if predicted_demand is not None:
        demand = Decimal(str(predicted_demand))
        metrics["predicted_demand"] = float(demand)
        if demand:
            deviation = (Decimal(total_quantity) - demand) / demand * 100
            metrics["demand_deviation_percent"] = float(
                deviation.quantize(Decimal("0.01"))
            )
    if current_price is not None and recommended_price is not None:
        current = Decimal(str(current_price))
        recommended = Decimal(str(recommended_price))
        metrics["current_price"] = float(current)
        metrics["recommended_price"] = float(recommended)
        if current:
            change = (recommended - current) / current * 100
            metrics["price_change_percent"] = float(
                change.quantize(Decimal("0.01"))
            )
    return metrics
