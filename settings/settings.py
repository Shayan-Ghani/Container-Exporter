# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CONTAINER_EXPORTER_ENV: str = "production"
    CONTAINER_EXPORTER_DEBUG: bool = False
    CONTAINER_EXPORTER_CLEAR_METRICS: bool = True
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()