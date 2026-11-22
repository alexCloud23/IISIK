from __future__ import annotations

import os
import tempfile
from pathlib import Path

_DB_DIR = Path(tempfile.mkdtemp(prefix="lr4_tests_"))

for _prefix, _name in (
    ("PRODUCT_", "product"),
    ("MARKET_DATA_", "market"),
    ("DEMAND_FORECAST_", "forecast"),
    ("COMPETITIVE_STRATEGY_", "strategy"),
    ("PRICING_", "pricing"),
    ("ANALYTICS_", "analytics"),
    ("NOTIFICATION_", "notification"),
    ("IDENTITY_", "identity"),
):
    os.environ.setdefault(
        f"{_prefix}DATABASE_URL",
        f"sqlite:///{(_DB_DIR / f'{_name}.db').as_posix()}",
    )

os.environ.setdefault("IDENTITY_REDIS_URL", "fakeredis://")
os.environ.setdefault("PRICING_FORECAST_PROVIDER", "mock")
os.environ.setdefault("NOTIFICATION_KAFKA_ENABLED", "false")

from gateway.app.dto import AuthUserData


def admin_user() -> AuthUserData:
    return AuthUserData(
        id="00000000-0000-4000-8000-000000000000",
        email="admin@example.com",
        full_name="Тестовый администратор",
        roles=["ADMIN"],
    )
