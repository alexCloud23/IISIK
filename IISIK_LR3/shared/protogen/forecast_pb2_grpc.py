"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import forecast_pb2 as forecast__pb2

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
        + ' but the generated code in forecast_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ForecastServiceStub:
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListForecasts = channel.unary_unary(
                '/forecast.ForecastService/ListForecasts',
                request_serializer=forecast__pb2.ListForecastsRequest.SerializeToString,
                response_deserializer=forecast__pb2.ListForecastsResponse.FromString,
                _registered_method=True)
        self.GetForecast = channel.unary_unary(
                '/forecast.ForecastService/GetForecast',
                request_serializer=forecast__pb2.GetForecastRequest.SerializeToString,
                response_deserializer=forecast__pb2.GetForecastResponse.FromString,
                _registered_method=True)
        self.GenerateForecast = channel.unary_unary(
                '/forecast.ForecastService/GenerateForecast',
                request_serializer=forecast__pb2.GenerateForecastRequest.SerializeToString,
                response_deserializer=forecast__pb2.Forecast.FromString,
                _registered_method=True)


class ForecastServiceServicer:
    """Missing associated documentation comment in .proto file."""

    def ListForecasts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetForecast(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GenerateForecast(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ForecastServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListForecasts': grpc.unary_unary_rpc_method_handler(
                    servicer.ListForecasts,
                    request_deserializer=forecast__pb2.ListForecastsRequest.FromString,
                    response_serializer=forecast__pb2.ListForecastsResponse.SerializeToString,
            ),
            'GetForecast': grpc.unary_unary_rpc_method_handler(
                    servicer.GetForecast,
                    request_deserializer=forecast__pb2.GetForecastRequest.FromString,
                    response_serializer=forecast__pb2.GetForecastResponse.SerializeToString,
            ),
            'GenerateForecast': grpc.unary_unary_rpc_method_handler(
                    servicer.GenerateForecast,
                    request_deserializer=forecast__pb2.GenerateForecastRequest.FromString,
                    response_serializer=forecast__pb2.Forecast.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'forecast.ForecastService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('forecast.ForecastService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ForecastService:
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListForecasts(request,
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
            '/forecast.ForecastService/ListForecasts',
            forecast__pb2.ListForecastsRequest.SerializeToString,
            forecast__pb2.ListForecastsResponse.FromString,
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
    def GetForecast(request,
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
            '/forecast.ForecastService/GetForecast',
            forecast__pb2.GetForecastRequest.SerializeToString,
            forecast__pb2.GetForecastResponse.FromString,
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
    def GenerateForecast(request,
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
            '/forecast.ForecastService/GenerateForecast',
            forecast__pb2.GenerateForecastRequest.SerializeToString,
            forecast__pb2.Forecast.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
