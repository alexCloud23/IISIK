from __future__ import annotations

from concurrent import futures
from decimal import Decimal

import grpc

import shared.protogen
import pricing_pb2
import pricing_pb2_grpc
from shared.grpc_errors import grpc_error_boundary

from . import service
from .db import SessionLocal
from .schemas import RecommendationCreateDTO


def _to_proto(dto) -> pricing_pb2.Recommendation:
    return pricing_pb2.Recommendation(
        id=dto.id,
        product_id=dto.product_id,
        forecast_id=dto.forecast_id,
        strategy_id=dto.strategy_id,
        current_price=str(dto.current_price),
        recommended_price=str(dto.recommended_price),
        currency=dto.currency,
        reason=dto.reason,
        status=dto.status,
        created_at=dto.created_at.isoformat(),
    )


class PricingGrpcService(pricing_pb2_grpc.PricingServiceServicer):
    def ListRecommendations(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            items = service.list_recommendations(
                session,
                request.product_id if request.HasField("product_id") else None,
                request.status if request.HasField("status") else None,
                request.sort or "created",
                request.order or "desc",
            )
            return pricing_pb2.ListRecommendationsResponse(
                recommendations=[_to_proto(item) for item in items]
            )

    def GetRecommendation(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.get_recommendation(session, request.id)
            return pricing_pb2.GetRecommendationResponse(
                recommendation=_to_proto(dto)
            )

    def CreateRecommendation(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.create_recommendation(
                session,
                RecommendationCreateDTO(
                    product_id=request.product_id,
                    forecast_id=request.forecast_id,
                    current_price=Decimal(request.current_price),
                    strategy_type=(
                        request.strategy_type
                        if request.HasField("strategy_type")
                        else None
                    ),
                    competitor_price=(
                        Decimal(request.competitor_price)
                        if request.HasField("competitor_price")
                        else None
                    ),
                    strategy_id=(
                        request.strategy_id
                        if request.HasField("strategy_id")
                        else None
                    ),
                ),
            )
            return _to_proto(dto)

    def DecideRecommendation(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.decide_recommendation(session, request.id, request.decision)
            return _to_proto(dto)

    def RecommendationsSummary(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            summary = service.recommendations_summary(session)
            return pricing_pb2.RecommendationsSummaryResponse(
                total=summary.get("total", 0),
                new=summary.get("new", 0),
                accepted=summary.get("accepted", 0),
                rejected=summary.get("rejected", 0),
            )


def start_grpc_server(port: int) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pricing_pb2_grpc.add_PricingServiceServicer_to_server(
        PricingGrpcService(), server
    )
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    return server
