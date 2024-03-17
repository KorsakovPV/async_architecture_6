import json
import logging
from datetime import datetime
from logging.config import dictConfig
from uuid import UUID

from aiokafka import AIOKafkaProducer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import parse_obj_as

from core.config import app_settings
from core.logs import LOGGER_CONFIG
from db.base import async_session_maker
from sqlalchemy import update, and_, select

from db.model import TaskBoard
from schemas.task_schemas import TaskReadSchema, TaskBrockerMassageSchemaV1, TaskAssignSchema, TaskAssignMassageSchemaV1

dictConfig(LOGGER_CONFIG)

logger = logging.getLogger("root")

scheduler = AsyncIOScheduler()


async def push_assign_users(assigned_users):
    """
    Пушим событие таска заасайнена.
    """
    push_datetime = datetime.now()

    producer = AIOKafkaProducer(bootstrap_servers=app_settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        message_body = {
            "event_datetime": push_datetime,
            "version": 1,
            "body": [
                TaskAssignSchema(
                    # id пользователя на кого заасайнена
                    assigned_user_id=UUID(assigned_user_id),
                    # Сколько с пользователя нужно будет снять при биллинге
                    price=price
                )
                for assigned_user_id, price in assigned_users
            ],
        }

        body_json = json.dumps(parse_obj_as(TaskAssignMassageSchemaV1, message_body).json())
        await producer.send_and_wait("tasks.assigned", body_json.encode())
    finally:
        logger.info(f"{len(assigned_users)} Task for assign successful pushed")

        await producer.stop()

async def push_done_tasks():
    """
    По крону пушим завершенные таски. Устанавливаем is_billing в True. Повторно таску в биллинг не передать.
    """
    push_datetime = datetime.now()

    async with async_session_maker() as session:
        statement = update(TaskBoard).where(
        # statement = select(TaskBoard).where(
            and_(
                TaskBoard.status.in_(
                    [
                        "done",
                    ]
                )
            ),
            TaskBoard.is_billing.in_(
                [
                    False,
                ]
            ),
            TaskBoard.assigned_user_id.is_not(None)
            ).values({'is_billing': True}).returning(TaskBoard)
        # )
        billing_tasks = (await session.execute(statement)).scalars().all()

        await session.commit()

        logger.info(f"Task for billing {billing_tasks}")

    producer = AIOKafkaProducer(bootstrap_servers=app_settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        message_body = {
            "event_datetime": push_datetime,
            "version": 1,
            "body": [
                parse_obj_as(TaskReadSchema, billing_task)
                for billing_task in billing_tasks
            ],
        }

        body_json = json.dumps(parse_obj_as(TaskBrockerMassageSchemaV1, message_body).json())
        await producer.send_and_wait("tasks.closed", body_json.encode())
    finally:
        logger.info(f"{len(billing_tasks)} Task for billing successful pushed")

        await producer.stop()


async def main():
    logger.info("Start push_done_jobs")
    logger.info(f"Runs every days in 00:00")

    scheduler.add_job(
        push_done_tasks,
        trigger='cron', hour=0, minute=0,
        # trigger="interval", seconds=6,
    )

    scheduler.start()
