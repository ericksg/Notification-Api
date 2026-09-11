from src.app.repositories.notifications_repository import NotificationsRepository


class NotificationsService:
    def __init__(self, session=None):
        self.repo = NotificationsRepository(session)

    async def is_alive(self):
        return await self.repo.is_alive()

    async def get_notifications(self, user_id: str, page):
        return await self.repo.get_notifications(user_id, page=page)
