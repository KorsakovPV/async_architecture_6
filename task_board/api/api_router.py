from fastapi import APIRouter

from api.v1.task_board_router import task_board_router

api_router = APIRouter(prefix="/api")

api_router.include_router(task_board_router)
