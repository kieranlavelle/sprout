"""This module is used to wrap the content moderation API."""

from itertools import chain

import httpx

from blogs_api.core.exceptions import APIException
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


def has_foul_language(paragraphs: list[str]) -> bool:
    """This function is used to moderate the content of a blog post.

    The paragraphs are split into sentences. Each sentence is then moderated
    and the result of the function is the result of all(sentences...) where
    sentences is a list of booleans returned by the moderation service.

    Args:
        paragraphs (list[str]): The list of paragraphs to be moderated.

    Returns:
        bool: True if the content is foul, False otherwise.
    """

    moderated_sentences = map(moderate_sentence, _create_sentences(paragraphs))
    return any(moderated_sentences)


def moderate_sentence(sentence: str) -> bool:
    """This function is used to make calls to the moderation service.

    It transforms the response from the API into a boolean value.

    Args:
        sentence (str): The sentence to be moderated.

    Returns:
        bool: True if the sentence is safe, False otherwise.
    """

    response = httpx.post(
        f"{settings.MODERATION_API_ADDRESS}/sentences",
        json={"fragment": sentence},
    )

    try:
        if response.status_code == 200:
            json_response = response.json()
            return json_response["hasFoulLanguage"]
        else:
            raise APIException(
                f"Non 200 response from moderation service. Status Code: {response.status_code}"
            )
    except KeyError as e:
        raise ValueError("The moderation service returned an invalid response.") from e
