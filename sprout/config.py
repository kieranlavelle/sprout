from pydantic import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False


settings = Settings()

__all__ = [settings]