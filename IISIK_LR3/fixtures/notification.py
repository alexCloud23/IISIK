from __future__ import annotations

from fixtures.ids import FORECAST, NOTIFICATION, RECOMMENDATION, USER, uid
from fixtures.models import Notification, dt

NOTIFICATIONS: list[Notification] = [
    Notification(
        id=uid(NOTIFICATION, 1),
        user_id=uid(USER, 2),
        notification_type="RECOMMENDATION_CREATED",
        title="Новая ценовая рекомендация",
        message=(
            "Сформирована рекомендация по товару «Смартфон X200»: "
            "1249,00 BYN вместо 1299,00 BYN."
        ),
        related_entity_id=uid(RECOMMENDATION, 1),
        status="SENT",
        is_read=False,
        created_at=dt(2026, 10, 13, 9, 5),
        sent_at=dt(2026, 10, 13, 9, 6),
    ),
    Notification(
        id=uid(NOTIFICATION, 2),
        user_id=uid(USER, 2),
        notification_type="DECISION_ACCEPTED",
        title="Ценовое решение принято",
        message=(
            "Рекомендация по товару «Наушники AirSound» принята: "
            "установлена цена 239,00 BYN."
        ),
        related_entity_id=uid(RECOMMENDATION, 3),
        status="SENT",
        is_read=True,
        created_at=dt(2026, 10, 14, 9, 10),
        sent_at=dt(2026, 10, 14, 9, 11),
    ),
    Notification(
        id=uid(NOTIFICATION, 3),
        user_id=uid(USER, 1),
        notification_type="FORECAST_READY",
        title="Прогноз спроса готов",
        message="Сформирован прогноз спроса на период 20.10.2026–26.10.2026.",
        related_entity_id=uid(FORECAST, 5),
        status="PENDING",
        is_read=False,
        created_at=dt(2026, 10, 19, 9),
        sent_at=None,
    ),
]
