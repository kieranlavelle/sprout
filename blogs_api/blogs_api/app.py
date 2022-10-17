from fastapi import FastAPI

from blogs_api.api import posts

app = FastAPI()
app.include_router(posts.router)
