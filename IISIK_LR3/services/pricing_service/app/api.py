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
from .providers import ForecastProvider, get_forecast_provider
from .schemas import (
    RecommendationCreateDTO,
    RecommendationDecisionDTO,
    RecommendationDTO,
    RecommendationSummaryDTO,
    RecommendationWithForecastDTO,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Pricing Service", version="1.0.0", lifespan=lifespan)


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
            "/recommendations?product_id=&status=&sort=&order=",
            "/recommendations/{recommendation_id}",
            "POST /recommendations",
            "PATCH /recommendations/{recommendation_id}/decision",
            "/recommendations/summary",
        ],
    }


@app.get("/recommendations", response_model=list[RecommendationDTO])
def list_recommendations(
    product_id: str | None = None,
    status: str | None = None,
    sort: str = "created",
    order: str = "desc",
    session: Session = Depends(get_session),
) -> list[RecommendationDTO]:
    return service.list_recommendations(session, product_id, status, sort, order)


@app.get("/recommendations/summary", response_model=RecommendationSummaryDTO)
def recommendations_summary(
    session: Session = Depends(get_session),
) -> RecommendationSummaryDTO:
    return RecommendationSummaryDTO(**service.recommendations_summary(session))


@app.post("/recommendations", response_model=RecommendationDTO, status_code=201)
def create_recommendation(
    data: RecommendationCreateDTO, session: Session = Depends(get_session)
) -> RecommendationDTO:
    return service.create_recommendation(session, data)


@app.patch(
    "/recommendations/{recommendation_id}/decision",
    response_model=RecommendationDTO,
)
def decide_recommendation(
    recommendation_id: str,
    data: RecommendationDecisionDTO,
    session: Session = Depends(get_session),
) -> RecommendationDTO:
    return service.decide_recommendation(session, recommendation_id, data.decision)


@app.get(
    "/recommendations/{recommendation_id}",
    response_model=RecommendationWithForecastDTO,
)
def get_recommendation(
    recommendation_id: str,
    session: Session = Depends(get_session),
    provider: ForecastProvider = Depends(get_forecast_provider),
) -> RecommendationWithForecastDTO:
    return service.get_recommendation_with_forecast(
        session, recommendation_id, provider
    )
