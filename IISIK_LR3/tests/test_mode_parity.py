from __future__ import annotations

import httpx
import pytest
from starlette.testclient import TestClient

from gateway.app.clients.factory import build_http_bundle, build_mock_bundle
from gateway.app.config import Settings
from gateway.app.schema.schema import schema

P1 = "20000000-0000-4000-8000-000000000001"
P5 = "20000000-0000-4000-8000-000000000005"
R1 = "70000000-0000-4000-8000-000000000001"
R3 = "70000000-0000-4000-8000-000000000003"
N1 = "90000000-0000-4000-8000-000000000001"

SERVICE_MODULES = (
    ("product", "services.product_service.app"),
    ("market_data", "services.market_data_service.app"),
    ("forecast", "services.demand_forecast_service.app"),
    ("strategy", "services.competitive_strategy_service.app"),
    ("recommendation", "services.pricing_service.app"),
    ("analytics", "services.analytics_service.app"),
    ("notification", "services.notification_service.app"),
)


def _make_transport(app) -> httpx.BaseTransport:
    client = TestClient(app)

    def handler(request: httpx.Request) -> httpx.Response:
        content = request.read()
        headers = (
            {"content-type": request.headers.get("content-type", "application/json")}
            if content
            else {}
        )
        response = client.request(
            request.method,
            request.url.path,
            params=dict(request.url.params),
            content=content,
            headers=headers,
        )
        return httpx.Response(
            response.status_code, content=response.content, request=request
        )

    return httpx.MockTransport(handler)


@pytest.fixture(scope="module")
def http_context():
    import importlib

    bundle = build_http_bundle(
        Settings(client_mode="http"),
        {name: _make_transport(importlib.import_module(f"{pkg}.api").app) for name, pkg in SERVICE_MODULES},
    )
    ctx = {"clients": bundle, "cache": {}}
    for _name, pkg in SERVICE_MODULES:
        api = importlib.import_module(f"{pkg}.api")
        seed = importlib.import_module(f"{pkg}.seed")
        db = importlib.import_module(f"{pkg}.db")
        api.Base.metadata.create_all(api.engine)
        with db.SessionLocal() as session:
            seed.seed(session)
    yield ctx
    bundle.close()


@pytest.fixture(scope="module")
def mock_context():
    bundle = build_mock_bundle()
    ctx = {"clients": bundle, "cache": {}}
    yield ctx
    bundle.close()


def run_scenario(ctx) -> list[object]:
    def run(query: str):
        result = schema.execute_sync(query, context_value=ctx)
        if result.errors:
            return result.errors[0].extensions.get("code")
        return result.data

    outcome: list[object] = []
    outcome.append(
        run('{ products(category: "Электроника", orderBy: CURRENT_PRICE,'
            " orderDirection: DESC) { name currentPrice } }")
    )
    outcome.append(run('{ products(search: "pro") { name } }'))
    outcome.append(
        run(f'{{ salesSummary(productId: "{P1}") {{ ordersCount totalQuantity avgUnitPrice }} }}')
    )
    outcome.append(run("{ unreadNotificationsCount }"))
    outcome.append(
        run("{ recommendationsSummary { total newCount acceptedCount rejectedCount } }")
    )
    outcome.append(
        run(f'mutation {{ generatePriceRecommendation(productId: "{P1}")'
            " { status recommendedPrice rationale } }")
    )
    outcome.append(
        run(f'mutation {{ decideRecommendation(id: "{R1}", decision: ACCEPTED) {{ status }} }}')
    )
    outcome.append(
        run(f'mutation {{ decideRecommendation(id: "{R1}", decision: REJECTED) {{ id }} }}')
    )
    outcome.append(
        run(f'mutation {{ decideRecommendation(id: "{R3}", decision: REJECTED) {{ id }} }}')
    )
    outcome.append(run(f'mutation {{ markNotificationRead(id: "{N1}") {{ isRead }} }}'))
    outcome.append(run("mutation { markAllNotificationsRead }"))
    outcome.append(run("{ unreadNotificationsCount }"))
    outcome.append(
        run('mutation { createProduct(input: { name: "Паритетный товар",'
            ' category: "Прочее", price: 123.45 }) { name currentPrice isActive } }')
    )
    outcome.append(
        run('mutation { updateProduct(id: "00000000-0000-0000-0000-000000000000",'
            " input: { price: 1 }) { id } }")
    )
    outcome.append(
        run(f'mutation {{ updateProduct(id: "{P5}", input: {{ price: 10 }}) {{ id }} }}')
    )
    outcome.append(run('{ product(id: "не-uuid") { name } }'))
    outcome.append(
        run(f'mutation {{ generatePriceRecommendation(productId: "{P5}") {{ id }} }}')
    )
    return outcome


def test_mock_and_http_produce_same_results(mock_context, http_context):
    mock_results = run_scenario(mock_context)
    http_results = run_scenario(http_context)
    assert mock_results == http_results


def test_key_values_are_expected(mock_context):
    results = run_scenario(mock_context)
    assert [p["currentPrice"] for p in results[0]["products"]] == [3499.0, 1299.0, 249.0]
    assert results[2]["salesSummary"] == {
        "ordersCount": 6, "totalQuantity": 39, "avgUnitPrice": 1262.33,
    }
    generated = results[5]["generatePriceRecommendation"]
    assert generated["status"] == "NEW"
    assert generated["recommendedPrice"] == 1137.51
    assert results[7] == "INVALID_OPERATION"
    assert results[8] == "INVALID_OPERATION"
    assert results[13] == "NOT_FOUND"
    assert results[14] == "INVALID_OPERATION"
    assert results[15] == "INVALID_ID"
    assert results[16] == "INVALID_OPERATION"
