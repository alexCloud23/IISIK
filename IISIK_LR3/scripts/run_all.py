from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SERVICES: list[tuple[str, str, int]] = [
    ("identity", "services.identity_service.app.api:app", 8001),
    ("product", "services.product_service.app.api:app", 8002),
    ("market-data", "services.market_data_service.app.api:app", 8003),
    ("demand-forecast", "services.demand_forecast_service.app.api:app", 8004),
    ("competitive-strategy", "services.competitive_strategy_service.app.api:app", 8005),
    ("pricing", "services.pricing_service.app.api:app", 8006),
    ("analytics", "services.analytics_service.app.api:app", 8007),
    ("notification", "services.notification_service.app.api:app", 8008),
]

GATEWAY = ("gateway", "gateway.app.main:app", 8000)


def _spawn(name: str, target: str, port: int, env: dict[str, str]) -> subprocess.Popen:
    command = [
        sys.executable,
        "-m",
        "uvicorn",
        target,
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
    ]
    print(f"  {name:<22} http://127.0.0.1:{port}")
    return subprocess.Popen(command, cwd=ROOT, env=env)


def main() -> int:
    parser = argparse.ArgumentParser(description="Запуск всех сервисов системы")
    parser.add_argument(
        "--mode",
        choices=("mock", "http"),
        default="mock",
    )
    args = parser.parse_args()

    env = os.environ.copy()
    env["GATEWAY_CLIENT_MODE"] = args.mode

    print(f"Запуск сервисов (режим Gateway: {args.mode}):")
    processes: list[tuple[str, subprocess.Popen]] = []
    for name, target, port in SERVICES:
        processes.append((name, _spawn(name, target, port, env)))

    print("\nGateway:")
    gateway_process = _spawn(*GATEWAY, env)
    processes.append((GATEWAY[0], gateway_process))

    print("\nПолезные ссылки:")
    print("  GraphiQL (основной интерфейс)   http://127.0.0.1:8000/graphql")
    print("  Swagger-документация Product    http://127.0.0.1:8002/docs")
    print("  Список товаров                  http://127.0.0.1:8002/products")
    print("  Пользователи                    http://127.0.0.1:8001/users")
    print("  Рекомендации                    http://127.0.0.1:8006/recommendations")
    print("  Подсказка по любому сервису     http://127.0.0.1:<порт>/")
    print("\nОстановка — Ctrl+C.\n")

    exit_code = 0
    try:
        while True:
            for name, process in processes:
                code = process.poll()
                if code is not None:
                    print(f"Процесс {name} завершился с кодом {code}")
                    exit_code = 1
                    raise KeyboardInterrupt
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nОстанавливаю процессы...")
    finally:
        for _, process in processes:
            if process.poll() is None:
                process.terminate()
        for name, process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"Процесс {name} не завершился, принудительное завершение")
                process.kill()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
