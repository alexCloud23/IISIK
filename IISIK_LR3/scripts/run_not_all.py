from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))

from run_all import GATEWAY, SERVICES, _spawn

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _wait_health(port: int, timeout: float = 30.0) -> bool:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with opener.open(
                f"http://127.0.0.1:{port}/health", timeout=2
            ) as response:
                if response.status == 200:
                    return True
        except OSError:
            pass
        time.sleep(0.5)
    return False


def _docker(*args: str) -> None:
    subprocess.run(["docker", *args], check=False, capture_output=True)


def _kill_tree(process: subprocess.Popen) -> None:
    if process.poll() is None:
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            check=False,
            capture_output=True,
        )


def _pause(text: str) -> None:
    input(f"\n{text} и нажмите Enter. ")


def main() -> int:
    _docker("compose", "up", "-d")
    print("Redis и Kafka подняты.")

    env = os.environ.copy()
    env["GATEWAY_CLIENT_MODE"] = "grpc"
    processes: dict[str, subprocess.Popen] = {}
    for name, target, port in SERVICES + [GATEWAY]:
        processes[name] = _spawn(name, target, port, env)

    try:
        for name, _, port in SERVICES + [GATEWAY]:
            if not _wait_health(port):
                print(f"Сервис {name} (:{port}) не поднялся за 30 с")
                return 1
        print("Сервисы запущены (режим grpc).")

        _pause("Запустите в Postman папки 0, 1, 2")

        _kill_tree(processes["product"])
        _pause(
            "Product остановлен. Запустите тесты «products при мёртвом product»\n"
            "и «notifications при мёртвом product»"
        )

        processes["product"] = _spawn(
            "product", "services.product_service.app.api:app", 8002, env
        )
        if not _wait_health(8002):
            print("product не поднялся за 30 с")
            return 1
        _pause("Product запущен. Запустите тест «products после восстановления»")

        _docker("stop", "iisik_lr3-kafka-1")
        _pause(
            "Kafka остановлена. Запустите тест «generatePriceRecommendation при мёртвой Kafka»\n"
            "(может идти до ~60 с)"
        )

        _docker("start", "iisik_lr3-kafka-1")
        time.sleep(15)
        _pause("Kafka запущена. Запустите тест «generatePriceRecommendation после старта Kafka»")

        print("Готово.")
        return 0
    except KeyboardInterrupt:
        print("\nПрервано.")
        return 1
    finally:
        for process in processes.values():
            _kill_tree(process)
        print("Сервисы остановлены.")


if __name__ == "__main__":
    raise SystemExit(main())
