__all__ = ["api_router"]

from fastapi import APIRouter

from .routers.users import router as users_router

api_router = APIRouter(prefix="/api")
api_router.include_router(users_router, prefix="/users")
