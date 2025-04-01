# fastapi-microservice-template :floppy_disk: :green_heart:
The Ultimate Super-Convenient Template for Microservices Based on FastAPI :moneybag:

Main article on [medium.com](https://medium.com/@artur.rakhmatulin/the-ultimate-super-convenient-template-for-microservices-based-on-fastapi-919abe76699b). Please check this out.

----

The application starts on 0.0.0.0 host and 8000 port by default.

There is a little help:
- To get Swagget Docs reach: http://0.0.0.0:8000/docs
- To get openapi spec reach: http://0.0.0.0:8000/docs/openapi

`ultimate-fastapi-microservice` implements CRUD for User entity out of the box.

```
Read Users -> GET: /api/users/
Create New User -> POST: /api/users/
Read User -> GET: /api/users/{user_id}
Delete User Endpoint -> DELETE: /api/users/{user_id}
```


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
    --name microservice-db \
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
