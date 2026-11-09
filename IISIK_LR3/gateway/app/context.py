from __future__ import annotations

from strawberry.types import Info

from .clients.factory import ClientBundle
from .dto import ProductData


def get_clients(info: Info) -> ClientBundle:
    return info.context["clients"]


def get_product_cached(info: Info, product_id: str) -> ProductData | None:
    cache: dict[tuple[str, str], ProductData | None] = info.context.setdefault(
        "cache", {}
    )
    key = ("product", str(product_id))
    if key not in cache:
        cache[key] = get_clients(info).product.get_product(str(product_id))
    return cache[key]
