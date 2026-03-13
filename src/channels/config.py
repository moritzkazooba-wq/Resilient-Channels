from pydantic_settings import BaseSettings

import structlog


class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379"
    KAFKA_BOOTSTRAP: str = "localhost:9092"
    AT_USERNAME: str = "sandbox"
    AT_API_KEY: str = "test"
    WHATSAPP_TOKEN: str = "test"
    WHATSAPP_PHONE_ID: str = "test"
    WHATSAPP_VERIFY_TOKEN: str = "test"
    PHONE_HASH_SALT: str = "dev-salt-change-in-prod"
    ENV: str = "development"


structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)
