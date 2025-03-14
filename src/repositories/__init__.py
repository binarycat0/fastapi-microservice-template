from typing import Annotated, AsyncGenerator

from fastapi import Depends

from db.engine import sessionmakerDep

from .users import UsersRepository


async def get_repository(
    sessionmaker: sessionmakerDep,
) -> AsyncGenerator[UsersRepository, None]:
    yield UsersRepository(sessionmaker)


RepositoryDep = Annotated[UsersRepository, Depends(get_repository)]
