from uuid import UUID


from sqlalchemy import select


from db.model import TaskBoard

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.task_schemas import TaskReadSchema
from fastapi import APIRouter, status, Depends


from db.base import get_async_session

task_board_router = APIRouter(prefix="/task_board")


@task_board_router.get(
    "", status_code=status.HTTP_200_OK, response_model=list[TaskReadSchema]
)
async def get_tasks_board(session: AsyncSession = Depends(get_async_session)):

    statement = select(TaskBoard)
    return (await session.execute(statement)).scalars().all()


@task_board_router.get(
    "{task_id}", status_code=status.HTTP_200_OK, response_model=list[TaskReadSchema]
)
async def get_task_board(
    task_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    statement = select(TaskBoard).where(TaskBoard.id == task_id)
    return (await session.execute(statement)).scalar_one_or_none()


@task_board_router.post(
    "",
    status_code=status.HTTP_200_OK,
)
async def create_task_board(
    search: str | None = None,
    is_deleted: bool | None = None,
):
    return "get_task_board"


@task_board_router.put(
    "{task_id}",
    status_code=status.HTTP_200_OK,
)
async def update_task_board(
    search: str | None = None,
    is_deleted: bool | None = None,
):
    return "get_task_board"


@task_board_router.delete(
    "{task_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_task_board(
    search: str | None = None,
    is_deleted: bool | None = None,
):
    return "get_task_board"


@task_board_router.post(
    "/assign_tasks",
    status_code=status.HTTP_200_OK,
)
async def assign_tasks(
    search: str | None = None,
    is_deleted: bool | None = None,
):
    return "assign_tasks"
