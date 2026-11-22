"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import notification_pb2 as notification__pb2

GRPC_GENERATED_VERSION = '1.85.3'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + ' but the generated code in notification_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class NotificationServiceStub:
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListNotifications = channel.unary_unary(
                '/notification.NotificationService/ListNotifications',
                request_serializer=notification__pb2.ListNotificationsRequest.SerializeToString,
                response_deserializer=notification__pb2.ListNotificationsResponse.FromString,
                _registered_method=True)
        self.GetUnreadCount = channel.unary_unary(
                '/notification.NotificationService/GetUnreadCount',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=notification__pb2.UnreadCountResponse.FromString,
                _registered_method=True)
        self.CreateNotification = channel.unary_unary(
                '/notification.NotificationService/CreateNotification',
                request_serializer=notification__pb2.CreateNotificationRequest.SerializeToString,
                response_deserializer=notification__pb2.Notification.FromString,
                _registered_method=True)
        self.MarkNotificationRead = channel.unary_unary(
                '/notification.NotificationService/MarkNotificationRead',
                request_serializer=notification__pb2.MarkNotificationReadRequest.SerializeToString,
                response_deserializer=notification__pb2.Notification.FromString,
                _registered_method=True)
        self.MarkAllNotificationsRead = channel.unary_unary(
                '/notification.NotificationService/MarkAllNotificationsRead',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=notification__pb2.MarkAllReadResponse.FromString,
                _registered_method=True)


class NotificationServiceServicer:
    """Missing associated documentation comment in .proto file."""

    def ListNotifications(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUnreadCount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateNotification(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MarkNotificationRead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MarkAllNotificationsRead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NotificationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListNotifications': grpc.unary_unary_rpc_method_handler(
                    servicer.ListNotifications,
                    request_deserializer=notification__pb2.ListNotificationsRequest.FromString,
                    response_serializer=notification__pb2.ListNotificationsResponse.SerializeToString,
            ),
            'GetUnreadCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUnreadCount,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=notification__pb2.UnreadCountResponse.SerializeToString,
            ),
            'CreateNotification': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateNotification,
                    request_deserializer=notification__pb2.CreateNotificationRequest.FromString,
                    response_serializer=notification__pb2.Notification.SerializeToString,
            ),
            'MarkNotificationRead': grpc.unary_unary_rpc_method_handler(
                    servicer.MarkNotificationRead,
                    request_deserializer=notification__pb2.MarkNotificationReadRequest.FromString,
                    response_serializer=notification__pb2.Notification.SerializeToString,
            ),
            'MarkAllNotificationsRead': grpc.unary_unary_rpc_method_handler(
                    servicer.MarkAllNotificationsRead,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=notification__pb2.MarkAllReadResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'notification.NotificationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('notification.NotificationService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class NotificationService:
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListNotifications(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/notification.NotificationService/ListNotifications',
            notification__pb2.ListNotificationsRequest.SerializeToString,
            notification__pb2.ListNotificationsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetUnreadCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/notification.NotificationService/GetUnreadCount',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            notification__pb2.UnreadCountResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CreateNotification(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/notification.NotificationService/CreateNotification',
            notification__pb2.CreateNotificationRequest.SerializeToString,
            notification__pb2.Notification.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def MarkNotificationRead(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/notification.NotificationService/MarkNotificationRead',
            notification__pb2.MarkNotificationReadRequest.SerializeToString,
            notification__pb2.Notification.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def MarkAllNotificationsRead(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/notification.NotificationService/MarkAllNotificationsRead',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            notification__pb2.MarkAllReadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
