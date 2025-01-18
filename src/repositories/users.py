from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from schemas.users import UserCreateModel
from db.models.users import User


@dataclass
class UsersRepository:
    async_session: sessionmaker

    async def get_user_by_id(self, user_id: int) -> User:
        async with self.async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalars().first()

    async def get_users(self) -> Sequence[User]:
        async with self.async_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()

    async def create_user(self, user: UserCreateModel) -> User:
        new_user = User(
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email
        )
        async with self.async_session() as session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    async def delete_user(self, user_id: int) -> bool:
        async with self.async_session() as session:
            user = await self.get_user_by_id(user_id)
            if user:
                await session.delete(user)
                await session.commit()
                return True
        return False
