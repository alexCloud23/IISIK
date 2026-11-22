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
from .schemas import ForecastDTO, ForecastGenerateDTO


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(engine)
    grpc_server = start_grpc_server(settings.grpc_port)
    yield
    grpc_server.stop(grace=1).wait()


app = FastAPI(title="Demand Forecast Service", version="1.0.0", lifespan=lifespan)


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
            "/forecasts?product_id=",
            "/forecasts/{forecast_id}",
            "POST /forecasts/generate",
        ],
    }


@app.get("/forecasts", response_model=list[ForecastDTO])
def list_forecasts(
    product_id: str | None = None, session: Session = Depends(get_session)
) -> list[ForecastDTO]:
    return service.list_forecasts(session, product_id)


@app.post("/forecasts/generate", response_model=ForecastDTO, status_code=201)
def generate_forecast(
    data: ForecastGenerateDTO, session: Session = Depends(get_session)
) -> ForecastDTO:
    return service.generate_forecast(session, data)


@app.get("/forecasts/{forecast_id}", response_model=ForecastDTO)
def get_forecast(
    forecast_id: str, session: Session = Depends(get_session)
) -> ForecastDTO:
    return service.get_forecast(session, forecast_id)
