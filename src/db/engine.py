__all__ = [
    "init_async_sessionmaker",
    "sessionmakerDep",
]

from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import get_settings

settings = get_settings()


def init_async_sessionmaker() -> AsyncSession:
    engine = create_async_engine(settings.db.dsn, echo=True)
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_sessionmaker() -> AsyncGenerator[AsyncSession, None]:
    sessionmaker = init_async_sessionmaker()
    yield sessionmaker


sessionmakerDep = Annotated[AsyncSession, Depends(get_sessionmaker)]
