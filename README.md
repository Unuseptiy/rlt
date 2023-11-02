# Salary aggregator

## Project set up
1) `git clone` project.

2) `cd salary_aggregator`

3) Set up env vars

```commandline
touch .env
```

Fill the `.env` file with:
```commandline
MONGO_URI=
DB_NAME=
BOT_TOKEN=
```
with coresponding values. 

4) Add mongo dump to `dump` dir.

5) Set up mongo
```commandline
docker run --name test-mongo -p 27117:27017 -v "$(pwd)/dump":/dump -d mongo
docker exec -t test-mongo mongorestore
```

## Project test
Prerequisites: poetry

1) poetry install
2) poetry run pytest
