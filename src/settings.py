__all__ = ["Settings", "get_settings"]

import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOT_ENV = os.path.join(PROJECT_ROOT, ".env")


class DbSettings(BaseSettings):
    dsn: str = "postgresql+asyncpg://postgres:password@0.0.0.0:5432/microservice"


ENV_PREFIX = "DEMO_APP_"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOT_ENV, env_prefix=ENV_PREFIX)

    app_name: str = "my_ultimate_microservice"
    base_dir: str = Field(default=BASE_DIR)
    db: DbSettings = DbSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
