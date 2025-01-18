from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.engine import init_async_sessionmaker
from repositories.users import UsersRepository
from settings import get_settings

settings = get_settings()
templates_dir = settings.base_dir + "/templates"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup Ultimate Microservice")
    # init common services or repositories
    sessionmaker = init_async_sessionmaker(settings)
    app.state.users_repository = UsersRepository(sessionmaker)

    #
    yield
    print("Shutdown Ultimate Microservice")


def create_app() -> FastAPI:
    app = FastAPI(openapi_url="/docs/openapi", docs_url="/docs", lifespan=lifespan)
    templates = Jinja2Templates(directory=templates_dir)

    #
    @app.get("/", response_class=HTMLResponse, name="help")
    async def home(request: Request):
        return templates.TemplateResponse(request, "index.html")

    #
    from api import api_router

    app.include_router(api_router)
    return app


if __name__ == "__main__":
    uvicorn.run("app:create_app", host="0.0.0.0", port=8000, reload=True)
