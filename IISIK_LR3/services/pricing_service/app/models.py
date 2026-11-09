from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Index, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PriceRecommendation(Base):
    __tablename__ = "price_recommendations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(36), nullable=False)
    forecast_id: Mapped[str] = mapped_column(String(36), nullable=False)
    strategy_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    current_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    recommended_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (Index("ix_pr_product", "product_id"),)
