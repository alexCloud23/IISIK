from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Index, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CompetitorStrategy(Base):
    __tablename__ = "competitor_strategies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(36), nullable=False)
    competitor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    strategy_type: Mapped[str] = mapped_column(String(100), nullable=False)
    competitor_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    price_change_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 2), nullable=True
    )
    estimated_probability: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 4), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (Index("ix_cs_product", "product_id"),)
