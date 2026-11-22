from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import TypeVar

import grpc

T = TypeVar("T")

logger = logging.getLogger(__name__)

RETRYABLE_GRPC_CODES = frozenset(
    {
        grpc.StatusCode.UNAVAILABLE,
        grpc.StatusCode.DEADLINE_EXCEEDED,
        grpc.StatusCode.RESOURCE_EXHAUSTED,
    }
)


def is_retryable_grpc(exc: BaseException) -> bool:
    return isinstance(exc, grpc.RpcError) and exc.code() in RETRYABLE_GRPC_CODES


def is_retryable_http(exc: BaseException) -> bool:
    import httpx

    return isinstance(exc, httpx.TransportError)


def call_with_retry(
    func: Callable[[], T],
    *,
    label: str,
    attempts: int = 3,
    backoff: float = 0.2,
    retryable: Callable[[BaseException], bool] = is_retryable_grpc,
) -> T:
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except Exception as exc:
            if attempt >= attempts or not retryable(exc):
                if attempts > 1 and retryable(exc):
                    logger.error(
                        "%s: все %d попыток исчерпаны, последняя ошибка: %s",
                        label,
                        attempts,
                        exc,
                    )
                raise
            delay = backoff * (2 ** (attempt - 1))
            logger.warning(
                "%s: попытка %d/%d не удалась (%s), повтор через %.2f с",
                label,
                attempt,
                attempts,
                exc,
                delay,
            )
            time.sleep(delay)
    raise AssertionError("unreachable")
