from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from decimal import Decimal

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from shared.errors import DomainError

from . import service
from .config import settings
from .db import engine, get_session
from .models import Base
from .schemas import ProductCreateDTO, ProductDTO, ProductUpdateDTO


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Product Service", version="1.0.0", lifespan=lifespan)


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
            "/products",
            "/products/{product_id}",
            "POST /products",
            "PATCH /products/{product_id}",
        ],
    }


@app.get("/products", response_model=list[ProductDTO])
def list_products(
    category: str | None = None,
    is_active: bool | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort: str = "name",
    order: str = "asc",
    session: Session = Depends(get_session),
) -> list[ProductDTO]:
    return service.list_products(
        session,
        category,
        is_active,
        search,
        None if min_price is None else Decimal(str(min_price)),
        None if max_price is None else Decimal(str(max_price)),
        sort,
        order,
    )


@app.post("/products", response_model=ProductDTO, status_code=201)
def create_product(
    data: ProductCreateDTO, session: Session = Depends(get_session)
) -> ProductDTO:
    return service.create_product(session, data)


@app.patch("/products/{product_id}", response_model=ProductDTO)
def update_product(
    product_id: str,
    data: ProductUpdateDTO,
    session: Session = Depends(get_session),
) -> ProductDTO:
    return service.update_product(session, product_id, data)


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(
    product_id: str, session: Session = Depends(get_session)
) -> ProductDTO:
    return service.get_product(session, product_id)
