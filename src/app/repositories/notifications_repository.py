from src.app.database.manager import AsyncDatabaseManager


class NotificationsRepository:
    def __init__(self, session: AsyncDatabaseManager):
        self.database: AsyncDatabaseManager = session

    async def is_alive(self):
        return {"status": "Notifications is alive"}

    async def get_notifications(self, user_id: str, page):
        return await self.database.get_notifications(audience=user_id, page=page)
