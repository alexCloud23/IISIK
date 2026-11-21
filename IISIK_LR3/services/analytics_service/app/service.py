from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from shared.analytics_rules import build_sales_metrics
from shared.errors import parse_uuid
from shared.validation import validate_non_empty

from . import repository
from .models import AnalyticsResult
from .schemas import AnalyticsResultDTO, AnalyticsRunDTO


def list_results(
    session: Session, analysis_type: str | None = None
) -> list[AnalyticsResultDTO]:
    return [
        AnalyticsResultDTO.model_validate(row)
        for row in repository.list_results(session, analysis_type)
    ]


def run_analysis(session: Session, data: AnalyticsRunDTO) -> AnalyticsResultDTO:
    product_id = str(parse_uuid(data.product_id, "product_id"))
    analysis_type = validate_non_empty(data.analysis_type, "analysis_type")
    recommendation_id = (
        str(parse_uuid(data.recommendation_id, "recommendation_id"))
        if data.recommendation_id
        else None
    )
    metrics = build_sales_metrics(
        data.records,
        data.total_quantity,
        data.average_unit_price,
        predicted_demand=data.predicted_demand,
        current_price=data.current_price,
        recommended_price=data.recommended_price,
    )
    result = repository.add_result(
        session,
        AnalyticsResult(
            id=str(uuid4()),
            product_id=product_id,
            recommendation_id=recommendation_id,
            analysis_type=analysis_type,
            metrics=metrics,
            created_at=datetime.utcnow(),
        ),
    )
    return AnalyticsResultDTO.model_validate(result)


def format_metrics(metrics: dict[str, object]) -> str:
    if not metrics:
        return "—"
    parts = []
    for key, value in metrics.items():
        if isinstance(value, float):
            parts.append(f"{key}={value:.2f}")
        else:
            parts.append(f"{key}={value}")
    return "; ".join(parts)
