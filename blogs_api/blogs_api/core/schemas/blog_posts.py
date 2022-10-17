from pydantic import BaseModel


class BlogPost(BaseModel):
    title: str
    paragraphs: list[str]
