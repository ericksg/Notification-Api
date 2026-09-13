from fastapi import APIRouter, Depends

from src.app.database.manager import AsyncDatabaseManager, get_db
from src.app.services.notifications_service import NotificationsService

router = APIRouter()


@router.get("/isalive")
async def app_status():
    service: NotificationsService = NotificationsService()
    return await service.is_alive()


@router.get("/get_notifications")
async def get_notifications(
    user_id: str, page: int = 1, session: AsyncDatabaseManager | None = Depends(get_db)
):
    service: NotificationsService = NotificationsService(session)
    return await service.get_notifications(user_id=user_id, page=page)


@router.get("/mark_notification")
async def mark_notification(
    notification_id: int,
    unread: bool,
    session: AsyncDatabaseManager | None = Depends(get_db),
):
    service: NotificationsService = NotificationsService(session)
    return await service.mark_notifications(notification_id, unread)


@router.get("/delete_notification")
async def delete_notification(
    notification_id: int, session: AsyncDatabaseManager | None = Depends(get_db)
):
    service: NotificationsService = NotificationsService(session)
    return await service.delete_notifications(notification_id)
