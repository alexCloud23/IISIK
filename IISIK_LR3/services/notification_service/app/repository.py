from __future__ import annotations

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from .models import Notification


def get_notification(session: Session, notification_id: str) -> Notification | None:
    return session.get(Notification, notification_id)


def add_notification(session: Session, notification: Notification) -> Notification:
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


def list_notifications(
    session: Session,
    is_read: bool | None = None,
    notification_type: str | None = None,
) -> list[Notification]:
    stmt = select(Notification).order_by(Notification.created_at.desc())
    if is_read is not None:
        stmt = stmt.where(Notification.is_read == is_read)
    if notification_type is not None:
        stmt = stmt.where(Notification.notification_type == notification_type)
    return list(session.scalars(stmt))


def unread_count(session: Session) -> int:
    stmt = select(func.count(Notification.id)).where(Notification.is_read.is_(False))
    return int(session.scalar(stmt) or 0)


def mark_all_read(session: Session) -> int:
    stmt = (
        update(Notification)
        .where(Notification.is_read.is_(False))
        .values(is_read=True)
    )
    result = session.execute(stmt)
    session.commit()
    return int(result.rowcount or 0)
