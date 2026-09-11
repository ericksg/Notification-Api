import os

from pydantic import (
    AliasChoices,
    AnyHttpUrl,
    Field,
    RedisDsn,
    field_validator,
)
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = os.getenv("BACKEND_CORS_ORIGINS", [])

    # Global config
    PROJECT_NAME: str = "Brand Notification API"

    # ALLOWED_HOST
    ALLOWED_HOSTS: str | list[str] = os.getenv(
        "ALLOWED_HOSTS", ["127.0.0.1", "localhost", "100.70.210.123"]
    )

    # Redis
    REDIS_DSN: RedisDsn = Field(
        os.getenv("REDIS_DSN", "redis://localhost:6379"),
        validation_alias=AliasChoices("service_redis_dsn", "redis_url"),
    )

    # Redis channel
    NOTIFICATION_CHANNEL: str = "brand-notification"

    # Database config
    SQLALCHEMY_DATABASE_MASTER_URI: str = "sqlite+aiosqlite:///./notifications.db"

    # Validators
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
