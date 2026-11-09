from __future__ import annotations

from sqlalchemy import delete
from sqlalchemy.orm import Session

from fixtures.analytics import ANALYTICS_RESULTS

from .models import AnalyticsResult


def seed(session: Session) -> int:
    session.execute(delete(AnalyticsResult))
    session.add_all(
        [
            AnalyticsResult(
                id=item.id,
                product_id=item.product_id,
                recommendation_id=item.recommendation_id,
                analysis_type=item.analysis_type,
                metrics=item.metrics,
                created_at=item.created_at,
            )
            for item in ANALYTICS_RESULTS
        ]
    )
    session.commit()
    return len(ANALYTICS_RESULTS)
