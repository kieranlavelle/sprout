import pytest

from fastapi.testclient import TestClient


def test_api_happy_path(test_client: TestClient) -> None:
    # check saved in db
    pytest.fail("Not implemented")
