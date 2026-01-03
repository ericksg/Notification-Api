from fastapi import Depends
from src.app.repositories.notifications_repository import NotificationsRepository

class NotificationsService:
    def __init__(self, repo: NotificationsRepository = Depends()):
        self.repo = repo

    async def is_alive(self):
        return await self.repo.is_alive()

    async def ws_root(self, websocket, channel):
        await self.repo.socket_notifications(websocket, channel)