from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from repositories import EntitiesRepositoryDep, UsersRepository
from schemas.entities import BatchAddEntitiesModel

router = APIRouter(prefix="/entities", tags=["users"])


@router.post("/{user_id}/batch")
async def batch_add_entities(
    user_id: int,
    req: BatchAddEntitiesModel,
    entities_rep: EntitiesRepositoryDep,
    users_rep: UsersRepository,
):
    user = await users_rep.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        await entities_rep.batch_add_entities(user)
    except IntegrityError as ex:
        raise HTTPException(status_code=400, detail="Something went wrong.")
