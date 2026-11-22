from __future__ import annotations

import json
from concurrent import futures
from decimal import Decimal

import grpc

import shared.protogen
import analytics_pb2
import analytics_pb2_grpc
from shared.grpc_errors import grpc_error_boundary
from shared.grpc_logging import LoggingServerInterceptor

from . import service
from .db import SessionLocal
from .schemas import AnalyticsRunDTO


def _to_proto(dto) -> analytics_pb2.AnalyticsResult:
    return analytics_pb2.AnalyticsResult(
        id=dto.id,
        product_id=dto.product_id,
        recommendation_id=dto.recommendation_id,
        analysis_type=dto.analysis_type,
        metrics_json=json.dumps(dto.metrics, ensure_ascii=False, default=str),
        created_at=dto.created_at.isoformat(),
    )


class AnalyticsGrpcService(analytics_pb2_grpc.AnalyticsServiceServicer):
    def ListResults(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            items = service.list_results(
                session,
                request.analysis_type if request.HasField("analysis_type") else None,
            )
            return analytics_pb2.ListResultsResponse(
                results=[_to_proto(item) for item in items]
            )

    def RunAnalysis(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.run_analysis(
                session,
                AnalyticsRunDTO(
                    product_id=request.product_id,
                    analysis_type=request.analysis_type or "SALES_SUMMARY",
                    records=request.records,
                    total_quantity=request.total_quantity,
                    average_unit_price=Decimal(request.average_unit_price),
                    predicted_demand=(
                        Decimal(request.predicted_demand)
                        if request.HasField("predicted_demand")
                        else None
                    ),
                    current_price=(
                        Decimal(request.current_price)
                        if request.HasField("current_price")
                        else None
                    ),
                    recommended_price=(
                        Decimal(request.recommended_price)
                        if request.HasField("recommended_price")
                        else None
                    ),
                    recommendation_id=(
                        request.recommendation_id
                        if request.HasField("recommendation_id")
                        else None
                    ),
                ),
            )
            return _to_proto(dto)


def start_grpc_server(port: int) -> grpc.Server:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4),
        interceptors=(LoggingServerInterceptor(),),
    )
    analytics_pb2_grpc.add_AnalyticsServiceServicer_to_server(
        AnalyticsGrpcService(), server
    )
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    return server
