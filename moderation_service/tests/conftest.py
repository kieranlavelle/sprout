import pytest
from fastapi.testclient import TestClient

from moderation_service.app import app
from moderation_service.config import settings


@pytest.fixture
def create_foul_words(monkeypatch) -> list[str]:
    """This fixture is used to create a list of foul words."""

    foul_words = ["java", "php", "crap"]
    foul_words_csv = ",".join(foul_words)

    settings.CSV_FOUL_WORDS = foul_words_csv
    return foul_words


@pytest.fixture
def test_client() -> TestClient:
    """This fixture is used to create a test client."""

    return TestClient(app)


@pytest.fixture(autouse=True)
def foul_sentence(create_foul_words: list[str]) -> str:
    """This fixture is used to create a foul sentence."""

    foul_word = create_foul_words[0]
    sentence = f"{foul_word}! the rest of the sentence?"
    return sentence
