from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class BaseReadSchema(BaseModel):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class BaseCreateSchema(BaseModel):
    pass


class BaseEditSchema(BaseModel):
    pass


class TaskBaseSchema(BaseModel):
    description: str


class TaskReadSchema(TaskBaseSchema, BaseReadSchema):
    assigned_user_id: UUID | None
    status: Literal["pending", "done"]
    is_billing: bool


class TaskCreateSchema(TaskBaseSchema, BaseCreateSchema):
    pass


class TaskEditSchema(TaskBaseSchema, BaseEditSchema):
    description: str | None = None
    status: Literal["pending", "done"]


class TaskBrockerMassageSchemaV1(BaseModel):
    """Схема для отправки сообщений в брокер"""
    title: str = "Billing.Accruals.v1"
    description: str = "json schema for billing accruals event (version 1)"
    event_datetime: datetime | None = None
    version: int = 1
    body: list[TaskReadSchema]


class TaskAssignSchema(BaseModel):
    assigned_user_id: UUID
    price: int = -10

class TaskAssignMassageSchemaV1(BaseModel):
    """Схема для отправки сообщений в брокер"""
    title: str = "Billing.Assign.v1"
    description: str = "json schema for billing assign event (version 1)"
    event_datetime: datetime | None = None
    version: int = 1
    body: list[TaskAssignSchema]
