# fastapi-microservice-template
The Ultimate Super-Convenient Template for Microservices Based on FastAPI

By default, the application starts on 0.0.0.0 host and 8000 port: http://0.0.0.0:8000/

There is a little help:
- To get Swagget Docs reach: http://0.0.0.0:8000/docs
- To get openapi spec reach: http://0.0.0.0:8000/docs/openapi


## Initiate poetry environment
Make sure you set up poetry: https://python-poetry.org/

### Check
    which poetry
    poetry --version

### Install/Update environment

    make install

## Local development
Before start your development journey make sure you set up your poetry environment and run postgresql server.

### ex: run postgresql in docker
    docker run \
    --name test-db-postgres \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=microservice \
    -p 5432:5432 \
    -d postgres

### Migrations:

#### generate new
    make migration m="comment"

#### apply migrations
    make migrate

### Run locally
    make run

### Run in docker-compose environment
    
#### run
    make docker-up
    make docker-migrate

#### down
    make docker-down