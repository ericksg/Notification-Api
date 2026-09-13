from src.app.database.manager import AsyncDatabaseManager


class NotificationsRepository:
    def __init__(self, session: AsyncDatabaseManager | None):
        self.database: AsyncDatabaseManager = session

    async def is_alive(self):
        return {"status": "Notifications is alive"}

    async def get_notifications(self, user_id: str, page):
        return await self.database.get_notifications(audience=user_id, page=page)

    async def mark_notifications(self, notification_id: int, unread: bool):
        return await self.database.mark_notification(notification_id, unread)

    async def delete_notifications(self, notification_id: int):
        return await self.database.delete_notification(notification_id)
