from fastapi import FastAPI

from sprout.api import posts

app = FastAPI()
app.include_router(posts.router)
