from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import PriceHistory, Product

SORT_FIELDS: dict[str, object] = {
    "name": Product.name,
    "price": Product.base_price,
    "created": Product.created_at,
}


def get_product(session: Session, product_id: str) -> Product | None:
    return session.get(Product, product_id)


def get_by_name(session: Session, name: str) -> Product | None:
    target = name.strip().lower()
    return next(
        (
            product
            for product in session.scalars(select(Product))
            if product.name.lower() == target
        ),
        None,
    )


def add_product(session: Session, product: Product) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def add_price_history(session: Session, entry: PriceHistory) -> None:
    session.add(entry)


def list_price_history(session: Session, product_id: str) -> list[PriceHistory]:
    stmt = (
        select(PriceHistory)
        .where(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.changed_at.desc())
    )
    return list(session.scalars(stmt))


def list_products(
    session: Session,
    category: str | None = None,
    is_active: bool | None = None,
    search: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    sort_column: object = Product.name,
    descending: bool = False,
) -> list[Product]:
    stmt = select(Product)
    if category is not None:
        stmt = stmt.where(Product.category == category)
    if is_active is not None:
        stmt = stmt.where(Product.is_active == is_active)
    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        stmt = stmt.where(Product.base_price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.base_price <= max_price)
    stmt = stmt.order_by(sort_column.desc() if descending else sort_column.asc())
    return list(session.scalars(stmt))
