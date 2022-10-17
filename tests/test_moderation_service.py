"""This module contains a set of tests that validates the
functionality within the moderation service. The moderation API itself
is mocked."""

import httpx
import pytest

from sprout.core.services.content_moderation_service import (
    _create_sentences,
    moderate_content,
)


def test_create_sentences(paragraphs: list[str], expected_sentences: list[str]) -> None:

    sentences = _create_sentences(paragraphs)
    sentences = list(sentences)
    if sentences != expected_sentences:
        pytest.fail("Sentences are not the same")


@pytest.mark.parametrize("has_foul_language,expected", [(True, False), (False, True)])
def test_moderate_content(
    paragraphs: list[str], httpx_mock, has_foul_language, expected
) -> None:

    # add a mocked response for httpx for the moderation service
    def has_foul_language_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"hasFoulLanguage": has_foul_language},
        )

    httpx_mock.add_callback(has_foul_language_response)

    result = moderate_content(paragraphs)
    if result != expected:
        pytest.fail("Content was incorrectly marked.")
