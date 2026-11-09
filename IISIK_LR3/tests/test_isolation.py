from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([\w\.]+)", re.MULTILINE)


def imports_of(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(IMPORT_RE.findall(text))


def python_files(*parts: str) -> list[Path]:
    return sorted((ROOT.joinpath(*parts)).rglob("*.py"))


def test_gateway_does_not_import_services():
    offenders = [
        f
        for f in python_files("gateway")
        if any(mod == "services" or mod.startswith("services.") for mod in imports_of(f))
    ]
    assert not offenders, f"gateway импортирует services: {offenders}"


def test_mock_clients_have_no_network_imports():
    forbidden = {"httpx", "requests", "grpc", "socket", "urllib3"}
    offenders = [
        f
        for f in python_files("gateway", "app", "clients", "mock")
        if imports_of(f) & forbidden
    ]
    assert not offenders, f"mock-клиенты используют сеть: {offenders}"


def test_http_clients_do_not_import_fixtures():
    offenders = [
        f
        for f in python_files("gateway", "app", "clients", "http")
        if any(mod == "fixtures" or mod.startswith("fixtures.") for mod in imports_of(f))
    ]
    assert not offenders, f"http-клиенты используют fixtures: {offenders}"


def test_mock_clients_may_use_shared_rules():
    text = (ROOT / "gateway" / "app" / "clients" / "mock" / "clients.py").read_text(
        encoding="utf-8"
    )
    assert "from shared.pricing_rules import" in text


def test_services_do_not_import_each_other():
    services_dir = ROOT / "services"
    offenders = []
    for service_dir in services_dir.iterdir():
        if not (service_dir / "app").exists():
            continue
        for f in python_files("services", service_dir.name):
            for mod in imports_of(f):
                if mod.startswith("services."):
                    other = mod.split(".")[1] if "." in mod else mod
                    if other != service_dir.name:
                        offenders.append(f"{f}: {mod}")
    assert not offenders, f"сервисы импортируют другие сервисы: {offenders}"


def test_no_grpc_or_brokers():
    forbidden = {"grpc", "pika", "kafka", "celery", "redis"}
    offenders = []
    for f in python_files("gateway") + python_files("services") + python_files("shared"):
        if imports_of(f) & forbidden:
            offenders.append(str(f))
    assert not offenders, f"найдены сетевые брокеры/gRPC: {offenders}"


def test_gateway_uses_protocol_clients():
    text = (ROOT / "gateway" / "app" / "clients" / "base.py").read_text(encoding="utf-8")
    assert "Protocol" in text
    assert "MarketDataClient" in text


def test_pricing_service_uses_provider_stub():
    text = (ROOT / "services" / "pricing_service" / "app" / "service.py").read_text(
        encoding="utf-8"
    )
    assert "default_forecast_provider" in text
