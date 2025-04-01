import contextlib
from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from settings import get_settings

settings = get_settings()


class DbSessionManager:
    expire_on_commit: bool = False

    def __init__(self, dsn: str | None = None):
        self.engine = create_async_engine(dsn or settings.db.dsn, echo=True)
        self.async_sessionmaker = async_sessionmaker(
            bind=self.engine, expire_on_commit=self.expire_on_commit
        )

    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.async_sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@lru_cache
def get_db_session_manager(dsn: str | None = None) -> DbSessionManager:
    return DbSessionManager(dsn)
