"""This module is used to wrap the content moderation API."""

from itertools import chain

import httpx

from sprout.core.exceptions import APIException
from sprout.config import settings


def _split_paragraphs(paragraph: str) -> list[str]:
    """This function is used to split a string into paragraphs.

    Paragraphs are split by the `.` character.

    Args:
        paragraph (str): The string to be split.

    Returns:
        list[str]: The list of sentences.
    """

    return paragraph.split(".")


def moderate_content(paragraphs: list[str]) -> list[str]:
    """This function is used to moderate the content of a blog post.

    The paragraphs are split into strings using a splitting function to
    form sentences. Each sentence is then moderated and the result of the function is
    the result of all(sentences...) where sentences is a list of booleans
    returned by the moderation service.

    Args:
        paragraphs (list[str]): The list of paragraphs to be moderated.

    Returns:
        list[str]: The list of paragraphs that are safe.
    """

    all_sentences = (_split_paragraphs(p) for p in paragraphs)
    all_sentences = chain.from_iterable(all_sentences)
    moderated_sentences = map(moderate_sentence, all_sentences)
    return all(moderated_sentences)


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
