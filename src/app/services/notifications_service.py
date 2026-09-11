from src.app.repositories.notifications_repository import NotificationsRepository


class NotificationsService:
    def __init__(self):
        self.repo = NotificationsRepository()

    async def is_alive(self):
        return await self.repo.is_alive()
