from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False
    MODERATION_API_ADDRESS = "http://127.0.0.1:5001"
    BLOG_TABLE_NAME = "blog"
    AWS_REGION: str = "eu-west-1"
    DYNAMODB_ADDRESS: Optional[str] = None


settings = Settings()

__all__ = [settings]
