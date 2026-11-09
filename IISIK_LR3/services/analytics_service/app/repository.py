from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import AnalyticsResult


def list_results(
    session: Session, analysis_type: str | None = None
) -> list[AnalyticsResult]:
    stmt = select(AnalyticsResult).order_by(AnalyticsResult.created_at.desc())
    if analysis_type is not None:
        stmt = stmt.where(AnalyticsResult.analysis_type == analysis_type)
    return list(session.scalars(stmt))
