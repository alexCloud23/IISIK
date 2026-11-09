from __future__ import annotations

import pytest

from gateway.app.clients.factory import build_mock_bundle
from gateway.app.schema.schema import schema

P1 = "20000000-0000-4000-8000-000000000001"
P5 = "20000000-0000-4000-8000-000000000005"
R1 = "70000000-0000-4000-8000-000000000001"
R3 = "70000000-0000-4000-8000-000000000003"
N1 = "90000000-0000-4000-8000-000000000001"


@pytest.fixture()
def context():
    bundle = build_mock_bundle()
    ctx = {"clients": bundle, "cache": {}}
    yield ctx
    bundle.close()


def execute(ctx, query):
    return schema.execute_sync(query, context_value=ctx)


class TestSchemaStructure:
    def test_mutation_fields_present(self):
        sdl = schema.as_str()
        for field in (
            "createProduct", "updateProduct", "generatePriceRecommendation",
            "decideRecommendation", "markNotificationRead", "markAllNotificationsRead",
        ):
            assert field in sdl, field

    def test_query_fields_present(self):
        sdl = schema.as_str()
        for field in (
            "salesSummary", "unreadNotificationsCount", "recommendationsSummary",
            "search", "minPrice", "maxPrice", "orderBy", "orderDirection",
        ):
            assert field in sdl, field

    def test_enums_present(self):
        sdl = schema.as_str()
        for enum in (
            "SortDirection", "ProductSortField", "RecommendationSortField",
            "RecommendationStatus", "RecommendationDecision",
        ):
            assert enum in sdl, enum

    def test_recommendation_has_status(self):
        sdl = schema.as_str()
        assert "status: RecommendationStatus!" in sdl


class TestQueries:
    def test_products_filter_and_sort(self, context):
        result = execute(
            context,
            '{ products(category: "Электроника", orderBy: CURRENT_PRICE,'
            " orderDirection: DESC) { name currentPrice } }",
        )
        assert result.errors is None
        assert [p["currentPrice"] for p in result.data["products"]] == [3499.0, 1299.0, 249.0]

    def test_products_search(self, context):
        result = execute(context, '{ products(search: "pro") { name } }')
        assert result.errors is None
        assert [p["name"] for p in result.data["products"]] == ["Ноутбук Pro 15"]

    def test_price_recommendations_status_filter(self, context):
        result = execute(
            context, '{ priceRecommendations(status: NEW) { status recommendedPrice } }'
        )
        assert result.errors is None
        items = result.data["priceRecommendations"]
        assert len(items) == 2
        assert all(item["status"] == "NEW" for item in items)

    def test_sales_summary(self, context):
        result = execute(
            context,
            f'{{ salesSummary(productId: "{P1}") {{ ordersCount totalQuantity avgUnitPrice }} }}',
        )
        assert result.errors is None
        assert result.data["salesSummary"] == {
            "ordersCount": 6, "totalQuantity": 39, "avgUnitPrice": 1262.33,
        }

    def test_unread_notifications_count(self, context):
        result = execute(context, "{ unreadNotificationsCount }")
        assert result.data["unreadNotificationsCount"] == 2

    def test_recommendations_summary(self, context):
        result = execute(
            context,
            "{ recommendationsSummary { total newCount acceptedCount rejectedCount } }",
        )
        assert result.data["recommendationsSummary"] == {
            "total": 4, "newCount": 2, "acceptedCount": 1, "rejectedCount": 1,
        }

    def test_invalid_uuid_extension_code(self, context):
        result = execute(context, '{ product(id: "не-uuid") { name } }')
        assert result.data["product"] is None
        assert result.errors[0].extensions == {"code": "INVALID_ID"}

    def test_not_found_extension_code(self, context):
        result = execute(context, f'{{ product(id: "{P5[:-1]}9") {{ name }} }}')
        assert result.errors[0].extensions == {"code": "NOT_FOUND"}


class TestMutations:
    def test_create_and_update_product(self, context):
        result = execute(
            context,
            'mutation { createProduct(input: { name: "Тестовый", category: "Прочее",'
            " price: 99.99 }) { id currentPrice isActive } }",
        )
        assert result.errors is None
        created = result.data["createProduct"]
        assert created["currentPrice"] == 99.99
        assert created["isActive"] is True

        result = execute(
            context,
            f'mutation {{ updateProduct(id: "{created["id"]}", input: {{ price: 149.99 }})'
            " { currentPrice } }",
        )
        assert result.errors is None
        assert result.data["updateProduct"]["currentPrice"] == 149.99

    def test_create_duplicate_name(self, context):
        execute(
            context,
            'mutation { createProduct(input: { name: "Уникальный", category: "Прочее",'
            " price: 5 }) { id } }",
        )
        result = execute(
            context,
            'mutation { createProduct(input: { name: "Уникальный", category: "Прочее",'
            " price: 6 }) { id } }",
        )
        assert result.errors[0].extensions == {"code": "INVALID_OPERATION"}

    def test_update_price_of_inactive_product(self, context):
        result = execute(
            context,
            f'mutation {{ updateProduct(id: "{P5}", input: {{ price: 10 }}) {{ id }} }}',
        )
        assert result.errors[0].extensions == {"code": "INVALID_OPERATION"}

    def test_generate_price_recommendation(self, context):
        result = execute(
            context,
            f'mutation {{ generatePriceRecommendation(productId: "{P1}")'
            " { status recommendedPrice rationale } }",
        )
        assert result.errors is None
        data = result.data["generatePriceRecommendation"]
        assert data["status"] == "NEW"
        assert data["recommendedPrice"] == 1137.51
        assert "UNDERCUT" in data["rationale"]
        unread = execute(context, "{ unreadNotificationsCount }")
        assert unread.data["unreadNotificationsCount"] == 3

    def test_generate_for_inactive_product(self, context):
        result = execute(
            context, f'mutation {{ generatePriceRecommendation(productId: "{P5}") {{ id }} }}'
        )
        assert result.errors[0].extensions == {"code": "INVALID_OPERATION"}

    def test_decide_recommendation_flow(self, context):
        result = execute(
            context,
            f'mutation {{ decideRecommendation(id: "{R1}", decision: ACCEPTED)'
            " { status } }",
        )
        assert result.errors is None
        assert result.data["decideRecommendation"]["status"] == "ACCEPTED"

        result = execute(
            context,
            f'mutation {{ decideRecommendation(id: "{R1}", decision: REJECTED)'
            " { status } }",
        )
        assert result.errors[0].extensions == {"code": "INVALID_OPERATION"}

        result = execute(
            context,
            f'mutation {{ decideRecommendation(id: "{R3}", decision: REJECTED)'
            " { status } }",
        )
        assert result.errors[0].extensions == {"code": "INVALID_OPERATION"}

    def test_mark_notification_read_and_mark_all(self, context):
        result = execute(
            context, f'mutation {{ markNotificationRead(id: "{N1}") {{ isRead }} }}'
        )
        assert result.errors is None
        assert result.data["markNotificationRead"]["isRead"] is True

        result = execute(context, "mutation { markAllNotificationsRead }")
        assert result.errors is None
        assert result.data["markAllNotificationsRead"] == 1

        result = execute(context, "{ unreadNotificationsCount }")
        assert result.data["unreadNotificationsCount"] == 0
