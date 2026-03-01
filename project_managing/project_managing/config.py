
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DJANGO_SECRET_KEY: str = 'project_managing'
    DEBUG: bool = True
    ALLOWED_HOSTS: list[str] = []

    POSTGRES_DB: str = 'project_managing'
    POSTGRES_USER: str = 'project_managing'
    POSTGRES_PASSWORD: str = 'project_managing'
    POSTGRES_HOST: str = 'db'
    POSTGRES_PORT: int = 5432

    REDIS_PASSWORD: str = 'project_managing'

    FLOWER_USER: str = 'project_managing'
    FLOWER_PASSWORD: str = 'project_managing'

    SMTP_GMAIL_USER: str = ''
    SMTP_GMAIL_PASSWORD: str = ''
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
