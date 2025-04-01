__all__ = [
    "get_db_manager",
    "DBSessionManagerDep",
]

from typing import Annotated, AsyncGenerator

from fastapi import Depends

from .session import DbSessionManager, get_db_session_manager


async def get_db_manager() -> AsyncGenerator[DbSessionManager, None]:
    yield get_db_session_manager()


DBSessionManagerDep = Annotated[DbSessionManager, Depends(get_db_manager)]
