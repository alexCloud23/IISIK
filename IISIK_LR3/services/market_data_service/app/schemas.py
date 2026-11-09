from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CompetitorPriceDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str
    competitor_name: str
    price: Decimal
    currency: str
    source: str
    observed_at: datetime


class SalesRecordDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    currency: str
    sold_at: datetime


class SalesSummaryDTO(BaseModel):
    product_id: str
    records: int
    total_quantity: int
    average_unit_price: Decimal
