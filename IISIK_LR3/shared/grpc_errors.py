from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import NoReturn

import grpc

from .errors import (
    DomainError,
    ForbiddenError,
    InvalidFilterError,
    InvalidIdError,
    InvalidInputError,
    InvalidOperationError,
    NotFoundError,
    UnauthorizedError,
    UpstreamUnavailableError,
)

_TO_GRPC: dict[type[DomainError], grpc.StatusCode] = {
    NotFoundError: grpc.StatusCode.NOT_FOUND,
    InvalidIdError: grpc.StatusCode.INVALID_ARGUMENT,
    InvalidFilterError: grpc.StatusCode.INVALID_ARGUMENT,
    InvalidInputError: grpc.StatusCode.INVALID_ARGUMENT,
    InvalidOperationError: grpc.StatusCode.FAILED_PRECONDITION,
    UnauthorizedError: grpc.StatusCode.UNAUTHENTICATED,
    ForbiddenError: grpc.StatusCode.PERMISSION_DENIED,
}

_BY_CODE: dict[str, type[DomainError]] = {
    cls.code: cls for cls in _TO_GRPC
}

_FALLBACK: dict[grpc.StatusCode, type[DomainError]] = {
    grpc.StatusCode.NOT_FOUND: NotFoundError,
    grpc.StatusCode.INVALID_ARGUMENT: InvalidInputError,
    grpc.StatusCode.FAILED_PRECONDITION: InvalidOperationError,
    grpc.StatusCode.UNAUTHENTICATED: UnauthorizedError,
    grpc.StatusCode.PERMISSION_DENIED: ForbiddenError,
}


@contextmanager
def grpc_error_boundary(context: grpc.ServicerContext) -> Iterator[None]:
    try:
        yield
    except DomainError as exc:
        context.set_trailing_metadata((("error-code", exc.code),))
        context.abort(_TO_GRPC.get(type(exc), grpc.StatusCode.INTERNAL), exc.message)


def raise_domain_error(exc: grpc.RpcError, target: str) -> NoReturn:
    code = None
    for key, value in exc.trailing_metadata() or ():
        if key == "error-code":
            code = value
    error_cls = _BY_CODE.get(code) if code else _FALLBACK.get(exc.code())
    if error_cls is None:
        raise UpstreamUnavailableError(
            f"Сервис {target} недоступен: {exc.code().name}"
        ) from exc
    raise error_cls(exc.details() or "Ошибка сервиса") from exc
