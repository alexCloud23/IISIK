from __future__ import annotations

import uuid

import fakeredis

from fixtures.identity import ROLES, USER_ROLES, USERS
from shared.auth import decode_token, hash_password, issue_token, verify_password
from shared.errors import (
    InvalidInputError,
    InvalidOperationError,
    UnauthorizedError,
)

from ...dto import AuthPayloadData, AuthUserData

DEFAULT_ROLE = "ANALYST"
MOCK_JWT_SECRET = "dev-secret-change-me"


class MockAuthClient:
    def __init__(
        self,
        jwt_ttl_seconds: int = 3600,
        session_ttl_seconds: int = 1800,
    ) -> None:
        self._jwt_ttl_seconds = jwt_ttl_seconds
        self._session_ttl_seconds = session_ttl_seconds
        self._users: dict[str, dict] = {}
        self._role_names: dict[str, str] = {role.id: role.name for role in ROLES}
        self._user_roles: dict[str, list[str]] = {}
        for user in USERS:
            self._users[user.email] = {
                "id": user.id,
                "email": user.email,
                "password_hash": user.password_hash,
                "full_name": user.full_name,
                "is_active": user.is_active,
            }
        for link in USER_ROLES:
            self._user_roles.setdefault(link.user_id, []).append(
                self._role_names[link.role_id]
            )
        self._sessions = fakeredis.FakeStrictRedis(decode_responses=True)

    def close(self) -> None:
        self._sessions.close()

    def _roles(self, user_id: str) -> list[str]:
        return list(self._user_roles.get(user_id, []))

    def _issue(self, user: dict) -> AuthPayloadData:
        roles = self._roles(user["id"])
        token, jti = issue_token(
            user["id"], roles, MOCK_JWT_SECRET, self._jwt_ttl_seconds
        )
        self._sessions.set(
            f"session:{jti}", user["id"], ex=self._session_ttl_seconds
        )
        return AuthPayloadData(
            token=token,
            user=AuthUserData(
                id=user["id"],
                email=user["email"],
                full_name=user["full_name"],
                roles=roles,
            ),
        )

    def login(self, email: str, password: str) -> AuthPayloadData:
        user = self._users.get(email.strip().lower())
        if user is None or not verify_password(password, user["password_hash"]):
            raise UnauthorizedError("Неверный email или пароль")
        if not user["is_active"]:
            raise UnauthorizedError("Учётная запись деактивирована")
        return self._issue(user)

    def register(
        self, email: str, password: str, full_name: str
    ) -> AuthPayloadData:
        email = email.strip().lower()
        if not email or "@" not in email:
            raise InvalidInputError("Некорректный email")
        if len(password) < 6:
            raise InvalidInputError("Пароль должен содержать не менее 6 символов")
        if not full_name.strip():
            raise InvalidInputError("Имя пользователя не может быть пустым")
        if email in self._users:
            raise InvalidOperationError(
                f"Пользователь с email {email} уже существует"
            )
        user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password_hash": hash_password(password),
            "full_name": full_name.strip(),
            "is_active": True,
        }
        self._users[email] = user
        self._user_roles[user["id"]] = [DEFAULT_ROLE]
        return self._issue(user)

    def logout(self, token: str) -> None:
        payload = decode_token(token, MOCK_JWT_SECRET)
        self._sessions.delete(f"session:{payload['jti']}")

    def introspect(self, token: str) -> AuthUserData:
        payload = decode_token(token, MOCK_JWT_SECRET)
        if not self._sessions.exists(f"session:{payload['jti']}"):
            raise UnauthorizedError(
                "Сессия истекла или завершена, требуется повторный вход"
            )
        user_id = payload["sub"]
        user = next(
            (item for item in self._users.values() if item["id"] == user_id), None
        )
        if user is None or not user["is_active"]:
            raise UnauthorizedError("Пользователь не найден или деактивирован")
        return AuthUserData(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            roles=self._roles(user["id"]),
        )
