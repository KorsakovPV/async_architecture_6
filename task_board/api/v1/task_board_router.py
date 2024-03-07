from uuid import UUID


from sqlalchemy import select


from db.model import TaskBoard

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.task_schemas import TaskReadSchema, TaskCreateSchema, TaskEditSchema
from fastapi import APIRouter, status, Depends

from typing import Generic, Sequence, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel, EmailStr
from sqlalchemy import BinaryExpression, and_, delete, exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import _AbstractLoad


from db.base import get_async_session

task_board_router = APIRouter(prefix="/task_board")


@task_board_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskReadSchema]
)
async def get_tasks_board(
        session: AsyncSession = Depends(get_async_session)
):
    statement = select(TaskBoard)
    return (await session.execute(statement)).scalars().all()


@task_board_router.get(
    "{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskReadSchema
)
async def get_task_board(
    task_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    statement = select(TaskBoard).where(TaskBoard.id == task_id)
    return (await session.execute(statement)).scalar_one_or_none()


@task_board_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskReadSchema,
)
async def create_task_board(
        task: TaskCreateSchema,
        session: AsyncSession = Depends(get_async_session),
):
    results = await session.execute(
        insert(TaskBoard)
        .values(status="pending", **task.dict(exclude_unset=True))
        .returning(TaskBoard)
        .options()
    )
    create_task = results.scalar_one()

    await session.commit()

    return create_task



@task_board_router.patch(
    "{task_id}",
    status_code=status.HTTP_200_OK,
)
async def update_task_board(
        task_id: UUID,
        task: TaskEditSchema,
        session: AsyncSession = Depends(get_async_session),
):
    update_task = (
        await session.execute(
            update(TaskBoard)
            .where(TaskBoard.id == task_id)
            .values(**task.dict(exclude_unset=True))
            .returning(TaskBoard)
            .options()
        )
    ).scalar_one_or_none()

    await session.commit()

    return update_task


@task_board_router.delete(
    "{task_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_task_board(
        task_id: UUID,
        session: AsyncSession = Depends(get_async_session),
):
    result = (
        await session.execute(delete(TaskBoard).where(TaskBoard.id == task_id).returning(TaskBoard))
    ).scalar_one_or_none()
    return result


@task_board_router.post(
    "/assign_tasks",
    status_code=status.HTTP_200_OK,
)
async def assign_tasks(
):
    #TODO Получить список пользователей с нужными ролями
    # получить не закрытые таски
    # заасайнить их


    return "assign_tasks"
