from pydantic import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False
    MODERATION_API_ADDRESS = "http://127.0.0.1:5001"


settings = Settings()

__all__ = [settings]
