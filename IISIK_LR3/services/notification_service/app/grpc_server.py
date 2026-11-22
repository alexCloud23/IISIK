from __future__ import annotations

from concurrent import futures

import grpc

import shared.protogen
import notification_pb2
import notification_pb2_grpc
from shared.grpc_errors import grpc_error_boundary
from shared.grpc_logging import LoggingServerInterceptor

from . import service
from .db import SessionLocal
from .schemas import NotificationCreateDTO


def _to_proto(dto) -> notification_pb2.Notification:
    return notification_pb2.Notification(
        id=dto.id,
        user_id=dto.user_id,
        notification_type=dto.notification_type,
        title=dto.title,
        message=dto.message,
        related_entity_id=dto.related_entity_id,
        status=dto.status,
        is_read=dto.is_read,
        created_at=dto.created_at.isoformat(),
        sent_at=dto.sent_at.isoformat() if dto.sent_at else None,
    )


class NotificationGrpcService(notification_pb2_grpc.NotificationServiceServicer):
    def ListNotifications(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            items = service.list_notifications(
                session,
                request.is_read if request.HasField("is_read") else None,
                (
                    request.notification_type
                    if request.HasField("notification_type")
                    else None
                ),
            )
            return notification_pb2.ListNotificationsResponse(
                notifications=[_to_proto(item) for item in items]
            )

    def GetUnreadCount(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            return notification_pb2.UnreadCountResponse(
                unread=service.get_unread_count(session)
            )

    def CreateNotification(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.create_notification(
                session,
                NotificationCreateDTO(
                    notification_type=request.notification_type,
                    title=request.title,
                    message=request.message,
                    related_entity_id=(
                        request.related_entity_id
                        if request.HasField("related_entity_id")
                        else None
                    ),
                    user_id=(
                        request.user_id if request.HasField("user_id") else None
                    ),
                ),
            )
            return _to_proto(dto)

    def MarkNotificationRead(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            dto = service.mark_notification_read(session, request.id)
            return _to_proto(dto)

    def MarkAllNotificationsRead(self, request, context):
        with grpc_error_boundary(context), SessionLocal() as session:
            return notification_pb2.MarkAllReadResponse(
                updated=service.mark_all_notifications_read(session)
            )


def start_grpc_server(port: int) -> grpc.Server:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4),
        interceptors=(LoggingServerInterceptor(),),
    )
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(
        NotificationGrpcService(), server
    )
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    return server
