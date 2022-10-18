"""This module is used to wrap the content moderation API."""

from itertools import chain

import httpx

from blogs_api.core.exceptions import ModerationServiceException
from blogs_api.config import settings


def _split_paragraphs(paragraph: str) -> list[str]:
    """This function is used to split a string into paragraphs.

    Paragraphs are split by the `.` character.

    Args:
        paragraph (str): The string to be split.

    Returns:
        list[str]: The list of sentences.
    """

    return [s.strip() for s in paragraph.split(".") if s]


def _create_sentences(paragraphs: list[str]) -> list[str]:
    """This function is used to split paragraphs into sentences.

    Sentences are split by the `.` character.

    Args:
        paragraphs (list[str]): The list of paragraphs to be split.

    Returns:
        list[str]: The list of sentences.
    """

    return chain.from_iterable(map(_split_paragraphs, paragraphs))


async def has_foul_language(paragraphs: list[str]) -> bool:
    """This function is used to moderate the content of a blog post.

    The paragraphs are split into sentences. Each sentence is then moderated
    and the result of the function is the result of all(sentences...) where
    sentences is a list of booleans returned by the moderation service.

    Args:
        paragraphs (list[str]): The list of paragraphs to be moderated.

    Returns:
        bool: True if the content is foul, False otherwise.
    """

    has_foul_content = await moderate_sentences(_create_sentences(paragraphs))
    return has_foul_content


async def moderate_sentences(sentences: list[str]) -> bool:
    """This function is used to make calls to the moderation service.

    It transforms the response from the API into a boolean value.

    Args:
        sentence (str): The sentence to be moderated.

    Returns:
        bool: True if the sentence is safe, False otherwise.
    """

    try:
        async with httpx.AsyncClient() as client:
            for sentence in sentences:
                response = await client.post(
                    settings.MODERATION_API_ADDRESS, json={"sentence": sentence}
                )

                response.raise_for_status()

                # parse and process the body of the response
                json_response = response.json()
                if json_response["hasFoulLanguage"]:
                    return True

    except httpx.HTTPError as e:
        raise ModerationServiceException(
            "Bad response from the moderation service."
        ) from e
    except KeyError as e:
        raise ModerationServiceException(
            "Badly formatted body from the moderation service."
        ) from e

    return False
