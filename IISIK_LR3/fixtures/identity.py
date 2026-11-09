from __future__ import annotations

from fixtures.ids import ROLE, USER, uid
from fixtures.models import Role, User, UserRole, dt

ROLES: list[Role] = [
    Role(id=uid(ROLE, 1), name="ANALYST", description="Аналитик рынка и спроса"),
    Role(
        id=uid(ROLE, 2),
        name="PRICING_MANAGER",
        description="Менеджер по ценообразованию",
    ),
    Role(id=uid(ROLE, 3), name="ADMIN", description="Администратор системы"),
]

USERS: list[User] = [
    User(
        id=uid(USER, 1),
        email="analyst@example.com",
        password_hash="sha256:demo-analyst",
        full_name="Иванов Иван",
        is_active=True,
        created_at=dt(2026, 1, 15, 9),
    ),
    User(
        id=uid(USER, 2),
        email="manager@example.com",
        password_hash="sha256:demo-manager",
        full_name="Петрова Мария",
        is_active=True,
        created_at=dt(2026, 2, 1, 11),
    ),
    User(
        id=uid(USER, 3),
        email="admin@example.com",
        password_hash="sha256:demo-admin",
        full_name="Сидоров Алексей",
        is_active=True,
        created_at=dt(2026, 1, 10, 8),
    ),
]

USER_ROLES: list[UserRole] = [
    UserRole(user_id=uid(USER, 1), role_id=uid(ROLE, 1)),
    UserRole(user_id=uid(USER, 2), role_id=uid(ROLE, 2)),
    UserRole(user_id=uid(USER, 3), role_id=uid(ROLE, 3)),
]
