
# BlogsAPI

The point of this api is to ingest blog posts which are made up of a title & a collection of this paragraphs and store them in a database. Prior to storing these posts, the paragraphs must be split into sentences and checked to ensure that none of the word's within those sentences are "foul" words. Depending on the result of that check, a database property on the row for that blog post should either be marked True or False.

## Running the application
```bash
docker compose up
```

## Running the tests
```bash
# install poetry
pip install poetry

# running the tests for the blogs_api
cd blogs_api
poetry install
poetry run pytests

# running the tests for the moderation_service
cd moderation_service
poetry install
poetry run pytests
```

## Points to consider
#### Database Of choice
For the database, I went with a local version of DynamoDB running inside a docker-container. For the unit-testing I've used the package `moto` to mock the database calls. The main reason's I chose dynamo are outlined below.
1. High scalability, as the application scales the database performance should remain constant.
1. You only have to pay for the throughput you use.
1. It's fast to develop with.
1. It's easy to model the data in when your use cases are know. As they were in this case.

It's also worth highlighting the table design. In this case the table has a compound primary key where the title of the blog post is the hash-key and the date_created of the blog post is the sort key. In a real world application, we'd probably want to have a generic hash-key value of something like `#BLOG_POST` & a ULID sort-key (A UUID that is UTF sortable) for the blog post id. We'd likely also want several global secondary indexes to support additional query patterns on our blog items in the database, such as `blog_posts_by_user` & `blog_posts_by_date`. We'd design the table in this way in order to allow us to store all of the attributes for the API in a single table, as is often recommended for DynamoDB.

#### Tokenisation
#### Process the blog post after a while and then mark it to go live
#### Table design for dynamoDB
#### A real-world architechture.
