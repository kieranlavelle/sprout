import os

import boto3
from moto import mock_dynamodb
from uvicorn import run

from sprout.config import settings


def create_dynamo_db_table():
    client = boto3.client("dynamodb")
    client.create_table(
        TableName=settings.BLOG_TABLE_NAME,
        BillingMode="PAY_PER_REQUEST",
        KeySchema=[
            {"AttributeName": "hk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "hk",
                "AttributeType": "S",
            },
            {
                "AttributeName": "sk",
                "AttributeType": "S",
            },
        ],
    )


def run_webserver():
    os.environ["DEV_MODE"] = "True"
    with mock_dynamodb():
        create_dynamo_db_table()
        run("sprout.app:app", host="127.0.0.1")


if __name__ == "__main__":
    run_webserver()
