from typing import AsyncGenerator

import redis.asyncio as aioredis
from loguru import logger

from core.config import settings

_redis: aioredis.Redis | None = None

async def init_redis() -> None:
    global _redis
    if _redis is not None:
        return
    _redis = aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True, max_connections=10)

    await _redis.ping()

    logger.info("Redis Connected-{}",settings.redis_url)

def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None
        logger.info("Redis Connection Closed")
    
def get_redis() -> aioredis.Redis:
    """ return single redis client """
    if _redis is None:
        raise RuntimeError("Redis client not initialized. Call init_redis() first.")
    return _redis

async def redis_dependency() -> AsyncGenerator[aioredis.Redis, None]:
    """ Dependency for FastAPI routes to get a Redis client """
    if _redis is None:
        raise RuntimeError("Redis client not initialized. Call init_redis() first.")
    yield get_redis()