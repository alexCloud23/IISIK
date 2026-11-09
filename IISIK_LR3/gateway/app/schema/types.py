from __future__ import annotations

from decimal import Decimal
from enum import Enum

import strawberry
from strawberry.types import Info

from ..context import get_product_cached
from ..dto import (
    AnalyticsResultData,
    ForecastData,
    NotificationData,
    ProductData,
    RecommendationData,
    RecommendationsSummaryData,
    SalesSummaryData,
    StrategyData,
)

COST_RATIO = Decimal("0.6")


@strawberry.enum
class SortDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"


@strawberry.enum
class ProductSortField(Enum):
    NAME = "name"
    CURRENT_PRICE = "price"
    CREATED_AT = "created"


@strawberry.enum
class RecommendationSortField(Enum):
    CREATED_AT = "created"
    RECOMMENDED_PRICE = "price"


@strawberry.enum
class RecommendationStatus(Enum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@strawberry.enum
class RecommendationDecision(Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


def _money(value: Decimal | float) -> float:
    return round(float(value), 2)


def _moment(value: object) -> str:
    return value.isoformat(timespec="seconds")


def _format_metrics(metrics: dict[str, object]) -> str:
    if not metrics:
        return "—"
    parts = []
    for key, value in metrics.items():
        if isinstance(value, float):
            parts.append(f"{key}={value:.2f}")
        else:
            parts.append(f"{key}={value}")
    return "; ".join(parts)


@strawberry.type(name="Product")
class ProductType:
    id: strawberry.ID
    name: str
    description: str | None
    category: str
    current_price: float
    cost_price: float
    is_active: bool

    @classmethod
    def from_dto(cls, dto: ProductData) -> ProductType:
        base_price = _money(dto.base_price)
        return cls(
            id=strawberry.ID(dto.id),
            name=dto.name,
            description=dto.description,
            category=dto.category,
            current_price=base_price,
            cost_price=_money(dto.base_price * COST_RATIO),
            is_active=dto.is_active,
        )


@strawberry.type(name="DemandForecast")
class DemandForecastType:
    id: strawberry.ID
    product_id: strawberry.ID
    forecast_period: str
    predicted_demand: float
    confidence: float | None
    created_at: str

    @classmethod
    def from_dto(cls, dto: ForecastData) -> DemandForecastType:
        return cls(
            id=strawberry.ID(dto.id),
            product_id=strawberry.ID(dto.product_id),
            forecast_period=(
                f"{dto.period_start:%Y-%m-%d}..{dto.period_end:%Y-%m-%d}"
            ),
            predicted_demand=_money(dto.predicted_demand),
            confidence=float(dto.confidence) if dto.confidence is not None else None,
            created_at=_moment(dto.created_at),
        )


@strawberry.type(name="CompetitorStrategy")
class CompetitorStrategyType:
    id: strawberry.ID
    product_id: strawberry.ID
    strategy_type: str
    competitor_price: float
    description: str
    created_at: str

    @classmethod
    def from_dto(cls, dto: StrategyData) -> CompetitorStrategyType:
        probability = dto.estimated_probability
        probability_text = (
            f"{float(probability) * 100:.0f}%" if probability is not None else "не оценена"
        )
        return cls(
            id=strawberry.ID(dto.id),
            product_id=strawberry.ID(dto.product_id),
            strategy_type=dto.strategy_type,
            competitor_price=_money(dto.competitor_price),
            description=(
                f"Конкурент {dto.competitor_name}: стратегия {dto.strategy_type}, "
                f"цена {_money(dto.competitor_price):.2f} BYN, "
                f"вероятность {probability_text}"
            ),
            created_at=_moment(dto.created_at),
        )


@strawberry.type(name="PriceRecommendation")
class PriceRecommendationType:
    id: strawberry.ID
    product_id: strawberry.ID
    current_price: float
    recommended_price: float
    status: RecommendationStatus
    rationale: str
    created_at: str

    @strawberry.field
    def product(self, info: Info) -> ProductType | None:
        dto = get_product_cached(info, str(self.product_id))
        return ProductType.from_dto(dto) if dto else None

    @classmethod
    def from_dto(cls, dto: RecommendationData) -> PriceRecommendationType:
        return cls(
            id=strawberry.ID(dto.id),
            product_id=strawberry.ID(dto.product_id),
            current_price=_money(dto.current_price),
            recommended_price=_money(dto.recommended_price),
            status=RecommendationStatus(dto.status),
            rationale=dto.reason,
            created_at=_moment(dto.created_at),
        )


@strawberry.type(name="SalesSummary")
class SalesSummaryType:
    product_id: strawberry.ID
    orders_count: int
    total_quantity: int
    avg_unit_price: float

    @classmethod
    def from_dto(cls, dto: SalesSummaryData) -> SalesSummaryType:
        return cls(
            product_id=strawberry.ID(dto.product_id),
            orders_count=dto.records,
            total_quantity=dto.total_quantity,
            avg_unit_price=_money(dto.average_unit_price),
        )


@strawberry.type(name="RecommendationsSummary")
class RecommendationsSummaryType:
    total: int
    new_count: int
    accepted_count: int
    rejected_count: int

    @classmethod
    def from_dto(cls, dto: RecommendationsSummaryData) -> RecommendationsSummaryType:
        return cls(
            total=dto.total,
            new_count=dto.new,
            accepted_count=dto.accepted,
            rejected_count=dto.rejected,
        )


@strawberry.type(name="AnalyticsResult")
class AnalyticsResultType:
    id: strawberry.ID
    analysis_type: str
    result: str
    created_at: str

    @classmethod
    def from_dto(cls, dto: AnalyticsResultData) -> AnalyticsResultType:
        return cls(
            id=strawberry.ID(dto.id),
            analysis_type=dto.analysis_type,
            result=_format_metrics(dto.metrics),
            created_at=_moment(dto.created_at),
        )


@strawberry.type(name="Notification")
class NotificationType:
    id: strawberry.ID
    message: str
    notification_type: str
    is_read: bool
    created_at: str

    @classmethod
    def from_dto(cls, dto: NotificationData) -> NotificationType:
        return cls(
            id=strawberry.ID(dto.id),
            message=f"{dto.title}. {dto.message}",
            notification_type=dto.notification_type,
            is_read=dto.is_read,
            created_at=_moment(dto.created_at),
        )
