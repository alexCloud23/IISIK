from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class RecommendationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str
    forecast_id: str
    strategy_id: str | None
    current_price: Decimal
    recommended_price: Decimal
    currency: str
    reason: str
    status: str
    created_at: datetime


class RecommendationCreateDTO(BaseModel):
    product_id: str
    forecast_id: str
    current_price: Decimal
    strategy_type: str | None = None
    competitor_price: Decimal | None = None
    strategy_id: str | None = None


class RecommendationDecisionDTO(BaseModel):
    decision: str


class RecommendationSummaryDTO(BaseModel):
    total: int
    new: int
    accepted: int
    rejected: int


class ForecastRefDTO(BaseModel):
    id: str
    product_id: str
    period_start: datetime
    period_end: datetime
    predicted_demand: Decimal
    confidence: Decimal | None
    model_version: str


class RecommendationWithForecastDTO(RecommendationDTO):
    forecast: ForecastRefDTO | None = None
