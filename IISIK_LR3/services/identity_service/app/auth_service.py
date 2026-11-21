from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from shared.auth import decode_token, hash_password, issue_token, verify_password
from shared.errors import InvalidInputError, InvalidOperationError, UnauthorizedError

from . import repository, sessions
from .config import settings
from .models import User, UserRole
from .schemas import AuthPayloadDTO, IntrospectDTO, UserDTO

DEFAULT_ROLE = "ANALYST"


def _role_names(session: Session, user_id: str) -> list[str]:
    return [role.name for role in repository.roles_for_user(session, user_id)]


def register(
    session: Session, email: str, password: str, full_name: str
) -> AuthPayloadDTO:
    email = email.strip().lower()
    if not email or "@" not in email:
        raise InvalidInputError("Некорректный email")
    if len(password) < 6:
        raise InvalidInputError("Пароль должен содержать не менее 6 символов")
    if not full_name.strip():
        raise InvalidInputError("Имя пользователя не может быть пустым")
    if repository.get_user_by_email(session, email) is not None:
        raise InvalidOperationError(f"Пользователь с email {email} уже существует")

    role = repository.get_role_by_name(session, DEFAULT_ROLE)
    if role is None:
        raise InvalidOperationError(f"Базовая роль {DEFAULT_ROLE} не найдена")

    user = User(
        id=str(uuid.uuid4()),
        email=email,
        password_hash=hash_password(password),
        full_name=full_name.strip(),
        is_active=True,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    session.add(user)
    session.add(UserRole(user_id=user.id, role_id=role.id))
    session.commit()
    return _issue(session, user)


def login(session: Session, email: str, password: str) -> AuthPayloadDTO:
    user = repository.get_user_by_email(session, email.strip().lower())
    if user is None or not verify_password(password, user.password_hash):
        raise UnauthorizedError("Неверный email или пароль")
    if not user.is_active:
        raise UnauthorizedError("Учётная запись деактивирована")
    return _issue(session, user)


def _issue(session: Session, user: User) -> AuthPayloadDTO:
    roles = _role_names(session, user.id)
    token, jti = issue_token(
        user.id, roles, settings.jwt_secret, settings.jwt_ttl_seconds
    )
    sessions.create_session(jti, user.id, settings.session_ttl_seconds)
    return AuthPayloadDTO(
        token=token, user=UserDTO.model_validate(user), roles=roles
    )


def logout(token: str) -> None:
    payload = decode_token(token, settings.jwt_secret)
    sessions.delete_session(payload["jti"])


def introspect(session: Session, token: str) -> IntrospectDTO:
    payload = decode_token(token, settings.jwt_secret)
    if not sessions.session_exists(payload["jti"]):
        raise UnauthorizedError("Сессия истекла или завершена, требуется повторный вход")
    user = repository.get_user(session, payload["sub"])
    if user is None or not user.is_active:
        raise UnauthorizedError("Пользователь не найден или деактивирован")
    return IntrospectDTO(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        roles=_role_names(session, user.id),
    )
