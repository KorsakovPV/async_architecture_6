import uuid
from typing import Literal

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    role: Literal["user", "manager", "bookkeeper"]
    pass


class UserCreate(schemas.BaseUserCreate):
    role: Literal["user", "manager", "bookkeeper"]
    pass


class UserUpdate(schemas.BaseUserUpdate):
    role: Literal["user", "manager", "bookkeeper"]
    pass
