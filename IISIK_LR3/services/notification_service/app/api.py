from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from shared.errors import DomainError

from . import service
from .config import settings
from .db import engine, get_session
from .models import Base
from .schemas import NotificationCreateDTO, NotificationDTO


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Notification Service", version="1.0.0", lifespan=lifespan)


@app.exception_handler(DomainError)
def domain_error_handler(_: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.http_status,
        content={"code": exc.code, "message": exc.message},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


@app.get("/")
def root() -> dict[str, object]:
    return {
        "service": settings.service_name,
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
        "endpoints": [
            "/notifications?is_read=&notification_type=",
            "/notifications/unread-count",
            "POST /notifications",
            "PATCH /notifications/{notification_id}/read",
            "POST /notifications/read-all",
        ],
    }


@app.get("/notifications", response_model=list[NotificationDTO])
def list_notifications(
    is_read: bool | None = None,
    notification_type: str | None = None,
    session: Session = Depends(get_session),
) -> list[NotificationDTO]:
    return service.list_notifications(session, is_read, notification_type)


@app.post("/notifications", response_model=NotificationDTO, status_code=201)
def create_notification(
    data: NotificationCreateDTO, session: Session = Depends(get_session)
) -> NotificationDTO:
    return service.create_notification(session, data)


@app.patch("/notifications/{notification_id}/read", response_model=NotificationDTO)
def mark_notification_read(
    notification_id: str, session: Session = Depends(get_session)
) -> NotificationDTO:
    return service.mark_notification_read(session, notification_id)


@app.post("/notifications/read-all")
def mark_all_notifications_read(
    session: Session = Depends(get_session),
) -> dict[str, int]:
    return {"updated": service.mark_all_notifications_read(session)}


@app.get("/notifications/unread-count")
def unread_count(session: Session = Depends(get_session)) -> dict[str, int]:
    return {"unread": service.get_unread_count(session)}
