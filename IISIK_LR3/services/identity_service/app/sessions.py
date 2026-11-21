from __future__ import annotations

from .config import settings

_client = None


def _redis():
    global _client
    if _client is None:
        if settings.redis_url.startswith("fakeredis://"):
            import fakeredis

            _client = fakeredis.FakeStrictRedis(decode_responses=True)
        else:
            import redis

            _client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    return _client


def _key(jti: str) -> str:
    return f"session:{jti}"


def create_session(jti: str, user_id: str, ttl_seconds: int) -> None:
    _redis().set(_key(jti), user_id, ex=ttl_seconds)


def session_exists(jti: str) -> bool:
    return bool(_redis().exists(_key(jti)))


def delete_session(jti: str) -> None:
    _redis().delete(_key(jti))
