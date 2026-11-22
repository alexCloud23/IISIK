"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import strategy_pb2 as strategy__pb2

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
        + ' but the generated code in strategy_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class StrategyServiceStub:
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListStrategies = channel.unary_unary(
                '/strategy.StrategyService/ListStrategies',
                request_serializer=strategy__pb2.ListStrategiesRequest.SerializeToString,
                response_deserializer=strategy__pb2.ListStrategiesResponse.FromString,
                _registered_method=True)
        self.AnalyzeStrategy = channel.unary_unary(
                '/strategy.StrategyService/AnalyzeStrategy',
                request_serializer=strategy__pb2.AnalyzeStrategyRequest.SerializeToString,
                response_deserializer=strategy__pb2.Strategy.FromString,
                _registered_method=True)


class StrategyServiceServicer:
    """Missing associated documentation comment in .proto file."""

    def ListStrategies(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AnalyzeStrategy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StrategyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListStrategies': grpc.unary_unary_rpc_method_handler(
                    servicer.ListStrategies,
                    request_deserializer=strategy__pb2.ListStrategiesRequest.FromString,
                    response_serializer=strategy__pb2.ListStrategiesResponse.SerializeToString,
            ),
            'AnalyzeStrategy': grpc.unary_unary_rpc_method_handler(
                    servicer.AnalyzeStrategy,
                    request_deserializer=strategy__pb2.AnalyzeStrategyRequest.FromString,
                    response_serializer=strategy__pb2.Strategy.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'strategy.StrategyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('strategy.StrategyService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class StrategyService:
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListStrategies(request,
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
            '/strategy.StrategyService/ListStrategies',
            strategy__pb2.ListStrategiesRequest.SerializeToString,
            strategy__pb2.ListStrategiesResponse.FromString,
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
    def AnalyzeStrategy(request,
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
            '/strategy.StrategyService/AnalyzeStrategy',
            strategy__pb2.AnalyzeStrategyRequest.SerializeToString,
            strategy__pb2.Strategy.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
