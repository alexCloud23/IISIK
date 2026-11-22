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
from .grpc_server import start_grpc_server
from .models import Base
from .schemas import AnalyticsResultDTO, AnalyticsRunDTO


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(engine)
    grpc_server = start_grpc_server(settings.grpc_port)
    yield
    grpc_server.stop(grace=1).wait()


app = FastAPI(title="Analytics Service", version="1.0.0", lifespan=lifespan)


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
            "/analytics-results?analysis_type=",
            "POST /analytics-results/run",
        ],
    }


@app.get("/analytics-results", response_model=list[AnalyticsResultDTO])
def list_results(
    analysis_type: str | None = None, session: Session = Depends(get_session)
) -> list[AnalyticsResultDTO]:
    return service.list_results(session, analysis_type)


@app.post("/analytics-results/run", response_model=AnalyticsResultDTO, status_code=201)
def run_analysis(
    data: AnalyticsRunDTO, session: Session = Depends(get_session)
) -> AnalyticsResultDTO:
    return service.run_analysis(session, data)
