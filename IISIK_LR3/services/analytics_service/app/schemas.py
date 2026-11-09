from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AnalyticsResultDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str | None
    recommendation_id: str | None
    analysis_type: str
    metrics: dict[str, Any]
    created_at: datetime
