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


class BillingTaskBaseSchema(BaseModel):
    assigned_user_id: UUID | None
    task_id: UUID | None
    # sent_email: bool = False
    # is_payment: bool = False
    price: int = -10
    award: int = 100


class BillingTaskReadSchema(BillingTaskBaseSchema, BaseReadSchema):
    pass


class BillingTaskCreateSchema(BillingTaskBaseSchema, BaseCreateSchema):
    pass


class BillingTaskEditSchema(BillingTaskBaseSchema, BaseEditSchema):
    pass


class DailyBillingBaseSchema(BaseModel):
    assigned_user_id: UUID | None
    # task_id: UUID | None
    sent_email: bool = False
    is_payment: bool = False
    # price: int = -10
    award: int


class DailyBillingReadSchema(DailyBillingBaseSchema, BaseReadSchema):
    pass


class DailyBillingCreateSchema(DailyBillingBaseSchema, BaseCreateSchema):
    pass


class DailyBillingEditSchema(DailyBillingBaseSchema, BaseEditSchema):
    pass


class BaseReadSchema(BaseModel):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBaseSchema(BaseModel):
    description: str


class TaskReadSchema(TaskBaseSchema, BaseReadSchema):
    assigned_user_id: UUID | None
    status: Literal["pending", "done"]
    is_billing: bool


class TaskBrockerMassageSchema(BaseModel):
    """Схема для отправки сообщений в брокер"""
    title: str = ""
    description: str = ""
    event_datetime: datetime | None = None
    version: int
    body: list[TaskReadSchema]

class UnprocessedEventsSchema(BaseModel):
    """Схема для отправки сообщений в брокер"""
    topic: str = ""
    message: str = ""
    error: str = ""

class TaskAssignSchema(BaseModel):
    assigned_user_id: UUID
    price: int = -10

class TaskAssignMassageSchema(BaseModel):
    """Схема для отправки сообщений в брокер"""
    title: str = ""
    description: str = ""
    event_datetime: datetime | None = None
    version: int = 1
    body: list[TaskAssignSchema]

