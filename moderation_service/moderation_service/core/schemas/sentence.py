from pydantic import BaseModel


class Sentence(BaseModel):
    fragment: str
