from fastapi import FastAPI
from src.app.core.config import settings
from src.app.core.lifespan import lifespan
from src.app.routers import notifications_router


def create_app() -> FastAPI:
    notifications_app = FastAPI(title=settings.PROJECT_NAME,
                  version="1.0.0",
                  lifespan=lifespan)

    notifications_app.include_router(notifications_router.router, prefix="/notifications", tags=["Notifications"])
    return notifications_app

app = create_app()
