import asyncio

import pytest

from db.session import get_db_session_manager
from repositories import UsersRepository


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_session_manager():
    return get_db_session_manager()


@pytest.fixture(scope="session")
def rep(db_session_manager) -> UsersRepository:
    return UsersRepository(db_session_manager)
