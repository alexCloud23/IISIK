from __future__ import annotations

from concurrent import futures
from datetime import datetime
from decimal import Decimal

import grpc

import shared.protogen
import strategy_pb2
import strategy_pb2_grpc
from shared.grpc_errors import grpc_error_boundary
from shared.grpc_logging import LoggingServerInterceptor

from . import service
from .db import SessionLocal
from .schemas import CompetitorPricePointDTO, StrategyAnalyzeDTO


def _to_proto(dto) -> strategy_pb2.Strategy:
    return strategy_pb2.Strategy(
        id=dto.id,
        product_id=dto.product_id,
        competitor_name=dto.competitor_name,
        strategy_type=dto.strategy_type,
        competitor_price=str(dto.competitor_price),
        price_change_percent=(
            str(dto.price_change_percent)
            if dto.price_change_percent is not None
            else None
        ),
        estimated_probability=(
            str(dto.estimated_probability)
            if dto.estimated_probability is not None
            else None
        ),
        created_at=dto.created_at.isoformat(),
    )


class StrategyGrpcService(strategy_pb2_grpc.StrategyServiceServicer):
    def ListStrategies(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            items = service.list_strategies(
                session,
                request.product_id if request.HasField("product_id") else None,
            )
            return strategy_pb2.ListStrategiesResponse(
                strategies=[_to_proto(item) for item in items]
            )

    def AnalyzeStrategy(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.analyze_strategy(
                session,
                StrategyAnalyzeDTO(
                    product_id=request.product_id,
                    current_price=Decimal(request.current_price),
                    competitor_prices=[
                        CompetitorPricePointDTO(
                            competitor_name=point.competitor_name,
                            price=Decimal(point.price),
                            observed_at=(
                                datetime.fromisoformat(point.observed_at)
                                if point.HasField("observed_at")
                                else None
                            ),
                        )
                        for point in request.competitor_prices
                    ],
                ),
            )
            return _to_proto(dto)


def start_grpc_server(port: int) -> grpc.Server:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4),
        interceptors=(LoggingServerInterceptor(),),
    )
    strategy_pb2_grpc.add_StrategyServiceServicer_to_server(
        StrategyGrpcService(), server
    )
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    return server
