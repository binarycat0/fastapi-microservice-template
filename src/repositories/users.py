from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import asc, delete, select, update
from sqlalchemy.orm import joinedload, selectinload

from db.models.users import User
from db.session import DbSessionManager
from schemas.users import UserCreateModel


@dataclass
class UsersRepository:
    session_manager: DbSessionManager

    async def get_user_by_id(self, user_id: int) -> User | None:
        async with self.session_manager.get_session() as session:
            result = await session.execute(
                select(User)
                .options(
                    joinedload(User.primary_address),
                    joinedload(User.addresses),
                    joinedload(User.groups),
                    joinedload(User.memberships),
                )
                .where(User.id == user_id)
            )
            return result.scalars().first()

    async def get_users(self) -> Sequence[User]:
        async with self.session_manager.get_session() as session:
            result = await session.execute(
                select(User)
                .options(
                    selectinload(User.addresses),
                    selectinload(User.primary_address),
                    selectinload(User.groups),
                    selectinload(User.memberships),
                )
                .order_by(asc(User.created_at))
            )
            return result.scalars().all()

    async def create_user(self, user: UserCreateModel) -> User:
        new_user = User(
            first_name=user.first_name, last_name=user.last_name, email=user.email
        )
        async with self.session_manager.get_session() as session:
            async with session.begin():
                session.add(new_user)
            await session.refresh(new_user)
            return new_user

    async def update_user(
        self,
        user_id: int,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None
    ) -> None:
        values = {}
        if first_name is not None:
            values["first_name"] = first_name
        if last_name is not None:
            values["last_name"] = last_name
        if email is not None:
            values["email"] = email

        async with self.session_manager.get_session() as session:
            async with session.begin():
                await session.execute(
                    update(User).where(User.id == user_id).values(**values)
                )

    async def delete_user(self, user_id: int) -> None:
        async with self.session_manager.get_session() as session:
            async with session.begin():
                await session.execute(delete(User).where(User.id == user_id))
