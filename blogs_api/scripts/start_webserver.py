import uvicorn
import boto3

from blogs_api.app import app
from blogs_api.config import settings


def start() -> None:
    """Starts the FastAPI server."""
    create_table()
    uvicorn.run(app, host="0.0.0.0", port=8000)


def create_table() -> None:
    client = boto3.client(
        "dynamodb",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.DYNAMODB_ADDRESS,
    )

    try:
        client.delete_table(TableName=settings.BLOG_TABLE_NAME)
    except:
        pass

    client.create_table(
        TableName=settings.BLOG_TABLE_NAME,
        BillingMode="PAY_PER_REQUEST",
        KeySchema=[
            {"AttributeName": "title", "KeyType": "HASH"},
            {"AttributeName": "date_created", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "title", "AttributeType": "S"},
            {"AttributeName": "date_created", "AttributeType": "S"},
        ],
    )
