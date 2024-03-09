from fastapi import APIRouter

from api.v1.auth_router import auth_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
