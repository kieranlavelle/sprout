import pytest

from moderation_service.config import settings


@pytest.fixture
def create_foul_words(monkeypatch) -> list[str]:
    """This fixture is used to create a list of foul words."""

    foul_words = ["java", "php", "crap"]
    foul_words_csv = ",".join(foul_words)

    settings.CSV_FOUL_WORDS = foul_words_csv
    return foul_words
