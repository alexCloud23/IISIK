from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AnalyticsResult(Base):
    __tablename__ = "analytics_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    product_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    recommendation_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    analysis_type: Mapped[str] = mapped_column(String(100), nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (Index("ix_ar_type", "analysis_type"),)
