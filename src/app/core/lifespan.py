from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.cache.cache_provider import RedisProvider
from src.app.core.config import settings
from src.app.database import sessions


@asynccontextmanager
async def lifespan(application: FastAPI):
    redis = RedisProvider(settings.REDIS_DSN)
    application.state.redis = redis

    await sessions.init_db()

    yield

    await redis.close()
