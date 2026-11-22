from __future__ import annotations

from concurrent import futures

import grpc

import shared.protogen
import identity_pb2
import identity_pb2_grpc
from shared.grpc_errors import grpc_error_boundary
from shared.grpc_logging import LoggingServerInterceptor

from . import auth_service
from .db import SessionLocal


def _payload_to_proto(dto) -> identity_pb2.AuthPayload:
    return identity_pb2.AuthPayload(
        token=dto.token,
        user=identity_pb2.User(
            id=dto.user.id,
            email=dto.user.email,
            full_name=dto.user.full_name,
            is_active=dto.user.is_active,
            created_at=dto.user.created_at.isoformat(),
        ),
        roles=list(dto.roles),
    )


class IdentityGrpcService(identity_pb2_grpc.IdentityServiceServicer):
    def Login(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = auth_service.login(session, request.email, request.password)
            return _payload_to_proto(dto)

    def Register(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = auth_service.register(
                session, request.email, request.password, request.full_name
            )
            return _payload_to_proto(dto)

    def Logout(self, request, context):
        with grpc_error_boundary(context):
            auth_service.logout(request.token)
            from google.protobuf.empty_pb2 import Empty

            return Empty()

    def Introspect(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = auth_service.introspect(session, request.token)
            return identity_pb2.IntrospectResponse(
                user_id=dto.user_id,
                email=dto.email,
                full_name=dto.full_name,
                roles=list(dto.roles),
            )


def start_grpc_server(port: int) -> grpc.Server:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4),
        interceptors=(LoggingServerInterceptor(),),
    )
    identity_pb2_grpc.add_IdentityServiceServicer_to_server(
        IdentityGrpcService(), server
    )
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    return server
