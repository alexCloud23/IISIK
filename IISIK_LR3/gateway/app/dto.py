from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict


class ProductData(BaseModel):
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


class ForecastData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str
    period_start: datetime
    period_end: datetime
    predicted_demand: Decimal
    confidence: Decimal | None
    model_version: str
    created_at: datetime


class StrategyData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str
    competitor_name: str
    strategy_type: str
    competitor_price: Decimal
    price_change_percent: Decimal | None
    estimated_probability: Decimal | None
    created_at: datetime


class RecommendationData(BaseModel):
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


class RecommendationDetailData(RecommendationData):
    forecast: ForecastData | None = None


class SalesRecordData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    currency: str
    sold_at: datetime


class SalesSummaryData(BaseModel):
    product_id: str
    records: int
    total_quantity: int
    average_unit_price: Decimal


class RecommendationsSummaryData(BaseModel):
    total: int
    new: int
    accepted: int
    rejected: int


class AnalyticsResultData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str | None
    recommendation_id: str | None
    analysis_type: str
    metrics: dict[str, Any]
    created_at: datetime


class NotificationData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    notification_type: str
    title: str
    message: str
    related_entity_id: str | None
    status: str
    is_read: bool
    created_at: datetime
    sent_at: datetime | None
