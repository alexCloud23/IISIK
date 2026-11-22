from __future__ import annotations

from concurrent import futures
from datetime import datetime
from decimal import Decimal

import grpc

import shared.protogen
import forecast_pb2
import forecast_pb2_grpc
from shared.grpc_errors import grpc_error_boundary
from shared.grpc_logging import LoggingServerInterceptor

from . import service
from .db import SessionLocal
from .schemas import ForecastGenerateDTO, SalePointDTO


def _to_proto(dto) -> forecast_pb2.Forecast:
    return forecast_pb2.Forecast(
        id=dto.id,
        product_id=dto.product_id,
        period_start=dto.period_start.isoformat(),
        period_end=dto.period_end.isoformat(),
        predicted_demand=str(dto.predicted_demand),
        confidence=(
            str(dto.confidence) if dto.confidence is not None else None
        ),
        model_version=dto.model_version,
        created_at=dto.created_at.isoformat(),
    )


class ForecastGrpcService(forecast_pb2_grpc.ForecastServiceServicer):
    def ListForecasts(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            items = service.list_forecasts(
                session,
                request.product_id if request.HasField("product_id") else None,
            )
            return forecast_pb2.ListForecastsResponse(
                forecasts=[_to_proto(item) for item in items]
            )

    def GetForecast(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.get_forecast(session, request.id)
            return forecast_pb2.GetForecastResponse(forecast=_to_proto(dto))

    def GenerateForecast(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.generate_forecast(
                session,
                ForecastGenerateDTO(
                    product_id=request.product_id,
                    period_days=request.period_days or 7,
                    sales=[
                        SalePointDTO(
                            quantity=point.quantity,
                            sold_at=datetime.fromisoformat(point.sold_at),
                        )
                        for point in request.sales
                    ],
                ),
            )
            return _to_proto(dto)


def start_grpc_server(port: int) -> grpc.Server:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4),
        interceptors=(LoggingServerInterceptor(),),
    )
    forecast_pb2_grpc.add_ForecastServiceServicer_to_server(
        ForecastGrpcService(), server
    )
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    return server
