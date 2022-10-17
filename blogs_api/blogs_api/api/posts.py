from http import HTTPStatus
import logging

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from blogs_api.core.schemas.blog_posts import BlogPost, BlogPostResponse
from blogs_api.core.services.content_moderation_service import has_foul_language
from blogs_api.core.exceptions import APIException, FailedToSaveBlogPost
from blogs_api.core.persistence.blog_posts import save_blog_post

router = APIRouter(prefix="/posts")
LOGGER = logging.getLogger(__name__)


@router.post("/")
def create_billing_rate_endpoint(blog_post: BlogPost):

    try:
        content_has_foul_language = has_foul_language(blog_post.paragraphs)
        save_blog_post(
            title=blog_post.title,
            paragraphs=blog_post.paragraphs,
            has_foul_language=content_has_foul_language,
        )

        return JSONResponse(
            content=BlogPostResponse(
                **blog_post.dict(), has_foul_language=content_has_foul_language
            ),
            status_code=HTTPStatus.CREATED,
        )

    except FailedToSaveBlogPost as e:
        LOGGER.error(e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from e
    except APIException as e:
        LOGGER.exception("Error when calling moderation service.")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Unable to validate your blog post. Please try again later.",
        ) from e
