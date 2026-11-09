from __future__ import annotations

from sqlalchemy.orm import Session

from . import repository
from .schemas import AnalyticsResultDTO


def list_results(
    session: Session, analysis_type: str | None = None
) -> list[AnalyticsResultDTO]:
    return [
        AnalyticsResultDTO.model_validate(row)
        for row in repository.list_results(session, analysis_type)
    ]


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
