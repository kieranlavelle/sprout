from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


def test_foul_words_are_correctly_marked(
    test_client: TestClient, foul_sentence: str
) -> None:
    """This test validates that foul words are correctly marked."""

    response = test_client.post("/sentences", json={"fragment": foul_sentence})
    if response.status_code != HTTPStatus.OK:
        pytest.fail(f"Unexpected status code: {response.status_code}")

    # check the response body
    expected_response = {"hasFoulLanguage": True}
    if response.json() != expected_response:
        pytest.fail(f"Unexpected response: {response.json()}")


@pytest.mark.parametrize("sentence", ["", "This is a non foul sentence"])
def test_non_foul_sentences_are_correctly_marked(
    test_client: TestClient, sentence: str
) -> None:
    """This test validates that foul words are correctly marked."""

    response = test_client.post("/sentences", json={"fragment": sentence})
    if response.status_code != HTTPStatus.OK:
        pytest.fail(f"Unexpected status code: {response.status_code}")

    # check the response body
    expected_response = {"hasFoulLanguage": False}
    if response.json() != expected_response:
        pytest.fail(f"Unexpected response: {response.json()}")
