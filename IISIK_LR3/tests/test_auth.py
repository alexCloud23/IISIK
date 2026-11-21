from __future__ import annotations

import time
import uuid

import httpx
import pytest
from starlette.testclient import TestClient

from gateway.app.clients.factory import build_http_bundle, build_mock_bundle
from gateway.app.clients.mock import MockAuthClient
from gateway.app.config import Settings
from gateway.app.dto import AuthUserData
from gateway.app.schema.schema import schema
from shared.errors import (
    InvalidInputError,
    InvalidOperationError,
    UnauthorizedError,
)

from tests.test_mode_parity import _make_transport

ADMIN = ("admin@example.com", "admin")
ANALYST = ("analyst@example.com", "analyst")
MANAGER = ("manager@example.com", "manager")

P1 = "20000000-0000-4000-8000-000000000001"
R2 = "70000000-0000-4000-8000-000000000002"


def user_ctx(bundle, user: AuthUserData | None, token: str | None = None):
    return {"clients": bundle, "cache": {}, "user": user, "token": token}


def execute(ctx, query):
    return schema.execute_sync(query, context_value=ctx)


@pytest.fixture()
def bundle():
    instance = build_mock_bundle()
    yield instance
    instance.close()


def login(ctx, email=ADMIN[0], password=ADMIN[1]) -> str:
    result = execute(
        ctx,
        f'mutation {{ login(email: "{email}", password: "{password}")'
        " { token user { email roles } } }",
    )
    assert result.errors is None
    return result.data["login"]["token"]


class TestGraphQLAuth:
    def test_login_returns_token_and_roles(self, bundle):
        ctx = user_ctx(bundle, None)
        result = execute(
            ctx,
            f'mutation {{ login(email: "{ADMIN[0]}", password: "{ADMIN[1]}")'
            " { token user { email roles } } }",
        )
        assert result.errors is None
        payload = result.data["login"]
        assert payload["token"]
        assert payload["user"]["email"] == ADMIN[0]
        assert payload["user"]["roles"] == ["ADMIN"]

    def test_login_wrong_password(self, bundle):
        ctx = user_ctx(bundle, None)
        result = execute(
            ctx,
            f'mutation {{ login(email: "{ADMIN[0]}", password: "wrong-pass")'
            " { token } }",
        )
        assert result.errors[0].extensions["code"] == "UNAUTHENTICATED"

    def test_query_requires_authentication(self, bundle):
        result = execute(user_ctx(bundle, None), "{ products { id } }")
        assert result.errors[0].extensions["code"] == "UNAUTHENTICATED"

    def test_query_with_authenticated_user(self, bundle):
        ctx = user_ctx(bundle, None)
        token = login(ctx)
        authed = user_ctx(bundle, bundle.auth.introspect(token), token)
        result = execute(authed, "{ products { id } }")
        assert result.errors is None
        assert result.data["products"]

    def test_logout_invalidates_session(self, bundle):
        ctx = user_ctx(bundle, None)
        token = login(ctx)
        authed = user_ctx(bundle, bundle.auth.introspect(token), token)
        result = execute(authed, "mutation { logout }")
        assert result.errors is None
        with pytest.raises(UnauthorizedError):
            bundle.auth.introspect(token)
        result = execute(
            user_ctx(bundle, None), "{ products { id } }"
        )
        assert result.errors[0].extensions["code"] == "UNAUTHENTICATED"

    def test_expired_session_rejects_valid_jwt(self):
        client = MockAuthClient(session_ttl_seconds=1)
        payload = client.login(*ADMIN)
        time.sleep(1.1)
        with pytest.raises(UnauthorizedError):
            client.introspect(payload.token)

    def test_register_and_login(self, bundle):
        email = f"user-{uuid.uuid4().hex[:8]}@example.com"
        ctx = user_ctx(bundle, None)
        result = execute(
            ctx,
            f'mutation {{ register(email: "{email}", password: "secret123",'
            ' fullName: "Новый Пользователь") { token user { roles } } }',
        )
        assert result.errors is None
        assert result.data["register"]["user"]["roles"] == ["ANALYST"]

    def test_register_duplicate_email(self, bundle):
        with pytest.raises(InvalidOperationError):
            bundle.auth.register(ADMIN[0], "secret123", "Дубликат")

    def test_register_short_password(self, bundle):
        with pytest.raises(InvalidInputError):
            bundle.auth.register("short@example.com", "123", "Короткий")


class TestRoles:
    def _ctx(self, bundle, roles):
        user = AuthUserData(
            id="test-user", email="test@example.com",
            full_name="Тест", roles=roles,
        )
        return user_ctx(bundle, user)

    def test_analyst_cannot_decide_recommendation(self, bundle):
        ctx = self._ctx(bundle, ["ANALYST"])
        result = execute(
            ctx,
            f'mutation {{ decideRecommendation(id: "{R2}",'
            " decision: ACCEPTED) { id } }",
        )
        assert result.errors[0].extensions["code"] == "FORBIDDEN"

    def test_pricing_manager_decides_recommendation(self, bundle):
        ctx = self._ctx(bundle, ["PRICING_MANAGER"])
        result = execute(
            ctx,
            f'mutation {{ decideRecommendation(id: "{R2}",'
            " decision: REJECTED) { status } }",
        )
        assert result.errors is None
        assert result.data["decideRecommendation"]["status"] == "REJECTED"

    def test_pricing_manager_cannot_run_analytics(self, bundle):
        ctx = self._ctx(bundle, ["PRICING_MANAGER"])
        result = execute(
            ctx, f'mutation {{ runAnalytics(productId: "{P1}") {{ id }} }}'
        )
        assert result.errors[0].extensions["code"] == "FORBIDDEN"

    def test_analyst_runs_analytics(self, bundle):
        ctx = self._ctx(bundle, ["ANALYST"])
        result = execute(
            ctx,
            f'mutation {{ runAnalytics(productId: "{P1}") {{ analysisType }} }}',
        )
        assert result.errors is None

    def test_admin_can_do_everything(self, bundle):
        ctx = self._ctx(bundle, ["ADMIN"])
        for query in (
            f'mutation {{ runAnalytics(productId: "{P1}") {{ id }} }}',
            f'mutation {{ generatePriceRecommendation(productId: "{P1}") {{ id }} }}',
        ):
            result = execute(ctx, query)
            assert result.errors is None, query


@pytest.fixture(scope="module")
def http_bundle():
    from services.identity_service.app.api import Base, app, engine
    from services.identity_service.app.db import SessionLocal
    from services.identity_service.app.seed import seed

    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        seed(session)

    instance = build_http_bundle(
        Settings(client_mode="http"), {"auth": _make_transport(app)}
    )
    yield instance
    instance.close()


class TestHttpAuthClient:
    def test_login_and_introspect(self, http_bundle):
        payload = http_bundle.auth.login(*MANAGER)
        assert payload.token
        user = http_bundle.auth.introspect(payload.token)
        assert user.email == MANAGER[0]
        assert user.roles == ["PRICING_MANAGER"]

    def test_wrong_password(self, http_bundle):
        with pytest.raises(UnauthorizedError):
            http_bundle.auth.login(ADMIN[0], "wrong-pass")

    def test_logout_invalidates_session(self, http_bundle):
        payload = http_bundle.auth.login(*ANALYST)
        http_bundle.auth.logout(payload.token)
        with pytest.raises(UnauthorizedError):
            http_bundle.auth.introspect(payload.token)

    def test_register(self, http_bundle):
        email = f"http-{uuid.uuid4().hex[:8]}@example.com"
        payload = http_bundle.auth.register(email, "secret123", "HTTP Пользователь")
        assert payload.user.roles == ["ANALYST"]
        with pytest.raises(InvalidOperationError):
            http_bundle.auth.register(email, "secret123", "Дубликат")

    def test_introspect_garbage_token(self, http_bundle):
        with pytest.raises(UnauthorizedError):
            http_bundle.auth.introspect("not-a-jwt")
