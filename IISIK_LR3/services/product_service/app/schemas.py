from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    category: str
    base_price: Decimal
    currency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ProductCreateDTO(BaseModel):
    name: str
    description: str | None = None
    category: str
    base_price: Decimal
    currency: str = "BYN"


class ProductUpdateDTO(BaseModel):
    base_price: Decimal | None = None
    description: str | None = None
    is_active: bool | None = None
