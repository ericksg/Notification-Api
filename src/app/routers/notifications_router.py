from fastapi import APIRouter, Depends
from src.app.core.config import settings
from starlette.websockets import WebSocket
from src.app.services.notifications_service import NotificationsService

router = APIRouter()


@router.get("/isalive")
async def app_status(service: NotificationsService = Depends()):
    return await service.is_alive()

@router.websocket("/ws", "ws")
async def app_websocket(websocket: WebSocket, service: NotificationsService = Depends()):
    await service.ws_root(websocket, settings.NOTIFICATION_CHANNEL)