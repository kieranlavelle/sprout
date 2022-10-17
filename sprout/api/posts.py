from fastapi import APIRouter, Response

from sprout.core.schemas.blog_posts import BlogPost
from sprout.core.services.content_moderation_service import moderate_sentence

router = APIRouter(prefix="/posts")


@router.post("/")
def create_billing_rate_endpoint(blog_post: BlogPost, response: Response):
    pass
