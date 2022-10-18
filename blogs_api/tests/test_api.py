from http import HTTPStatus

import boto3
from boto3.dynamodb.conditions import Key
import pytest
import httpx
from fastapi.testclient import TestClient

from blogs_api.config import settings


@pytest.mark.asyncio
async def test_api_no_foul_language_response(
    test_client: TestClient, paragraphs: list[str], httpx_mock
) -> None:

    # add a mocked response for httpx for the moderation service
    def has_foul_language_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"hasFoulLanguage": False},
        )

    httpx_mock.add_callback(has_foul_language_response)

    response = test_client.post(
        "/posts", json={"title": "test", "paragraphs": paragraphs}
    )

    if response.status_code != HTTPStatus.CREATED:
        pytest.fail("Invalid status code returned from the API.")

    expected_response = {
        "title": "test",
        "paragraphs": paragraphs,
        "has_foul_language": False,
    }

    actual_response = response.json()

    if actual_response != expected_response:
        pytest.fail("Invalid response returned from the API.")


@pytest.mark.asyncio
async def test_api_foul_language_response(
    test_client: TestClient, paragraphs: list[str], httpx_mock
) -> None:

    # add a mocked response for httpx for the moderation service
    def has_foul_language_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"hasFoulLanguage": True},
        )

    httpx_mock.add_callback(has_foul_language_response)

    response = test_client.post(
        "/posts", json={"title": "test", "paragraphs": paragraphs}
    )

    if response.status_code != HTTPStatus.CREATED:
        pytest.fail("Invalid status code returned from the API.")

    expected_response = {
        "title": "test",
        "paragraphs": paragraphs,
        "has_foul_language": True,
    }

    actual_response = response.json()

    if actual_response != expected_response:
        pytest.fail("Invalid response returned from the API.")


@pytest.mark.asyncio
async def test_api_saves_to_db(
    test_client: TestClient, paragraphs: list[str], httpx_mock
) -> None:

    # add a mocked response for httpx for the moderation service
    def has_foul_language_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"hasFoulLanguage": False},
        )

    httpx_mock.add_callback(has_foul_language_response)

    response = test_client.post(
        "/posts", json={"title": "test", "paragraphs": paragraphs}
    )

    if response.status_code != HTTPStatus.CREATED:
        pytest.fail("Invalid status code returned from the API.")

    # query the db for the post
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(settings.BLOG_TABLE_NAME)

    blog_post = table.query(KeyConditionExpression=Key("title").eq("test"))
    if not blog_post["Items"]:
        pytest.fail("Blog post was not saved to the database.")


@pytest.mark.asyncio
async def test_api_fails_gracefully_on_moderation_service_error(
    test_client: TestClient, paragraphs: list[str], httpx_mock
) -> None:

    # add a mocked response for httpx for the moderation service
    def moderation_service_500(request: httpx.Request):
        return httpx.Response(status_code=500)

    httpx_mock.add_callback(moderation_service_500)

    response = test_client.post(
        "/posts", json={"title": "test", "paragraphs": paragraphs}
    )

    if response.status_code != HTTPStatus.INTERNAL_SERVER_ERROR:
        pytest.fail("Invalid status code returned from the API.")


@pytest.mark.asyncio
async def test_api_fails_gracefully_on_moderation_service_bad_format(
    test_client: TestClient, paragraphs: list[str], httpx_mock
) -> None:

    # add a mocked response for httpx for the moderation service
    def moderation_service_500(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"wrongKey": False},
        )

    httpx_mock.add_callback(moderation_service_500)

    response = test_client.post(
        "/posts", json={"title": "test", "paragraphs": paragraphs}
    )

    if response.status_code != HTTPStatus.INTERNAL_SERVER_ERROR:
        pytest.fail("Invalid status code returned from the API.")
