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
    assigned_user_id: UUID | None
    task_id: UUID | None
    # sent_email: bool = False
    # is_payment: bool = False
    price: int = -10
    award: int = 100


class TaskReadSchema(TaskBaseSchema, BaseReadSchema):
    pass


class TaskCreateSchema(TaskBaseSchema, BaseCreateSchema):
    pass


class TaskEditSchema(TaskBaseSchema, BaseEditSchema):
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
