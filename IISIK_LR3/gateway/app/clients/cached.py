from __future__ import annotations

import logging
from decimal import Decimal

from ..cache import RedisCache
from ..dto import ProductData
from .base import UNSET, ProductClient

logger = logging.getLogger(__name__)


class CachedProductClient:
    def __init__(self, inner: ProductClient, cache: RedisCache) -> None:
        self._inner = inner
        self._cache = cache

    @staticmethod
    def _key(product_id: str) -> str:
        return f"product:{product_id}"

    def get_product(self, product_id: str) -> ProductData | None:
        key = self._key(product_id)
        cached = self._cache.get_json(key)
        if cached is not None:
            logger.info("Кеш: товар %s получен из Redis", product_id)
            return ProductData.model_validate(cached)
        product = self._inner.get_product(product_id)
        if product is not None:
            self._cache.set_json(key, product.model_dump(mode="json"))
        return product

    def list_products(self, *args, **kwargs) -> list[ProductData]:
        return self._inner.list_products(*args, **kwargs)

    def create_product(self, **kwargs) -> ProductData:
        return self._inner.create_product(**kwargs)

    def update_product(
        self,
        product_id: str,
        *,
        base_price: Decimal | None = UNSET,
        description: str | None = UNSET,
        is_active: bool | None = UNSET,
    ) -> ProductData:
        product = self._inner.update_product(
            product_id,
            base_price=base_price,
            description=description,
            is_active=is_active,
        )
        self._cache.delete(self._key(product_id))
        return product

    def close(self) -> None:
        close = getattr(self._inner, "close", None)
        if callable(close):
            close()
