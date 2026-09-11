import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database.sessions import AsyncSessionLocal
from src.app.models.notifications_model import Notification


class AsyncDatabaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_notifications(self, audience: str, page: int = 1, per_page: int = 10):
        offset = (page - 1) * per_page
        query = (
            select(Notification)
            .where(Notification.audience == audience)
            .offset(offset)
            .limit(per_page)
        )
        result = await self.session.execute(query)
        total_count = await self.get_total_count(audience)
        unread_count = await self.get_unread_count(audience)
        next_page = page + 1 if (total_count / per_page) > page else None
        return {
            "notifications": result.scalars().all(),
            "next_page": next_page,
            "unread_count": unread_count,
        }

    async def get_total_count(self, audience: str):
        query = (
            select(Notification)
            .where(Notification.audience == audience)
            .with_only_columns([Notification.id])  # type: ignore
            .distinct()
        )  # type: ignore
        result = await self.session.execute(query)
        return len(result.all())

    async def get_unread_count(self, audience: str):
        query = (
            select(func.count())
            .where(Notification.audience == audience)
            .where(Notification.unread == True)
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def add_notification(self, notification: Notification):
        self.session.add(notification)
        await self.session.commit()
        return notification

    async def delete_notification(self, notification_id: int):
        query = select(Notification).where(Notification.id == notification_id)
        result = await self.session.execute(query)
        notification = result.scalar_one()
        if notification:
            await self.session.delete(notification)
            await self.session.commit()
        return notification

    async def purge_notifications(self, audience: str):
        thirty_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=30)
        query = (
            select(Notification)
            .where(Notification.audience == audience)
            .where(Notification.created_at < thirty_days_ago)
        )
        result = await self.session.execute(query)
        notifications_to_purge = result.scalars().all()
        for notification in notifications_to_purge:
            await self.session.delete(notification)
        await self.session.commit()
        return len(notifications_to_purge)


# Función para obtener una instancia de AsyncDatabaseManager
async def get_db():
    async with AsyncSessionLocal() as session:  # type: ignore
        yield AsyncDatabaseManager(session)
