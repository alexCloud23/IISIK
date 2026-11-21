from __future__ import annotations

from strawberry.types import Info

from shared.errors import ForbiddenError, UnauthorizedError

from .clients.factory import ClientBundle
from .dto import AuthUserData, ProductData

ADMIN_ROLE = "ADMIN"


def get_clients(info: Info) -> ClientBundle:
    return info.context["clients"]


def get_user(info: Info) -> AuthUserData | None:
    return info.context.get("user")


def require_user(info: Info) -> AuthUserData:
    user = get_user(info)
    if user is None:
        raise UnauthorizedError("Требуется аутентификация")
    return user


def require_role(info: Info, *roles: str) -> AuthUserData:
    user = require_user(info)
    if ADMIN_ROLE not in user.roles and not set(roles).intersection(user.roles):
        raise ForbiddenError("Недостаточно прав для выполнения операции")
    return user


def get_product_cached(info: Info, product_id: str) -> ProductData | None:
    cache: dict[tuple[str, str], ProductData | None] = info.context.setdefault(
        "cache", {}
    )
    key = ("product", str(product_id))
    if key not in cache:
        cache[key] = get_clients(info).product.get_product(str(product_id))
    return cache[key]
