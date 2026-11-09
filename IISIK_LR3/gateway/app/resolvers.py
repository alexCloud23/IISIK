from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from graphql import GraphQLError

from shared.errors import (
    DomainError,
    InvalidIdError,
    NotFoundError,
    UpstreamUnavailableError,
)

_TRANSLATED = (NotFoundError, InvalidIdError, UpstreamUnavailableError)


@contextmanager
def translate_errors() -> Iterator[None]:
    try:
        yield
    except _TRANSLATED as exc:
        raise GraphQLError(exc.message, extensions={"code": exc.code}) from exc
    except DomainError as exc:
        raise GraphQLError(exc.message, extensions={"code": exc.code}) from exc
