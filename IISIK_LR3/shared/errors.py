from __future__ import annotations

from uuid import UUID


class DomainError(Exception):
    code = "DOMAIN_ERROR"
    http_status = 400

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):
    code = "NOT_FOUND"
    http_status = 404


class InvalidIdError(DomainError):
    code = "INVALID_ID"
    http_status = 422


class InvalidFilterError(DomainError):
    code = "INVALID_FILTER"
    http_status = 422


class InvalidInputError(DomainError):
    code = "INVALID_INPUT"
    http_status = 400


class InvalidOperationError(DomainError):
    code = "INVALID_OPERATION"
    http_status = 409


class UpstreamUnavailableError(DomainError):
    code = "UPSTREAM_UNAVAILABLE"
    http_status = 502


def parse_uuid(value: str, field: str = "id") -> UUID:
    try:
        return UUID(str(value))
    except (ValueError, AttributeError, TypeError) as exc:
        raise InvalidIdError(
            f"Некорректный идентификатор {field}: {value!r}"
        ) from exc
