from __future__ import annotations

from decimal import Decimal

from fixtures.ids import PRODUCT, uid
from fixtures.models import Product, dt

PRODUCTS: list[Product] = [
    Product(
        id=uid(PRODUCT, 1),
        name="Смартфон X200",
        description="Смартфон с OLED-экраном 6.4 и накопителем 256 ГБ",
        category="Электроника",
        base_price=Decimal("1299.00"),
        currency="BYN",
        is_active=True,
        created_at=dt(2026, 3, 1, 10),
        updated_at=dt(2026, 9, 15, 16),
    ),
    Product(
        id=uid(PRODUCT, 2),
        name="Ноутбук Pro 15",
        description="Ноутбук для профессиональной работы, 16 ГБ ОЗУ",
        category="Электроника",
        base_price=Decimal("3499.00"),
        currency="BYN",
        is_active=True,
        created_at=dt(2026, 3, 5, 12),
        updated_at=dt(2026, 9, 20, 9),
    ),
    Product(
        id=uid(PRODUCT, 3),
        name="Наушники AirSound",
        description="Беспроводные наушники с активным шумоподавлением",
        category="Электроника",
        base_price=Decimal("249.00"),
        currency="BYN",
        is_active=True,
        created_at=dt(2026, 4, 10, 15),
        updated_at=dt(2026, 8, 30, 10),
    ),
    Product(
        id=uid(PRODUCT, 4),
        name="Холодильник FrostFree",
        description="Двухкамерный холодильник с системой No Frost",
        category="Бытовая техника",
        base_price=Decimal("2799.00"),
        currency="BYN",
        is_active=True,
        created_at=dt(2026, 2, 20, 9),
        updated_at=dt(2026, 9, 1, 11),
    ),
    Product(
        id=uid(PRODUCT, 5),
        name="Пылесос CycloneMax",
        description="Вертикальный пылесос, модель снята с продажи",
        category="Бытовая техника",
        base_price=Decimal("549.00"),
        currency="BYN",
        is_active=False,
        created_at=dt(2026, 1, 5, 14),
        updated_at=dt(2026, 7, 12, 10),
    ),
]
