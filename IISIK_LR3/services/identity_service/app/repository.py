from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Role, User, UserRole


def get_user(session: Session, user_id: str) -> User | None:
    return session.get(User, user_id)


def list_users(session: Session, is_active: bool | None = None) -> list[User]:
    stmt = select(User).order_by(User.full_name)
    if is_active is not None:
        stmt = stmt.where(User.is_active == is_active)
    return list(session.scalars(stmt))


def list_roles(session: Session) -> list[Role]:
    return list(session.scalars(select(Role).order_by(Role.name)))


def get_role(session: Session, role_id: str) -> Role | None:
    return session.get(Role, role_id)


def roles_for_user(session: Session, user_id: str) -> list[Role]:
    stmt = (
        select(Role)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
        .order_by(Role.name)
    )
    return list(session.scalars(stmt))
