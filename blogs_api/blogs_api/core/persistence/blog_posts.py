from datetime import datetime
import logging

import boto3
import botocore

from blogs_api.config import settings
from blogs_api.core.exceptions import FailedToSaveBlogPost

LOGGER = logging.getLogger(__name__)


def save_blog_post(title: str, paragraphs: list[str], has_foul_language: bool) -> None:
    """Save a blog post to the database.

    Args:
        title (str): The title of the blog post.
        paragraphs (list[str]): The paragraphs of the blog post.
        has_foul_language (bool): Whether the blog post has fould language or not.

    Raises:
        FailedToSaveBlogPost: If the blog post could not be saved.
    """

    dynamodb = boto3.resource(
        "dynamodb",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.DYNAMODB_ADDRESS,
    )
    table = dynamodb.Table(settings.BLOG_TABLE_NAME)

    try:
        table.put_item(
            Item={
                "title": title,
                "date_created": datetime.now().isoformat(),
                "paragraphs": paragraphs,
                "hasFoulLanguage": has_foul_language,
            },
            ReturnValues="NONE",
        )
    except botocore.exceptions.ClientError as error:
        LOGGER.exception("Failed to save blog post to database.")
        raise FailedToSaveBlogPost from error
