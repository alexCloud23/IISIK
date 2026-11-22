"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import pricing_pb2 as pricing__pb2

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
        + ' but the generated code in pricing_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class PricingServiceStub:
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListRecommendations = channel.unary_unary(
                '/pricing.PricingService/ListRecommendations',
                request_serializer=pricing__pb2.ListRecommendationsRequest.SerializeToString,
                response_deserializer=pricing__pb2.ListRecommendationsResponse.FromString,
                _registered_method=True)
        self.GetRecommendation = channel.unary_unary(
                '/pricing.PricingService/GetRecommendation',
                request_serializer=pricing__pb2.GetRecommendationRequest.SerializeToString,
                response_deserializer=pricing__pb2.GetRecommendationResponse.FromString,
                _registered_method=True)
        self.CreateRecommendation = channel.unary_unary(
                '/pricing.PricingService/CreateRecommendation',
                request_serializer=pricing__pb2.CreateRecommendationRequest.SerializeToString,
                response_deserializer=pricing__pb2.Recommendation.FromString,
                _registered_method=True)
        self.DecideRecommendation = channel.unary_unary(
                '/pricing.PricingService/DecideRecommendation',
                request_serializer=pricing__pb2.DecideRecommendationRequest.SerializeToString,
                response_deserializer=pricing__pb2.Recommendation.FromString,
                _registered_method=True)
        self.RecommendationsSummary = channel.unary_unary(
                '/pricing.PricingService/RecommendationsSummary',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=pricing__pb2.RecommendationsSummaryResponse.FromString,
                _registered_method=True)


class PricingServiceServicer:
    """Missing associated documentation comment in .proto file."""

    def ListRecommendations(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRecommendation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateRecommendation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DecideRecommendation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RecommendationsSummary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PricingServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListRecommendations': grpc.unary_unary_rpc_method_handler(
                    servicer.ListRecommendations,
                    request_deserializer=pricing__pb2.ListRecommendationsRequest.FromString,
                    response_serializer=pricing__pb2.ListRecommendationsResponse.SerializeToString,
            ),
            'GetRecommendation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRecommendation,
                    request_deserializer=pricing__pb2.GetRecommendationRequest.FromString,
                    response_serializer=pricing__pb2.GetRecommendationResponse.SerializeToString,
            ),
            'CreateRecommendation': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateRecommendation,
                    request_deserializer=pricing__pb2.CreateRecommendationRequest.FromString,
                    response_serializer=pricing__pb2.Recommendation.SerializeToString,
            ),
            'DecideRecommendation': grpc.unary_unary_rpc_method_handler(
                    servicer.DecideRecommendation,
                    request_deserializer=pricing__pb2.DecideRecommendationRequest.FromString,
                    response_serializer=pricing__pb2.Recommendation.SerializeToString,
            ),
            'RecommendationsSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.RecommendationsSummary,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=pricing__pb2.RecommendationsSummaryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'pricing.PricingService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('pricing.PricingService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class PricingService:
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListRecommendations(request,
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
            '/pricing.PricingService/ListRecommendations',
            pricing__pb2.ListRecommendationsRequest.SerializeToString,
            pricing__pb2.ListRecommendationsResponse.FromString,
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
    def GetRecommendation(request,
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
            '/pricing.PricingService/GetRecommendation',
            pricing__pb2.GetRecommendationRequest.SerializeToString,
            pricing__pb2.GetRecommendationResponse.FromString,
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
    def CreateRecommendation(request,
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
            '/pricing.PricingService/CreateRecommendation',
            pricing__pb2.CreateRecommendationRequest.SerializeToString,
            pricing__pb2.Recommendation.FromString,
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
    def DecideRecommendation(request,
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
            '/pricing.PricingService/DecideRecommendation',
            pricing__pb2.DecideRecommendationRequest.SerializeToString,
            pricing__pb2.Recommendation.FromString,
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
    def RecommendationsSummary(request,
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
            '/pricing.PricingService/RecommendationsSummary',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            pricing__pb2.RecommendationsSummaryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
