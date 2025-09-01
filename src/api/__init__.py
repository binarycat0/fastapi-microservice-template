__all__ = ["api_router"]

from fastapi import APIRouter

from .routers.users import router as users_router

api_router = APIRouter(prefix="/api/v1", tags=["api"])
api_router.include_router(users_router)
