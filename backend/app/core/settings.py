from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Learning Assistant API"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/learning_assistant"
    redis_url: str = "redis://redis:6379/0"
    clerk_secret_key: str = ""
    clerk_issuer: str = ""
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000


@lru_cache

def get_settings() -> Settings:
    return Settings()
