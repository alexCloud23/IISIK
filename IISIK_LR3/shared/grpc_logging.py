from __future__ import annotations

import logging
import time

import grpc

logger = logging.getLogger(__name__)


class LoggingServerInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        handler = continuation(handler_call_details)
        if handler is None or handler.unary_unary is None:
            return handler
        method = handler_call_details.method
        inner = handler.unary_unary

        def behavior(request, context):
            started = time.perf_counter()
            try:
                response = inner(request, context)
            except Exception as exc:
                logger.warning(
                    "gRPC %s: ошибка %s за %.0f мс",
                    method,
                    exc.__class__.__name__,
                    (time.perf_counter() - started) * 1000,
                )
                raise
            logger.info(
                "gRPC %s: OK за %.0f мс",
                method,
                (time.perf_counter() - started) * 1000,
            )
            return response

        return grpc.unary_unary_rpc_method_handler(
            behavior,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )
