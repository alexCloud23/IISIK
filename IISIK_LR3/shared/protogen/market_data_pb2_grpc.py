"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import market_data_pb2 as market__data__pb2

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
        + ' but the generated code in market_data_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class MarketDataServiceStub:
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SalesSummary = channel.unary_unary(
                '/marketdata.MarketDataService/SalesSummary',
                request_serializer=market__data__pb2.SalesSummaryRequest.SerializeToString,
                response_deserializer=market__data__pb2.SalesSummaryResponse.FromString,
                _registered_method=True)
        self.ListSales = channel.unary_unary(
                '/marketdata.MarketDataService/ListSales',
                request_serializer=market__data__pb2.ListSalesRequest.SerializeToString,
                response_deserializer=market__data__pb2.ListSalesResponse.FromString,
                _registered_method=True)
        self.ListCompetitorPrices = channel.unary_unary(
                '/marketdata.MarketDataService/ListCompetitorPrices',
                request_serializer=market__data__pb2.ListCompetitorPricesRequest.SerializeToString,
                response_deserializer=market__data__pb2.ListCompetitorPricesResponse.FromString,
                _registered_method=True)


class MarketDataServiceServicer:
    """Missing associated documentation comment in .proto file."""

    def SalesSummary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListSales(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCompetitorPrices(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MarketDataServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SalesSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.SalesSummary,
                    request_deserializer=market__data__pb2.SalesSummaryRequest.FromString,
                    response_serializer=market__data__pb2.SalesSummaryResponse.SerializeToString,
            ),
            'ListSales': grpc.unary_unary_rpc_method_handler(
                    servicer.ListSales,
                    request_deserializer=market__data__pb2.ListSalesRequest.FromString,
                    response_serializer=market__data__pb2.ListSalesResponse.SerializeToString,
            ),
            'ListCompetitorPrices': grpc.unary_unary_rpc_method_handler(
                    servicer.ListCompetitorPrices,
                    request_deserializer=market__data__pb2.ListCompetitorPricesRequest.FromString,
                    response_serializer=market__data__pb2.ListCompetitorPricesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'marketdata.MarketDataService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('marketdata.MarketDataService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class MarketDataService:
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SalesSummary(request,
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
            '/marketdata.MarketDataService/SalesSummary',
            market__data__pb2.SalesSummaryRequest.SerializeToString,
            market__data__pb2.SalesSummaryResponse.FromString,
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
    def ListSales(request,
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
            '/marketdata.MarketDataService/ListSales',
            market__data__pb2.ListSalesRequest.SerializeToString,
            market__data__pb2.ListSalesResponse.FromString,
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
    def ListCompetitorPrices(request,
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
            '/marketdata.MarketDataService/ListCompetitorPrices',
            market__data__pb2.ListCompetitorPricesRequest.SerializeToString,
            market__data__pb2.ListCompetitorPricesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
