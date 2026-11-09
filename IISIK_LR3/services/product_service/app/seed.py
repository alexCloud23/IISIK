from __future__ import annotations

from sqlalchemy import delete
from sqlalchemy.orm import Session

from fixtures.product import PRODUCTS

from .models import Product


def seed(session: Session) -> int:
    session.execute(delete(Product))
    session.add_all(
        [
            Product(
                id=item.id,
                name=item.name,
                description=item.description,
                category=item.category,
                base_price=item.base_price,
                currency=item.currency,
                is_active=item.is_active,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in PRODUCTS
        ]
    )
    session.commit()
    return len(PRODUCTS)
