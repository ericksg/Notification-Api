from fastapi import APIRouter

from src.app.services.notifications_service import NotificationsService

router = APIRouter()


@router.get("/isalive")
async def app_status():
    service: NotificationsService = NotificationsService()
    return await service.is_alive()
