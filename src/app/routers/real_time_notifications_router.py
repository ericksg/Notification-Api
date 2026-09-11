from fastapi import APIRouter
from starlette.websockets import WebSocket

from src.app.core.config import settings
from src.app.services.real_time_notifications_service import (
    RealTimeNotificationsService,
)

router = APIRouter()


@router.websocket("/ws", "ws")
async def app_websocket(websocket: WebSocket):
    service: RealTimeNotificationsService = RealTimeNotificationsService()
    await service.ws_root(websocket, settings.NOTIFICATION_CHANNEL)
