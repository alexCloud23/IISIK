from __future__ import annotations

from sqlalchemy.orm import Session

from shared.errors import NotFoundError, parse_uuid

from . import repository
from .schemas import RoleDTO, UserDTO


def get_user(session: Session, user_id: str) -> UserDTO:
    parsed = parse_uuid(user_id, "user_id")
    user = repository.get_user(session, str(parsed))
    if user is None:
        raise NotFoundError(f"Пользователь {user_id} не найден")
    return UserDTO.model_validate(user)


def list_users(session: Session, is_active: bool | None = None) -> list[UserDTO]:
    return [UserDTO.model_validate(user) for user in repository.list_users(session, is_active)]


def list_roles(session: Session) -> list[RoleDTO]:
    return [RoleDTO.model_validate(role) for role in repository.list_roles(session)]


def get_role(session: Session, role_id: str) -> RoleDTO:
    parsed = parse_uuid(role_id, "role_id")
    role = repository.get_role(session, str(parsed))
    if role is None:
        raise NotFoundError(f"Роль {role_id} не найдена")
    return RoleDTO.model_validate(role)


def get_user_roles(session: Session, user_id: str) -> list[RoleDTO]:
    parsed = parse_uuid(user_id, "user_id")
    user = repository.get_user(session, str(parsed))
    if user is None:
        raise NotFoundError(f"Пользователь {user_id} не найден")
    return [RoleDTO.model_validate(role) for role in repository.roles_for_user(session, str(parsed))]
