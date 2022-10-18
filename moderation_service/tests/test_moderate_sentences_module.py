import pytest

from moderation_service.core.services.moderate_sentences import (
    get_foul_words,
    has_foul_language,
)


def test_loading_words(create_foul_words: list[str]) -> None:
    """This test validates that the foul words are loaded correctly."""
    words = get_foul_words()
    if words != create_foul_words:
        pytest.fail("The foul words were not loaded correctly.")


def test_does_find_foul_words(create_foul_words: list[str]) -> None:
    """This test validates that the foul words are found correctly."""
    sentence = " ".join(create_foul_words)

    if not has_foul_language(sentence):
        pytest.fail("The foul words were not found correctly.")


def test_does_not_find_foul_words(create_foul_words: list[str]) -> None:
    """This test validates that the foul words are not found incorrectly."""
    sentence = "There are no foul words in this sentence."

    if has_foul_language(sentence):
        pytest.fail("Incorrectly marked sentence as foul.")


def test_fould_words_found_when_next_to_punc(create_foul_words: list[str]) -> None:
    """This test validates that the foul words are found correctly.

    This example is to make sure that the regex is working correctly by removing
    punctuation from the words.
    """

    foul_word = create_foul_words[0]
    sentence = f"{foul_word}! the rest of the sentence?"

    if not has_foul_language(sentence):
        pytest.fail("The foul words were not found correctly.")
