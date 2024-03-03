import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import TEXT, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass

text = Annotated[str, mapped_column(TEXT)]


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass


class TaskBoard(Base):
    pass
    __tablename__ = "task_board"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=func.uuid_generate_v4(), init=False
    )
    assigned_user_id: Mapped[uuid.UUID | None] = mapped_column(default=None, init=False)
    description: Mapped[text] = mapped_column(default="")
    status: Mapped[text] = mapped_column(default="")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(), init=False
    )
