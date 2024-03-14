import json
from collections import defaultdict

from fastapi import APIRouter
from sqlalchemy import insert, select

from core.config import loop, app_settings
from core.logs import logger
from db.base import async_session_maker
from db.model import BookkeepingBoard, DailyBilling, UnprocessedEvents

from aiokafka import AIOKafkaConsumer

from schemas.bookkeeping_schemas import BillingTaskCreateSchema, DailyBillingCreateSchema, TaskBrockerMassageSchema, \
    UnprocessedEventsSchema
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = APIRouter()

scheduler = AsyncIOScheduler()


class ErrorUnprocessedVersion(Exception):
    pass


async def message_process_task_to_billing_v1(messages):
    create_tasks = []
    async with async_session_maker() as session:
        for message in messages:
            task = BillingTaskCreateSchema(
                assigned_user_id=message.assigned_user_id,
                task_id=message.id,
            )

            results = await session.execute(
                insert(BookkeepingBoard)
                .values(**task.dict(exclude_unset=True))
                .returning(BookkeepingBoard)
                .options()
            )
            r = results.scalar_one()
            create_tasks.append(r)

        logger.info(f"Created {len(create_tasks)} records in BookkeepingBoard.")
        accounts_bulling = defaultdict(int)

        for create_task in create_tasks:
            accounts_bulling[create_task.assigned_user_id] += (
                    create_task.award + create_task.price
            )

        for account_id, account_value in accounts_bulling.items():
            daily_billing = DailyBillingCreateSchema(
                assigned_user_id=account_id, award=account_value
            )

            results = await session.execute(
                insert(DailyBilling)
                .values(**daily_billing.dict(exclude_unset=True))
                .returning(DailyBilling)
                .options()
            )
            results.scalar_one()

        logger.info(f"Created {len(accounts_bulling)} records in DailyBilling.")

        await session.commit()

    # TODO Отправить письмо

    # TODO Выполнить начисление


async def message_process_task_to_billing(message):
    message_dict = json.loads(json.loads(message.value))
    message_obj = TaskBrockerMassageSchema(**message_dict)
    if message_obj.version == 1:
        await message_process_task_to_billing_v1(message_obj.body)

    else:
        raise ErrorUnprocessedVersion(f"Wrong version: {message_obj.version} for {message=}")


async def message_process(message):
    if message.topic == "topic.task_to_billing":
        await message_process_task_to_billing(message)


async def consume_message():
    logger.info("Starting consuming message")
    consumer = AIOKafkaConsumer(
        "topic.task_to_billing",
        loop=loop,
        bootstrap_servers=app_settings.KAFKA_BOOTSTRAP_SERVERS,
    )
    await consumer.start()
    try:
        async for message in consumer:
            logger.info(f"Consumer msg: {message}")
            try:
                await message_process(message=message)
            except Exception as error:
                await save_error_message(error, message)

            finally:
                continue
    finally:
        await consumer.stop()


async def save_error_message(error, message):
    error_message = f"message_process is filed with {error=}"
    logger.error(error_message)
    async with async_session_maker() as session:
        task = UnprocessedEventsSchema(
            topic=message.topic,
            message=message.value,
            error=error_message,
        )

        results = await session.execute(
            insert(UnprocessedEvents)
            .values(**task.dict(exclude_unset=True))
            .returning(UnprocessedEvents)
            .options()
        )
        error_message = results.scalar_one()

        await session.commit()

        logger.info(f"error message wrote in DB {error_message=}")
