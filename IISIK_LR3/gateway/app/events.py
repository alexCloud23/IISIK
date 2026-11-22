from __future__ import annotations

import json
from typing import Any, Protocol

NOTIFICATION_TOPIC = "notification.events"


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
                value_serializer=lambda value: json.dumps(
                    value, ensure_ascii=False
                ).encode("utf-8"),
            )
        return self._producer

    def publish(self, event: dict[str, Any]) -> None:
        self._get_producer().send(NOTIFICATION_TOPIC, event).get(timeout=10)

    def close(self) -> None:
        if self._producer is not None:
            self._producer.close()
            self._producer = None
