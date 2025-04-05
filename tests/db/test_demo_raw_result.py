import contextlib
import datetime
from decimal import Decimal
from typing import Mapping

from sqlalchemy import select, delete, CursorResult
from sqlalchemy.engine.row import RowProxy

from db.models import DemoModel


@contextlib.asynccontextmanager
async def create_demo_model(session_manager):
    demo_model = DemoModel(
        1,
        1.1,
        Decimal("12388888.00009"),
        1,
        "col_str",
        False,
        datetime.datetime.now(datetime.UTC),
        datetime.datetime.now(datetime.UTC),
        [1, 2, 3],
    )

    async with session_manager.get_session() as session:
        async with session.begin():
            session.add(demo_model)

    yield demo_model

    async with session_manager.get_session() as session:
        session.execute(delete(DemoModel).where(DemoModel.id == demo_model.id))


class TestDemoQuery:
    async def test_result_as_model(self, db_session_manager):
        async with create_demo_model(db_session_manager) as demo_model:
            async with db_session_manager.get_session() as session:
                result = await session.execute(
                    select(DemoModel).where(DemoModel.id == demo_model.id)
                )
                models = result.scalars().all()
                assert models
                assert isinstance(models[0], DemoModel)

    async def test_result_as_row(self, db_session_manager):
        async with create_demo_model(db_session_manager) as demo_model:
            async with db_session_manager.get_session() as session:
                result = await session.execute(
                    select(DemoModel).where(DemoModel.id == demo_model.id)
                    # also you can select particular fields
                    # select(DemoModel.id, DemoModel.col_decimal).where(DemoModel.id == demo_model.id)
                )

                list_of_rows = result.fetchall()
                assert list_of_rows
                assert isinstance(list_of_rows[0], RowProxy)

    async def test_result_as_mapping(self, db_session_manager):
        async with create_demo_model(db_session_manager) as demo_model:
            async with db_session_manager.get_session() as session:
                result = await session.execute(
                    select(DemoModel).where(DemoModel.id == demo_model.id)
                    # also you can select particular fields
                    # select(DemoModel.id, DemoModel.col_decimal).where(DemoModel.id == demo_model.id)
                )

                list_of_rows = result.mappings().fetchall()
                assert list_of_rows
                assert isinstance(list_of_rows[0], Mapping)
                assert "DemoModel" in list_of_rows[0]

    async def test_use_engine_as_row(self, db_session_manager, db_engine):
        async with create_demo_model(db_session_manager) as demo_model:
            async with db_engine.begin() as aconn:
                result = await aconn.execute(
                    select(DemoModel).where(DemoModel.id == demo_model.id)
                )

                assert isinstance(result, CursorResult)
                list_of_rows = result.fetchall()
                assert isinstance(list_of_rows[0], RowProxy)

    async def test_use_engine_as_mapping(self, db_session_manager, db_engine):
        async with create_demo_model(db_session_manager) as demo_model:
            async with db_engine.begin() as aconn:
                result = await aconn.execute(
                    select(DemoModel).where(DemoModel.id == demo_model.id)
                )

                assert isinstance(result, CursorResult)
                list_of_rows = result.mappings().fetchall()
                assert isinstance(list_of_rows[0], Mapping)
                assert "DemoModel" not in list_of_rows[0]
                assert "id" in list_of_rows[0]
