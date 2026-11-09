from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotificationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    notification_type: str
    title: str
    message: str
    related_entity_id: str | None
    status: str
    is_read: bool
    created_at: datetime
    sent_at: datetime | None


class NotificationCreateDTO(BaseModel):
    notification_type: str
    title: str
    message: str
    related_entity_id: str | None = None
    user_id: str | None = None
