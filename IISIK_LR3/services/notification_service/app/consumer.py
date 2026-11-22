from __future__ import annotations

import json
import logging
import threading

from . import service
from .db import SessionLocal
from .schemas import NotificationCreateDTO

TOPIC = "notification.events"

logger = logging.getLogger(__name__)


def _handle_event(event: dict) -> None:
    with SessionLocal() as session:
        service.create_notification(
            session,
            NotificationCreateDTO(
                notification_type=str(event.get("notification_type", "")),
                title=str(event.get("title", "")),
                message=str(event.get("message", "")),
                related_entity_id=event.get("related_entity_id"),
                user_id=event.get("user_id"),
            ),
        )


def _consume_loop(bootstrap_servers: str, stop_event: threading.Event) -> None:
    from kafka import KafkaConsumer

    while not stop_event.is_set():
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=bootstrap_servers,
                group_id="notification-service",
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
            )
        except Exception as exc:
            logger.warning("Kafka недоступна, повтор через 5 с: %s", exc)
            stop_event.wait(5)
            continue
        try:
            while not stop_event.is_set():
                records = consumer.poll(timeout_ms=1000)
                for messages in records.values():
                    for message in messages:
                        try:
                            _handle_event(message.value)
                        except Exception:
                            logger.exception("Ошибка обработки события %s", message.value)
        finally:
            consumer.close()


def start_consumer(
    bootstrap_servers: str, stop_event: threading.Event
) -> threading.Thread:
    thread = threading.Thread(
        target=_consume_loop,
        args=(bootstrap_servers, stop_event),
        name="notification-kafka-consumer",
        daemon=True,
    )
    thread.start()
    return thread
