
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
#### Database Of Choise
#### Tokenisation
#### Process the blog post after a while and then mark it to go live
#### Table design for dynamoDB
#### A real-world architechture.
