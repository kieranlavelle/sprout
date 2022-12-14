import re
from functools import lru_cache

from moderation_service.config import settings

# in the real world we would likely use something like spacy
# or nltk to tokenize our sentences and remove punct.
splitting_regex = re.compile("([\w][\w]*'?\w?)")


@lru_cache
def get_foul_words() -> list[str]:
    return settings.CSV_FOUL_WORDS.split(",")


def _split_sentence(sentence: str) -> list[str]:
    """This function splits a sentence into words.

    Args:
        sentence (str): The sentence to be split.

    Returns:
        list[str]: The words in the sentence.
    """

    return splitting_regex.findall(sentence)


def has_foul_language(sentence: str) -> bool:
    """This function checks if a sentence contains foul words.

    Args:
        sentence (str): The sentence to be moderated.

    Returns:
        bool: True if the sentence is safe, False otherwise.
    """

    words = _split_sentence(sentence)
    return any(word in get_foul_words() for word in words)
