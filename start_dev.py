import os

import boto3
from moto import mock_dynamodb
from uvicorn import run


def create_dynamo_db_table():
    client = boto3.client("dynamodb")
    client.create_table(
        TableName="core-api",
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
            {
                "AttributeName": "billing_rate_id",
                "AttributeType": "S",
            },
            {
                "AttributeName": "driver_id",
                "AttributeType": "N",
            },
            {
                "AttributeName": "date_created",
                "AttributeType": "S",
            },
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "billing_rates_by_id",
                "KeySchema": [
                    {"AttributeName": "billing_rate_id", "KeyType": "HASH"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "jobs_by_driver",
                "KeySchema": [
                    {"AttributeName": "hk", "KeyType": "HASH"},
                    {"AttributeName": "driver_id", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "jobs_by_date",
                "KeySchema": [
                    {"AttributeName": "hk", "KeyType": "HASH"},
                    {"AttributeName": "date_created", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "quote_by_date",
                "KeySchema": [
                    {"AttributeName": "hk", "KeyType": "HASH"},
                    {"AttributeName": "date_created", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
    )


def run_webserver():
    os.environ["DEV_MODE"] = "True"
    with mock_dynamodb:
        create_dynamo_db_table()
        run("sprout.app:app", host="127.0.0.1")


if __name__ == "__main__":
    run_webserver()
