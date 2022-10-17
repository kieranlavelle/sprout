from functools import lru_cache

from moderation_service.config import settings

import nltk

nltk.download("punkt")  # this step would usually be done inside a Dockerfile
from nltk import word_tokenize


@lru_cache
def get_foul_words() -> list[str]:
    return settings.CSV_FOUL_WORDS.split(",")


def has_foul_language(sentence: str) -> bool:
    """This function checks if a sentence contains foul words.

    Args:
        sentence (str): The sentence to be moderated.

    Returns:
        bool: True if the sentence is safe, False otherwise.
    """

    words = word_tokenize(sentence)
    return any(word in get_foul_words() for word in words)
