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
from .schemas import CompetitorPriceDTO, SalesRecordDTO, SalesSummaryDTO


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Market Data Service", version="1.0.0", lifespan=lifespan)


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
            "/competitor-prices?product_id=",
            "/sales-history?product_id=",
            "/sales-summary?product_id=",
        ],
    }


@app.get("/competitor-prices", response_model=list[CompetitorPriceDTO])
def list_competitor_prices(
    product_id: str | None = None,
    limit: int = 100,
    session: Session = Depends(get_session),
) -> list[CompetitorPriceDTO]:
    return service.list_competitor_prices(session, product_id, limit)


@app.get("/sales-history", response_model=list[SalesRecordDTO])
def list_sales(
    product_id: str | None = None,
    limit: int = 100,
    session: Session = Depends(get_session),
) -> list[SalesRecordDTO]:
    return service.list_sales(session, product_id, limit)


@app.get("/sales-summary", response_model=SalesSummaryDTO)
def get_sales_summary(
    product_id: str, session: Session = Depends(get_session)
) -> SalesSummaryDTO:
    return service.get_sales_summary(session, product_id)
