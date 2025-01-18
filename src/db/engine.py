__all__ = [
    "init_async_sessionmaker",
]

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import Settings


def init_async_sessionmaker(settings: Settings) -> sessionmaker:
    engine = create_async_engine(settings.db.dsn, echo=True)
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
