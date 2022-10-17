import logging

from fastapi import APIRouter, Response, HTTPException

from sprout.core.schemas.blog_posts import BlogPost
from sprout.core.services.content_moderation_service import moderate_content
from sprout.core.exceptions import APIException

router = APIRouter(prefix="/posts")
LOGGER = logging.getLogger(__name__)


@router.post("/")
def create_billing_rate_endpoint(blog_post: BlogPost, response: Response):

    try:
        content_is_safe = moderate_content(blog_post.paragraphs)
        if content_is_safe:
            # persist to the database
            pass
        else:
            raise HTTPException(
                status_code=400,
                detail="Content is not safe",
            )
    except APIException as e:
        LOGGER.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
