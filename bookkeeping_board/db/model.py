import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import TEXT, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

text = Annotated[str, mapped_column(TEXT)]


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass


class BookkeepingBoard(Base):
    pass
    __tablename__ = "bookkeeping_board"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=func.uuid_generate_v4(), init=False
    )
    assigned_user_id: Mapped[uuid.UUID | None] = mapped_column(default=None, init=False)
    task_id: Mapped[uuid.UUID | None] = mapped_column(default=None, init=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(), init=False
    )
    used_in_billing: Mapped[bool] = mapped_column(default=False, init=False)
    price: Mapped[int] = mapped_column(default=-10, init=False)
    award: Mapped[int] = mapped_column(default=100, init=False)


class DailyBilling(Base):
    pass
    __tablename__ = "daily_billing"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=func.uuid_generate_v4(), init=False
    )
    assigned_user_id: Mapped[uuid.UUID | None] = mapped_column(default=None, init=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(), init=False
    )
    sent_email: Mapped[bool] = mapped_column(default=False, init=False)
    is_payment: Mapped[bool] = mapped_column(default=False, init=False)
    award: Mapped[int] = mapped_column(init=False)


class UnprocessedEvents(Base):
    pass
    __tablename__ = "unprocessed_events"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=func.uuid_generate_v4(), init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(), init=False
    )
    topic: Mapped[text] = mapped_column(init=False)
    message: Mapped[text] = mapped_column(init=False)
    error: Mapped[text] = mapped_column(init=False)
