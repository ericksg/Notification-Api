from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator, RedisDsn, Field, AliasChoices
from typing import List, Union
import os

class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.getenv("BACKEND_CORS_ORIGINS", [])

    # Global config
    PROJECT_NAME: str = "Brand Notification API"

    # ALLOWED_HOST
    ALLOWED_HOSTS: Union[str, List[str]] = os.getenv("ALLOWED_HOSTS", ["127.0.0.1", "localhost"])

    # Redis
    REDIS_DSN: RedisDsn = Field(
        os.getenv("REDIS_DSN", "redis://172.17.0.3:6379"),
        validation_alias=AliasChoices('service_redis_dsn', 'redis_url'),

    )

    # Redis channel
    NOTIFICATION_CHANNEL: str = "brand-notification"

    # Validators
    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()