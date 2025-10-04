from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.cache.cache_provider import RedisProvider
from src.core.config import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Shutdown event handler."""
    yield
    provider = RedisProvider(settings.REDIS_DSN)
    await provider.close()
