import redis

from app.config import (
    REDIS_URL,
)


# =========================================================
# Redis Client
# =========================================================

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


# =========================================================
# Redis 연결 확인
# =========================================================

def check_redis_connection() -> bool:

    return redis_client.ping()