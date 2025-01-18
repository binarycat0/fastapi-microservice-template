from asyncpg import UniqueViolationError
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from sqlalchemy.exc import IntegrityError

from schemas.users import UserCreateModel, UserResponseModel
from repositories.users import UsersRepository

router = APIRouter()


@router.post("/", response_model=UserResponseModel)
async def create_new_user(request: Request, user: UserCreateModel):
    users_repository: UsersRepository = request.app.state.users_repository
    try:
        new_user = await users_repository.create_user(user)
        return new_user
    except IntegrityError as ex:
        raise HTTPException(status_code=400, detail="User already exists.")


@router.get("/{user_id}", response_model=UserResponseModel)
async def read_user(request: Request, user_id: int):
    users_repository: UsersRepository = request.app.state.users_repository
    user = await users_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[UserResponseModel])
async def read_users(request: Request):
    users_repository: UsersRepository = request.app.state.users_repository
    return await users_repository.get_users()


@router.delete("/{user_id}")
async def delete_user_endpoint(request: Request, user_id: int):
    users_repository: UsersRepository = request.app.state.users_repository
    success = await users_repository.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "deleted"}
