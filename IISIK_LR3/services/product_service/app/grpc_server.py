from __future__ import annotations

from concurrent import futures
from decimal import Decimal

import grpc

import shared.protogen
import product_pb2
import product_pb2_grpc
from shared.grpc_errors import grpc_error_boundary

from . import service
from .db import SessionLocal


def _to_proto(dto) -> product_pb2.Product:
    return product_pb2.Product(
        id=dto.id,
        name=dto.name,
        description=dto.description,
        category=dto.category,
        base_price=str(dto.base_price),
        currency=dto.currency,
        is_active=dto.is_active,
        created_at=dto.created_at.isoformat(),
        updated_at=dto.updated_at.isoformat(),
    )


class ProductGrpcService(product_pb2_grpc.ProductServiceServicer):
    def ListProducts(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            items = service.list_products(
                session,
                request.category if request.HasField("category") else None,
                request.is_active if request.HasField("is_active") else None,
                request.search if request.HasField("search") else None,
                Decimal(request.min_price) if request.HasField("min_price") else None,
                Decimal(request.max_price) if request.HasField("max_price") else None,
                request.sort or "name",
                request.order or "asc",
            )
            return product_pb2.ListProductsResponse(
                products=[_to_proto(item) for item in items]
            )

    def GetProduct(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.get_product(session, request.id)
            return product_pb2.GetProductResponse(product=_to_proto(dto))

    def CreateProduct(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.create_product(
                session,
                _create_dto(request),
            )
            return _to_proto(dto)

    def UpdateProduct(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.update_product(session, request.id, _update_dto(request))
            return _to_proto(dto)


def _create_dto(request):
    from .schemas import ProductCreateDTO

    return ProductCreateDTO(
        name=request.name,
        description=request.description if request.HasField("description") else None,
        category=request.category,
        base_price=Decimal(request.base_price),
        currency=request.currency or "BYN",
    )


def _update_dto(request):
    from .schemas import ProductUpdateDTO

    data: dict[str, object] = {}
    if request.HasField("base_price"):
        data["base_price"] = Decimal(request.base_price)
    if request.HasField("description"):
        data["description"] = request.description
    if request.HasField("is_active"):
        data["is_active"] = request.is_active
    return ProductUpdateDTO.model_validate(data)


def start_grpc_server(port: int) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        ProductGrpcService(), server
    )
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    return server
