from __future__ import annotations

import json
import logging
from typing import Any, Protocol

from kafka.errors import KafkaError

from shared.resilience import call_with_retry

NOTIFICATION_TOPIC = "notification.events"

logger = logging.getLogger(__name__)


def _is_retryable(exc: BaseException) -> bool:
    return isinstance(exc, KafkaError)


class EventPublisher(Protocol):
    def publish(self, event: dict[str, Any]) -> None: ...


class KafkaEventPublisher:
    def __init__(self, bootstrap_servers: str) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._producer = None

    def _get_producer(self):
        if self._producer is None:
            from kafka import KafkaProducer

            self._producer = KafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                max_block_ms=5000,
                request_timeout_ms=5000,
                value_serializer=lambda value: json.dumps(
                    value, ensure_ascii=False
                ).encode("utf-8"),
            )
        return self._producer

    def publish(self, event: dict[str, Any]) -> None:
        call_with_retry(
            lambda: self._get_producer().send(NOTIFICATION_TOPIC, event).get(timeout=10),
            label=f"kafka publish {NOTIFICATION_TOPIC}",
            attempts=2,
            backoff=0.5,
            retryable=_is_retryable,
        )
        logger.info(
            "Kafka: событие %s опубликовано в %s",
            event.get("notification_type"),
            NOTIFICATION_TOPIC,
        )

    def close(self) -> None:
        if self._producer is not None:
            self._producer.close()
            self._producer = None
