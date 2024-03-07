import uuid

from fastapi_users import FastAPIUsers

from auth_backend.auth_jwt_bearer_backend import auth_backend
from auth_backend.user_manager import get_user_manager
from db.base import get_async_session
from db.model import User
from schemas.auth_schemas import UserCreate, UserRead, UserUpdate


from fastapi import APIRouter, status, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter(prefix="")

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# роутер для аутентификации и получения access token
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Роутер для регистрации
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Роутер для сброса пароля
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

# Роутер для получения пользователя по id, редактирования, удаления
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@auth_router.get(
    "/get_users", status_code=status.HTTP_200_OK, response_model=list[UserRead]
)
async def get_users(session: AsyncSession = Depends(get_async_session)):
    statement = select(User).where(
        User.role.in_(
            [
                "user",
            ]
        )
    )
    results = await session.execute(statement=statement)
    users = results.scalars().all()
    return users
