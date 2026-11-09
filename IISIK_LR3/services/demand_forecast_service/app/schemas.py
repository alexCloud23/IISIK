from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ForecastDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str
    period_start: datetime
    period_end: datetime
    predicted_demand: Decimal
    confidence: Decimal | None
    model_version: str
    created_at: datetime
