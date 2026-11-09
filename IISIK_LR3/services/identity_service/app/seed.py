from __future__ import annotations

from sqlalchemy import delete
from sqlalchemy.orm import Session

from fixtures.identity import ROLES, USERS, USER_ROLES

from .models import Role, User, UserRole


def seed(session: Session) -> int:
    session.execute(delete(UserRole))
    session.execute(delete(User))
    session.execute(delete(Role))

    session.add_all(
        [
            Role(id=item.id, name=item.name, description=item.description)
            for item in ROLES
        ]
    )
    session.add_all(
        [
            User(
                id=item.id,
                email=item.email,
                password_hash=item.password_hash,
                full_name=item.full_name,
                is_active=item.is_active,
                created_at=item.created_at,
            )
            for item in USERS
        ]
    )
    session.add_all(
        [UserRole(user_id=item.user_id, role_id=item.role_id) for item in USER_ROLES]
    )
    session.commit()
    return len(USERS) + len(ROLES) + len(USER_ROLES)
