import boto3
import pytest
from moto import mock_dynamodb


@pytest.fixture(autouse=True)
def create_table():
    with mock_dynamodb():
        client = boto3.resource("dynamodb")
        table = client.create_table(
            TableName="posts",
            BillingMode="PAY_PER_REQUEST",
            KeySchema=[
                {"AttributeName": "post_id", "KeyType": "HASH"},
                {"AttributeName": "date_created", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "post_id", "AttributeType": "S"},
                {"AttributeName": "date_created", "AttributeType": "S"},
            ],
        )
        yield table


@pytest.fixture
def paragraphs() -> list[str]:
    """This fixture is used to create a list of paragraphs."""
    return [
        "This is the first paragraph. It contains two sentences.",
        "This is the second parapgraph. It contains two more sentences",
        "Third paraphraph here.",
    ]


@pytest.fixture
def expected_sentences() -> list[str]:
    """This fixture is used to create a list of sentences."""
    return [
        "This is the first paragraph",
        "It contains two sentences",
        "This is the second parapgraph",
        "It contains two more sentences",
        "Third paraphraph here",
    ]
