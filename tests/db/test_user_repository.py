from datetime import datetime

import pytest

from schemas.users import UserCreateModel


@pytest.mark.asyncio(loop_scope="session")
class TestUsersRepository:

    async def test_create_user__ok(self, rep):
        new_email = f"{datetime.now().timestamp()}_test@test.com"
        new_user = UserCreateModel(
            first_name="first name", last_name="last name", email=new_email
        )
        result = await rep.create_user(new_user)

        assert result.id
        assert result.created_at
        assert result.updated_at

    async def test_create_user__unique_constraint_error(self, rep):
        new_email = f"{datetime.now().timestamp()}_test@test.com"
        new_user = UserCreateModel(
            first_name="first name", last_name="last name", email=new_email
        )
        await rep.create_user(new_user)

        with pytest.raises(Exception) as ex:
            await rep.create_user(new_user)

        assert "violates unique constraint" in str(ex)

    async def test_get_user_by_id__ok(self, rep):
        new_email = f"{datetime.now().timestamp()}_test@test.com"
        new_user = await rep.create_user(
            UserCreateModel(
                first_name="first name", last_name="last name", email=new_email
            )
        )

        result = await rep.get_user_by_id(new_user.id)

        assert result.id == new_user.id
        assert result.first_name == new_user.first_name
        assert result.last_name == new_user.last_name
        assert result.email == new_user.email
        assert result.created_at == new_user.created_at
        assert result.updated_at == new_user.updated_at
        assert result.primary_address is None
        assert result.addresses == []
        assert result.groups == []
        assert result.memberships == []

    async def test_get_user_by_id__not_found(self, rep):
        result = await rep.get_user_by_id(-9999)
        assert result is None

    async def test_get_all__ok(self, rep):
        new_email = f"{datetime.now().timestamp()}_test@test.com"
        await rep.create_user(
            UserCreateModel(
                first_name="first name", last_name="last name", email=new_email
            )
        )

        results = await rep.get_users()

        assert len(results) > 0
        result = results[-1]
        assert result.id
        assert result.first_name
        assert result.last_name
        assert result.email == new_email

    async def test_update_user__ok(self, rep):
        new_email = f"{datetime.now().timestamp()}_test@test.com"
        new_user = await rep.create_user(
            UserCreateModel(
                first_name="first name", last_name="last name", email=new_email
            )
        )

        expected_email = f"{datetime.now().timestamp()}_some_new@test.com"
        expected_first_name = "new_first_name"
        await rep.update_user(
            new_user.id, first_name=expected_first_name, email=expected_email
        )

        result = await rep.get_user_by_id(new_user.id)

        assert result.first_name == expected_first_name
        assert result.email == expected_email

    async def test_delete_user__ok(self, rep):
        new_email = f"{datetime.now().timestamp()}_test@test.com"
        new_user = await rep.create_user(
            UserCreateModel(
                first_name="first name", last_name="last name", email=new_email
            )
        )

        await rep.delete_user(new_user.id)

        result = await rep.get_user_by_id(new_user.id)
        assert result is None
