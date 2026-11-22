from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from shared.errors import DomainError

from . import service
from shared.logging import setup_logging

from .config import settings

setup_logging(settings.service_name)
from .db import engine, get_session
from .grpc_server import start_grpc_server
from .models import Base
from .schemas import StrategyAnalyzeDTO, StrategyDTO


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(engine)
    grpc_server = start_grpc_server(settings.grpc_port)
    yield
    grpc_server.stop(grace=1).wait()


app = FastAPI(
    title="Competitive Strategy Service", version="1.0.0", lifespan=lifespan
)


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
            "/strategies?product_id=",
            "POST /strategies/analyze",
        ],
    }


@app.get("/strategies", response_model=list[StrategyDTO])
def list_strategies(
    product_id: str | None = None, session: Session = Depends(get_session)
) -> list[StrategyDTO]:
    return service.list_strategies(session, product_id)


@app.post("/strategies/analyze", response_model=StrategyDTO, status_code=201)
def analyze_strategy(
    data: StrategyAnalyzeDTO, session: Session = Depends(get_session)
) -> StrategyDTO:
    return service.analyze_strategy(session, data)
