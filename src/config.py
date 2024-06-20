from pathlib import Path
from typing import Literal

from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='src/.env', env_file_encoding='utf-8')

    TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    RECOVERY_TOKEN_EXPIRE_MINUTES: int
    CONFIRMATION_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str = "HS256"

    PASSWORD_RECOVERY_LINK: str
    EMAIL_CONFIRMATION_LINK: str

    POSTGRESQL_DB_URL: str

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000"
    ]

    SAME_SITE_COOKIE: Literal['strict', 'lax', 'none']

    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_PORT: int
    SMTP_MAIL: str
    SMTP_SERVER: str


settings = Settings()

smtp_config = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USERNAME,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_MAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_SERVER,
    TEMPLATE_FOLDER=Path(__file__).parent / "html_templates",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
