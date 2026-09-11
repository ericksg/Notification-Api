from src.app.repositories.real_time_notifications_repository import (
    RealTimeNotificationsRepository,
)


class RealTimeNotificationsService:
    def __init__(self):
        self.repo = RealTimeNotificationsRepository()

    async def ws_root(self, websocket, channel):
        await self.repo.socket_notifications(websocket, channel)
