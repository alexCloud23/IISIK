from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self, url: str, ttl_seconds: int) -> None:
        self._url = url
        self._ttl = ttl_seconds
        self._client = None

    def _redis(self):
        if self._client is None:
            if self._url.startswith("fakeredis://"):
                import fakeredis

                self._client = fakeredis.FakeStrictRedis(decode_responses=True)
            else:
                import redis

                self._client = redis.Redis.from_url(self._url, decode_responses=True)
        return self._client

    def get_json(self, key: str) -> dict[str, Any] | None:
        try:
            raw = self._redis().get(key)
        except Exception as exc:
            logger.warning("Кеш недоступен (get %s): %s", key, exc)
            return None
        return json.loads(raw) if raw else None

    def set_json(self, key: str, value: Any) -> None:
        try:
            self._redis().set(
                key, json.dumps(value, ensure_ascii=False), ex=self._ttl
            )
        except Exception as exc:
            logger.warning("Кеш недоступен (set %s): %s", key, exc)

    def delete(self, key: str) -> None:
        try:
            self._redis().delete(key)
        except Exception as exc:
            logger.warning("Кеш недоступен (delete %s): %s", key, exc)
