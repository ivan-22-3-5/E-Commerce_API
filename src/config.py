from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='src/.env', env_file_encoding='utf-8')

    TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALGORITHM: str = "HS256"

    POSTGRESQL_DB_URL: str

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000"
    ]

    SAME_SITE_COOKIE: Literal['strict', 'lax', 'none']


settings = Settings()
