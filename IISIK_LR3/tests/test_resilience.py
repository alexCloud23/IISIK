from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock

import grpc
import pytest

from gateway.app.cache import RedisCache
from gateway.app.clients.cached import CachedProductClient
from gateway.app.clients.grpc.clients import GrpcServiceClient
from gateway.app.dto import ProductData
from shared.errors import UpstreamUnavailableError
from shared.grpc_logging import LoggingServerInterceptor
from shared.resilience import call_with_retry


class _FakeRpcError(grpc.RpcError):
    def __init__(self, code: grpc.StatusCode) -> None:
        super().__init__()
        self._code = code

    def code(self) -> grpc.StatusCode:
        return self._code

    def details(self) -> str:
        return "boom"

    def trailing_metadata(self):
        return ()


def test_retry_succeeds_after_transient_failure() -> None:
    calls = {"n": 0}

    def flaky() -> str:
        calls["n"] += 1
        if calls["n"] == 1:
            raise _FakeRpcError(grpc.StatusCode.UNAVAILABLE)
        return "ok"

    assert call_with_retry(flaky, label="t", attempts=3, backoff=0) == "ok"
    assert calls["n"] == 2


def test_retry_exhausted_raises_after_all_attempts() -> None:
    calls = {"n": 0}

    def failing() -> str:
        calls["n"] += 1
        raise _FakeRpcError(grpc.StatusCode.DEADLINE_EXCEEDED)

    with pytest.raises(grpc.RpcError):
        call_with_retry(failing, label="t", attempts=3, backoff=0)
    assert calls["n"] == 3


def test_no_retry_on_domain_error() -> None:
    calls = {"n": 0}

    def failing() -> str:
        calls["n"] += 1
        raise _FakeRpcError(grpc.StatusCode.INVALID_ARGUMENT)

    with pytest.raises(grpc.RpcError):
        call_with_retry(failing, label="t", attempts=3, backoff=0)
    assert calls["n"] == 1


def test_grpc_client_retries_unavailable() -> None:
    client = GrpcServiceClient("127.0.0.1:1", retry_attempts=3, retry_backoff=0)
    attempts = {"n": 0}

    def method(request, timeout=None):
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise _FakeRpcError(grpc.StatusCode.UNAVAILABLE)
        return "resp"

    assert client._call(method, object()) == "resp"
    assert attempts["n"] == 2
    client.close()


def test_grpc_client_maps_exhausted_retry_to_upstream_error() -> None:
    client = GrpcServiceClient("127.0.0.1:1", retry_attempts=2, retry_backoff=0)
    attempts = {"n": 0}

    def method(request, timeout=None):
        attempts["n"] += 1
        raise _FakeRpcError(grpc.StatusCode.UNAVAILABLE)

    with pytest.raises(UpstreamUnavailableError):
        client._call(method, object())
    assert attempts["n"] == 2
    client.close()


def _product(product_id: str = "p1") -> ProductData:
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return ProductData(
        id=product_id,
        name="Товар",
        description=None,
        category="c",
        base_price=Decimal("10.00"),
        currency="BYN",
        is_active=True,
        created_at=now,
        updated_at=now,
    )


def test_cached_product_client_reads_cache_on_second_call() -> None:
    inner = MagicMock()
    inner.get_product.return_value = _product()
    client = CachedProductClient(inner, RedisCache("fakeredis://", 60))

    assert client.get_product("p1").name == "Товар"
    assert client.get_product("p1").name == "Товар"
    inner.get_product.assert_called_once_with("p1")


def test_cached_product_client_update_invalidates_cache() -> None:
    inner = MagicMock()
    inner.get_product.return_value = _product()
    inner.update_product.return_value = _product()
    client = CachedProductClient(inner, RedisCache("fakeredis://", 60))

    client.get_product("p1")
    client.update_product("p1", base_price=Decimal("12.00"))
    client.get_product("p1")

    assert inner.get_product.call_count == 2


def test_cached_product_client_survives_redis_failure() -> None:
    class _BrokenRedis:
        def get(self, key):
            raise ConnectionError("redis down")

        def set(self, *args, **kwargs):
            raise ConnectionError("redis down")

        def delete(self, *args):
            raise ConnectionError("redis down")

    cache = RedisCache("fakeredis://", 60)
    cache._client = _BrokenRedis()
    inner = MagicMock()
    inner.get_product.return_value = _product()
    client = CachedProductClient(inner, cache)

    assert client.get_product("p1").name == "Товар"
    inner.get_product.assert_called_once_with("p1")


def _grpc_handler(func):
    handler = MagicMock()
    handler.unary_unary = func
    handler.request_deserializer = None
    handler.response_serializer = None
    return handler


def test_logging_interceptor_passes_through_and_logs(caplog) -> None:
    import logging

    interceptor = LoggingServerInterceptor()
    handler = _grpc_handler(MagicMock(return_value="resp"))
    details = MagicMock(method="/svc/Method")
    wrapped = interceptor.intercept_service(lambda d: handler, details)

    with caplog.at_level(logging.INFO, "shared.grpc_logging"):
        assert wrapped.unary_unary("req", MagicMock()) == "resp"
    assert "/svc/Method" in caplog.text
    assert "OK" in caplog.text


def test_logging_interceptor_logs_and_reraises_errors(caplog) -> None:
    import logging

    interceptor = LoggingServerInterceptor()
    handler = _grpc_handler(MagicMock(side_effect=ValueError("boom")))
    details = MagicMock(method="/svc/Method")
    wrapped = interceptor.intercept_service(lambda d: handler, details)

    with pytest.raises(ValueError), caplog.at_level(logging.INFO, "shared.grpc_logging"):
        wrapped.unary_unary("req", MagicMock())
    assert "/svc/Method" in caplog.text
    assert "ValueError" in caplog.text
