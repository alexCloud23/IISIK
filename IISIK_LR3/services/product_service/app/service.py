from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from shared.errors import InvalidFilterError, InvalidOperationError, NotFoundError, parse_uuid
from shared.pricing_rules import round_money
from shared.validation import validate_non_empty, validate_positive_price

from . import repository
from .models import Product
from .schemas import ProductCreateDTO, ProductDTO, ProductUpdateDTO

VALID_SORT_FIELDS = ("name", "price", "created")
VALID_ORDERS = ("asc", "desc")


def get_product(session: Session, product_id: str) -> ProductDTO:
    parsed = parse_uuid(product_id, "product_id")
    product = repository.get_product(session, str(parsed))
    if product is None:
        raise NotFoundError(f"Товар {product_id} не найден")
    return ProductDTO.model_validate(product)


def list_products(
    session: Session,
    category: str | None = None,
    is_active: bool | None = None,
    search: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    sort: str = "name",
    order: str = "asc",
) -> list[ProductDTO]:
    if sort not in VALID_SORT_FIELDS:
        raise InvalidFilterError(
            f"Неизвестное поле сортировки: {sort!r}; "
            f"допустимо: {', '.join(VALID_SORT_FIELDS)}"
        )
    if order not in VALID_ORDERS:
        raise InvalidFilterError(
            f"Неизвестное направление сортировки: {order!r}; "
            f"допустимо: {', '.join(VALID_ORDERS)}"
        )
    products = repository.list_products(
        session,
        category,
        is_active,
        search,
        min_price,
        max_price,
        sort_column=repository.SORT_FIELDS[sort],
        descending=order == "desc",
    )
    return [ProductDTO.model_validate(product) for product in products]


def create_product(session: Session, data: ProductCreateDTO) -> ProductDTO:
    name = validate_non_empty(data.name, "name")
    category = validate_non_empty(data.category, "category")
    currency = validate_non_empty(data.currency, "currency")
    price = validate_positive_price(data.base_price, "base_price")
    if repository.get_by_name(session, name) is not None:
        raise InvalidOperationError(f"Товар с названием «{name}» уже существует")

    now = datetime.utcnow()
    product = repository.add_product(
        session,
        Product(
            id=str(uuid4()),
            name=name,
            description=data.description,
            category=category,
            base_price=round_money(price),
            currency=currency,
            is_active=True,
            created_at=now,
            updated_at=now,
        ),
    )
    return ProductDTO.model_validate(product)


def update_product(session: Session, product_id: str, data: ProductUpdateDTO) -> ProductDTO:
    parsed = parse_uuid(product_id, "product_id")
    product = repository.get_product(session, str(parsed))
    if product is None:
        raise NotFoundError(f"Товар {product_id} не найден")

    provided = data.model_fields_set
    if "base_price" in provided:
        if not product.is_active:
            raise InvalidOperationError("Нельзя изменять цену неактивного товара")
        price = validate_positive_price(data.base_price, "base_price")
        product.base_price = round_money(price)
    if "description" in provided:
        product.description = data.description
    if "is_active" in provided and data.is_active is not None:
        product.is_active = data.is_active

    product.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(product)
    return ProductDTO.model_validate(product)
