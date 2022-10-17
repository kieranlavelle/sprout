from pydantic import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False
    CSV_FOUL_WORDS: str = "java,php,crap,foul"


settings = Settings()

__all__ = [settings]
