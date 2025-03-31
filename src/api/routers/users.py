from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from repositories import RepositoryDep
from schemas.users import UserCreateModel, UserResponseModel

router = APIRouter()


@router.post("/", response_model=UserResponseModel)
async def create_new_user(user: UserCreateModel, users_repository: RepositoryDep):
    try:
        new_user = await users_repository.create_user(user)
        return new_user
    except IntegrityError as ex:
        raise HTTPException(status_code=400, detail="User already exists.")


@router.get("/{user_id}", response_model=UserResponseModel)
async def read_user(user_id: int, users_repository: RepositoryDep):
    user = await users_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[UserResponseModel])
async def read_users(users_repository: RepositoryDep):
    return await users_repository.get_users()


@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, users_repository: RepositoryDep):
    success = await users_repository.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "deleted"}
