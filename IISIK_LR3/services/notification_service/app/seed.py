from __future__ import annotations

from sqlalchemy import delete
from sqlalchemy.orm import Session

from fixtures.notification import NOTIFICATIONS

from .models import Notification


def seed(session: Session) -> int:
    session.execute(delete(Notification))
    session.add_all(
        [
            Notification(
                id=item.id,
                user_id=item.user_id,
                notification_type=item.notification_type,
                title=item.title,
                message=item.message,
                related_entity_id=item.related_entity_id,
                status=item.status,
                is_read=item.is_read,
                created_at=item.created_at,
                sent_at=item.sent_at,
            )
            for item in NOTIFICATIONS
        ]
    )
    session.commit()
    return len(NOTIFICATIONS)
