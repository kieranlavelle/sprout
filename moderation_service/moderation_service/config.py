from pydantic import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False
    CSV_FOUL_WORDS: str


settings = Settings()

__all__ = [settings]
