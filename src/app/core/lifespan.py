from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.app.cache.cache_provider import RedisProvider
from src.app.core.config import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    redis = RedisProvider(settings.REDIS_DSN)
    application.state.redis = redis

    yield

    await redis.close()
