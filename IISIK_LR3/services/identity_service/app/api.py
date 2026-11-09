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
from .schemas import RoleDTO, UserDTO


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Identity Service", version="1.0.0", lifespan=lifespan)


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
            "/users",
            "/users/{user_id}",
            "/users/{user_id}/roles",
            "/roles",
            "/roles/{role_id}",
        ],
    }


@app.get("/users", response_model=list[UserDTO])
def list_users(
    is_active: bool | None = None, session: Session = Depends(get_session)
) -> list[UserDTO]:
    return service.list_users(session, is_active)


@app.get("/users/{user_id}", response_model=UserDTO)
def get_user(user_id: str, session: Session = Depends(get_session)) -> UserDTO:
    return service.get_user(session, user_id)


@app.get("/users/{user_id}/roles", response_model=list[RoleDTO])
def get_user_roles(
    user_id: str, session: Session = Depends(get_session)
) -> list[RoleDTO]:
    return service.get_user_roles(session, user_id)


@app.get("/roles", response_model=list[RoleDTO])
def list_roles(session: Session = Depends(get_session)) -> list[RoleDTO]:
    return service.list_roles(session)


@app.get("/roles/{role_id}", response_model=RoleDTO)
def get_role(role_id: str, session: Session = Depends(get_session)) -> RoleDTO:
    return service.get_role(session, role_id)
