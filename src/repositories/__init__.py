from typing import Annotated, AsyncGenerator

from fastapi import Depends

from db.engine import DBSessionManagerDep

from .users import UsersRepository


async def get_repository(
    session_manager: DBSessionManagerDep,
) -> AsyncGenerator[UsersRepository, None]:
    yield UsersRepository(session_manager)


RepositoryDep = Annotated[UsersRepository, Depends(get_repository)]
