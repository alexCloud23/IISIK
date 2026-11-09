from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any


def dt(year: int, month: int, day: int, hour: int = 10, minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute)


@dataclass(frozen=True)
class Role:
    id: str
    name: str
    description: str | None


@dataclass(frozen=True)
class User:
    id: str
    email: str
    password_hash: str
    full_name: str
    is_active: bool
    created_at: datetime


@dataclass(frozen=True)
class UserRole:
    user_id: str
    role_id: str


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    description: str | None
    category: str
    base_price: Decimal
    currency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CompetitorPrice:
    id: str
    product_id: str
    competitor_name: str
    price: Decimal
    currency: str
    source: str
    observed_at: datetime


@dataclass(frozen=True)
class SalesRecord:
    id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    currency: str
    sold_at: datetime


@dataclass(frozen=True)
class DemandForecast:
    id: str
    product_id: str
    period_start: datetime
    period_end: datetime
    predicted_demand: Decimal
    confidence: Decimal | None
    model_version: str
    created_at: datetime


@dataclass(frozen=True)
class CompetitorStrategy:
    id: str
    product_id: str
    competitor_name: str
    strategy_type: str
    competitor_price: Decimal
    price_change_percent: Decimal | None
    estimated_probability: Decimal | None
    created_at: datetime


@dataclass(frozen=True)
class PriceRecommendation:
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


@dataclass(frozen=True)
class AnalyticsResult:
    id: str
    product_id: str | None
    recommendation_id: str | None
    analysis_type: str
    metrics: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class Notification:
    id: str
    user_id: str
    notification_type: str
    title: str
    message: str
    related_entity_id: str | None
    status: str
    is_read: bool
    created_at: datetime
    sent_at: datetime | None = None
