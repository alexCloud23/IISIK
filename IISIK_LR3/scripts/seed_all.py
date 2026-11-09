from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from sqlalchemy import func, select

SERVICES: list[tuple[str, str]] = [
    ("Identity", "services.identity_service.app"),
    ("Product", "services.product_service.app"),
    ("Market Data", "services.market_data_service.app"),
    ("Demand Forecast", "services.demand_forecast_service.app"),
    ("Competitive Strategy", "services.competitive_strategy_service.app"),
    ("Pricing", "services.pricing_service.app"),
    ("Analytics", "services.analytics_service.app"),
    ("Notification", "services.notification_service.app"),
]


def seed_service(title: str, package: str) -> int:
    models = importlib.import_module(f"{package}.models")
    db = importlib.import_module(f"{package}.db")
    seed_module = importlib.import_module(f"{package}.seed")

    models.Base.metadata.create_all(db.engine)
    with db.SessionLocal() as session:
        seed_module.seed(session)

    with db.SessionLocal() as session:
        counts = {
            table.name: session.scalar(select(func.count()).select_from(table))
            for table in models.Base.metadata.sorted_tables
        }

    summary = ", ".join(f"{name}={count}" for name, count in counts.items())
    print(f"[{title}] {summary}")
    print(f"          БД: {db.settings.database_url}")
    return sum(int(value or 0) for value in counts.values())


def main() -> int:
    total = 0
    for title, package in SERVICES:
        total += seed_service(title, package)
    print(f"\nГотово: {total} записей в {len(SERVICES)} сервисах.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
