 
# Blogs API & Moderation API
 
The point of this API is to ingest blog posts which are made up of a title & a collection of paragraphs and store them in a database. Prior to saving these posts, the paragraphs must be split into sentences and checked to ensure that no words in the sentences are "foul". Depending on the result of that check, a database property on the row for that blog post should either be marked True or False.
 
## Running the application
1. Install docker.
2. `cd` to the root of the repository.
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

## Foul words
There are a couple of places where foul word's are configured depending on how you're running the application. In the case of unit tests the foul words environment variable `CSV_FOUL_WORDS` is set in `conftest.py`. The foul words are `"java", "php", "crap"`. When running the application using docker, the environment variable `CSV_FOUL_WORDS` is set in the container; `ENV CSV_FOUL_WORDS=java,php,html,crap`.

## Database Of choice
For the database, I went with a local version of DynamoDB running inside a docker container. For the unit testing, I've used the package `moto` to mock the database calls. The main reason's I chose dynamo are outlined below.
1. High scalability, as the application scales the database performance should remain constant.
1. You only have to pay for the throughput you use.
1. It's fast to develop with.
1. It's easy to model the data when your use cases are known. As they were in this case.
 
It's also worth highlighting the table design.
```json
# current table design
# primary key = (title, date_created)
{
   "title": "kierans blog post",
   "date_created": "2022-10-17T19:33:24.877456",
   "paragraphs": [...],
   "has_foul_language": False
}
 
# real world table design
# primary key = (hk, sk)
{
   "hk": "#BLOG_POST",
   "sk": "01GFKQ30926MMQ7HNQSDZSCYXH",
   "paragraphs": [....],
   "date_created": "2022-10-17T19:33:24.877456",
   "created_by": "kieran"
}
```
 
In the code base, the first table pattern is used. This has been done to aid with the readability of the code. I've provided a more typical real-world example below to indicate what a production table might look like. The improved example has a couple of features that the first one does not have. I've highlighted these below. The real-world table design is an example of a pattern in DynamoDB where you use a single table for your entire application and is typically the recommended way to design dynamo tables.
1. As it's typical to store multiple entity types in a single DynamoDB table, the name of our hash and sort key attributes should be generic. In this case, they're `hk` & `sk`.
2. By having a fixed hash_key value for each entity type we're able to write queries that only fetch a single entity type from the database.
3. Using a ULID as our sort-key attribute ensures the items are sorted in the database.
4. We can have additional attributes & global secondary indexes to enable other query patterns that are not directly supported by the hash or sort key.
 
 
## Tokenisation
For tokenising the strings into words and sentences I've used a naive approach. The best / most appropriate approach would depend on how the downstream model had been trained. It'd likely be best to do some sort of customised text cleaning using one of several libraries for nlp such as `spaCy` or `nltk`.
 
## Process the blog post after a while and then mark it to go live
In a real-world system, it might be best to split the process of adding blog posts into two distinct stages. The approach below provides fast response times to users, whilst still enabling the system to check all posts.
1. The post is sent to the API, which puts the `post` on a queue for processing.
2. A worker read's `posts` off of the queue, and checks their content to see if it's safe or not. This worker then inserts the post into the database and set's the attribute `has_foul_language` against the item in the database.
 

 

