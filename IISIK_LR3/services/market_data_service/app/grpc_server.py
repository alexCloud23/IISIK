from __future__ import annotations

from concurrent import futures

import grpc

import shared.protogen
import market_data_pb2
import market_data_pb2_grpc
from shared.grpc_errors import grpc_error_boundary
from shared.grpc_logging import LoggingServerInterceptor

from . import service
from .db import SessionLocal


def _sales_to_proto(dto) -> market_data_pb2.SalesRecord:
    return market_data_pb2.SalesRecord(
        id=dto.id,
        product_id=dto.product_id,
        quantity=dto.quantity,
        unit_price=str(dto.unit_price),
        currency=dto.currency,
        sold_at=dto.sold_at.isoformat(),
    )


def _price_to_proto(dto) -> market_data_pb2.CompetitorPrice:
    return market_data_pb2.CompetitorPrice(
        id=dto.id,
        product_id=dto.product_id,
        competitor_name=dto.competitor_name,
        price=str(dto.price),
        currency=dto.currency,
        source=dto.source,
        observed_at=dto.observed_at.isoformat(),
    )


class MarketDataGrpcService(market_data_pb2_grpc.MarketDataServiceServicer):
    def SalesSummary(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.get_sales_summary(session, request.product_id)
            return market_data_pb2.SalesSummaryResponse(
                product_id=dto.product_id,
                records=dto.records,
                total_quantity=dto.total_quantity,
                average_unit_price=str(dto.average_unit_price),
            )

    def ListSales(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            items = service.list_sales(
                session,
                request.product_id if request.HasField("product_id") else None,
                request.limit or 1000,
            )
            return market_data_pb2.ListSalesResponse(
                sales=[_sales_to_proto(item) for item in items]
            )

    def ListCompetitorPrices(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            items = service.list_competitor_prices(
                session,
                request.product_id if request.HasField("product_id") else None,
                request.limit or 1000,
            )
            return market_data_pb2.ListCompetitorPricesResponse(
                prices=[_price_to_proto(item) for item in items]
            )


def start_grpc_server(port: int) -> grpc.Server:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4),
        interceptors=(LoggingServerInterceptor(),),
    )
    market_data_pb2_grpc.add_MarketDataServiceServicer_to_server(
        MarketDataGrpcService(), server
    )
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    return server
