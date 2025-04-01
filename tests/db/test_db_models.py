from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db.models import User, Group, Membership, Address, AddressType


class TestDbModels:

    async def test_users__addresses__ok(self, db_session_manager):
        new_user = User("first_name", "last_name", f"{uuid4().hex}@text.com")
        async with db_session_manager.get_session() as session:
            async with session.begin():
                session.add(new_user)
                await session.flush()

                session.add_all(
                    [
                        Address(
                            new_user.id, address1="address1", type=AddressType.PRIMARY
                        ),
                        Address(new_user.id, address1="address2"),
                    ]
                )
                await session.flush()

                result = await session.execute(
                    select(User)
                    .options(
                        joinedload(User.addresses), joinedload(User.primary_address)
                    )
                    .where(User.id == new_user.id)
                )
                user = result.scalars().first()

        assert user.primary_address
        assert len(user.addresses) == 2
        assert user.addresses[0].type == AddressType.PRIMARY
        assert user.addresses[1].type == AddressType.REGULAR
        assert user.primary_address.type == AddressType.PRIMARY

    async def test_users__primary_address__unique_constraint_error(
        self, db_session_manager
    ):
        new_user = User("first_name", "last_name", f"{uuid4().hex}@text.com")
        async with db_session_manager.get_session() as session:
            async with session.begin():
                session.add(new_user)
                await session.flush()

                session.add(
                    Address(new_user.id, address1="address1", type=AddressType.PRIMARY)
                )
                await session.flush()

                result = await session.execute(
                    select(User)
                    .options(
                        joinedload(User.addresses), joinedload(User.primary_address)
                    )
                    .where(User.id == new_user.id)
                )
                user = result.scalars().first()

        assert user.addresses
        assert user.primary_address

        with pytest.raises(Exception) as ex:
            async with db_session_manager.get_session() as session:
                async with session.begin():
                    session.add(
                        Address(
                            new_user.id, address1="address1", type=AddressType.PRIMARY
                        )
                    )

        assert "violates unique constraint" in str(ex)

    async def test_users__groups(self, db_session_manager):
        new_user = User("first_name", "last_name", f"{uuid4().hex}@text.com")
        new_group = Group("test group")

        async with db_session_manager.get_session() as session:
            async with session.begin():
                session.add(new_user)
                session.add(new_group)
                new_group.members.append(new_user)

            result = await session.execute(
                select(User)
                .options(joinedload(User.groups), joinedload(User.memberships))
                .where(User.id == new_user.id)
            )
            user = result.scalars().first()

        assert user.groups
        assert user.memberships
        assert isinstance(user.groups[0], Group)
        assert isinstance(user.memberships[0], Membership)

    async def test_groups__users(self, db_session_manager):
        user1 = User("first_name1", "last_name", f"{uuid4().hex}@text.com")
        user2 = User("first_name2", "last_name", f"{uuid4().hex}@text.com")
        new_group = Group("test group")

        async with db_session_manager.get_session() as session:
            async with session.begin():
                session.add(user1)
                session.add(user2)
                session.add(new_group)
                user1.groups.append(new_group)
                user2.groups.append(new_group)

            result = await session.execute(
                select(Group)
                .options(joinedload(Group.members), joinedload(Group.memberships))
                .where(Group.id == new_group.id)
            )
            new_group = result.scalars().first()

        assert len(new_group.members) == 2
        assert len(new_group.memberships) == 2