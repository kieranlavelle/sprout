"""This module contains a set of tests that validates the
functionality within the moderation service. The moderation API itself
is mocked."""

import httpx
import pytest

from blogs_api.core.services.content_moderation_service import (
    _create_sentences,
    has_foul_language,
)


def test_create_sentences(paragraphs: list[str], expected_sentences: list[str]) -> None:

    sentences = _create_sentences(paragraphs)
    sentences = list(sentences)
    if sentences != expected_sentences:
        pytest.fail("Sentences are not the same")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "content_has_foul_language,expected", [(True, True), (False, False)]
)
async def test_moderate_content(
    paragraphs: list[str], httpx_mock, content_has_foul_language, expected
) -> None:

    # add a mocked response for httpx for the moderation service
    def has_foul_language_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"hasFoulLanguage": content_has_foul_language},
        )

    httpx_mock.add_callback(has_foul_language_response)

    result = await has_foul_language(paragraphs)
    if result != expected:
        pytest.fail("Content was incorrectly marked.")
