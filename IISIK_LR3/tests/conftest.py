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
