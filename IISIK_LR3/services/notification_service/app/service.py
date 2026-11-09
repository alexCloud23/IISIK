from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from fixtures.ids import USER, uid
from shared.errors import NotFoundError, parse_uuid
from shared.validation import validate_non_empty

from . import repository
from .models import Notification
from .schemas import NotificationCreateDTO, NotificationDTO

DEFAULT_USER_ID = uid(USER, 1)


def list_notifications(
    session: Session,
    is_read: bool | None = None,
    notification_type: str | None = None,
) -> list[NotificationDTO]:
    return [
        NotificationDTO.model_validate(row)
        for row in repository.list_notifications(session, is_read, notification_type)
    ]


def get_unread_count(session: Session) -> int:
    return repository.unread_count(session)


def create_notification(
    session: Session, data: NotificationCreateDTO
) -> NotificationDTO:
    notification_type = validate_non_empty(data.notification_type, "notification_type")
    title = validate_non_empty(data.title, "title")
    message = validate_non_empty(data.message, "message")

    user_id = DEFAULT_USER_ID
    if data.user_id is not None:
        user_id = str(parse_uuid(data.user_id, "user_id"))
    related_entity_id = None
    if data.related_entity_id is not None:
        related_entity_id = str(
            parse_uuid(data.related_entity_id, "related_entity_id")
        )

    now = datetime.utcnow()
    notification = repository.add_notification(
        session,
        Notification(
            id=str(uuid4()),
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=message,
            related_entity_id=related_entity_id,
            status="SENT",
            is_read=False,
            created_at=now,
            sent_at=now,
        ),
    )
    return NotificationDTO.model_validate(notification)


def mark_notification_read(session: Session, notification_id: str) -> NotificationDTO:
    parsed = parse_uuid(notification_id, "notification_id")
    notification = repository.get_notification(session, str(parsed))
    if notification is None:
        raise NotFoundError(f"Уведомление {notification_id} не найдено")

    notification.is_read = True
    session.commit()
    session.refresh(notification)
    return NotificationDTO.model_validate(notification)


def mark_all_notifications_read(session: Session) -> int:
    return repository.mark_all_read(session)
