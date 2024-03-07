from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class BaseReadSchema(BaseModel):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class BaseCreateSchema(BaseModel):
    pass


class BaseEditSchema(BaseModel):
    pass


class TaskBaseSchema(BaseModel):
    description: str



class TaskReadSchema(TaskBaseSchema, BaseReadSchema):
    assigned_user_id: UUID | None
    status: Literal["pending", "done"]


class TaskCreateSchema(TaskBaseSchema, BaseCreateSchema):
    pass


class TaskEditSchema(TaskBaseSchema, BaseEditSchema):
    description: str | None = None
    status: Literal["pending", "done"]
