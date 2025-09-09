from typing import Annotated, AsyncGenerator

from fastapi import Depends

from db.engine import DBSessionManagerDep

from .entities import EntitiesRepository
from .users import UsersRepository


async def get_users_repository(
    session_manager: DBSessionManagerDep,
) -> AsyncGenerator[UsersRepository, None]:
    yield UsersRepository(session_manager)


async def get_entities_repository(
    session_manager: DBSessionManagerDep,
) -> AsyncGenerator[EntitiesRepository, None]:
    yield EntitiesRepository(session_manager)


UsersRepositoryDep = Annotated[UsersRepository, Depends(get_users_repository)]
EntitiesRepositoryDep = Annotated[EntitiesRepository, Depends(get_entities_repository)]
