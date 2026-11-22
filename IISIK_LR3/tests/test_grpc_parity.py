from __future__ import annotations

import importlib
from concurrent import futures

import grpc
import pytest

import shared.protogen
import analytics_pb2_grpc
import forecast_pb2_grpc
import market_data_pb2_grpc
import notification_pb2_grpc
import pricing_pb2_grpc
import product_pb2_grpc
import strategy_pb2_grpc
from gateway.app.clients.factory import build_grpc_bundle, build_http_bundle
from gateway.app.config import Settings
from tests.conftest import admin_user
from tests.test_mode_parity import SERVICE_MODULES, _make_transport, run_scenario

GRPC_SERVICES = {
    "product": ("ProductGrpcService", product_pb2_grpc.add_ProductServiceServicer_to_server),
    "market_data": ("MarketDataGrpcService", market_data_pb2_grpc.add_MarketDataServiceServicer_to_server),
    "forecast": ("ForecastGrpcService", forecast_pb2_grpc.add_ForecastServiceServicer_to_server),
    "strategy": ("StrategyGrpcService", strategy_pb2_grpc.add_StrategyServiceServicer_to_server),
    "recommendation": ("PricingGrpcService", pricing_pb2_grpc.add_PricingServiceServicer_to_server),
    "analytics": ("AnalyticsGrpcService", analytics_pb2_grpc.add_AnalyticsServiceServicer_to_server),
    "notification": ("NotificationGrpcService", notification_pb2_grpc.add_NotificationServiceServicer_to_server),
}


def _seed_all() -> None:
    for _name, pkg in SERVICE_MODULES:
        api = importlib.import_module(f"{pkg}.api")
        seed = importlib.import_module(f"{pkg}.seed")
        db = importlib.import_module(f"{pkg}.db")
        api.Base.metadata.create_all(api.engine)
        with db.SessionLocal() as session:
            seed.seed(session)


@pytest.fixture(scope="module")
def http_context():
    bundle = build_http_bundle(
        Settings(client_mode="http"),
        {
            name: _make_transport(importlib.import_module(f"{pkg}.api").app)
            for name, pkg in SERVICE_MODULES
        },
    )
    yield {"clients": bundle, "cache": {}, "user": admin_user()}
    bundle.close()


@pytest.fixture(scope="module")
def grpc_context():
    servers = []
    addrs = {}
    for name, pkg in SERVICE_MODULES:
        grpc_module = importlib.import_module(f"{pkg}.grpc_server")
        servicer_cls_name, register = GRPC_SERVICES[name]
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        register(getattr(grpc_module, servicer_cls_name)(), server)
        port = server.add_insecure_port("127.0.0.1:0")
        server.start()
        servers.append(server)
        addrs[name] = f"127.0.0.1:{port}"
    bundle = build_grpc_bundle(Settings(client_mode="grpc"), addrs)
    yield {"clients": bundle, "cache": {}, "user": admin_user()}
    bundle.close()
    for server in servers:
        server.stop(0).wait()


def test_http_and_grpc_produce_same_results(http_context, grpc_context):
    _seed_all()
    http_results = run_scenario(http_context)
    _seed_all()
    grpc_results = run_scenario(grpc_context)
    assert http_results == grpc_results
