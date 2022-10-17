from pydantic import BaseModel


class BlogPost(BaseModel):
    title: str
    paragraphs: list[str]


class BlogPostResponse(BlogPost):
    has_foul_language: bool
