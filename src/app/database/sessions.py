from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.app.core.config import settings
from src.app.models.notifications_model import Base

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_MASTER_URI, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore


async def init_db():
    async with engine.begin() as conn:
        result = await conn.execute(
            text(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='notifications'"
            )
        )

        table_exists = result.first() is not None

        if not table_exists:
            await conn.run_sync(Base.metadata.create_all)
