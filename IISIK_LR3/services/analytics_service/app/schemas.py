from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict


class AnalyticsResultDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str | None
    recommendation_id: str | None
    analysis_type: str
    metrics: dict[str, Any]
    created_at: datetime


class AnalyticsRunDTO(BaseModel):
    product_id: str
    analysis_type: str = "SALES_SUMMARY"
    records: int
    total_quantity: int
    average_unit_price: Decimal
    predicted_demand: Decimal | None = None
    current_price: Decimal | None = None
    recommended_price: Decimal | None = None
    recommendation_id: str | None = None
