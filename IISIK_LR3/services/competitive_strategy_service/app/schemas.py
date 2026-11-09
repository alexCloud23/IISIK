from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class StrategyDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str
    competitor_name: str
    strategy_type: str
    competitor_price: Decimal
    price_change_percent: Decimal | None
    estimated_probability: Decimal | None
    created_at: datetime
