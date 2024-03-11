import json
from collections import defaultdict
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy import insert

from core.config import loop, app_settings
from core.logs import logger
from db.base import async_session_maker
from db.model import BookkeepingBoard, DailyBilling

from aiokafka import AIOKafkaConsumer

from schemas.bookkeeping_schemas import TaskCreateSchema, DailyBillingCreateSchema
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = APIRouter()

scheduler = AsyncIOScheduler()

router.post("/create_message")


async def message_process_task_to_billing_v1(messages):
    create_tasks = []
    async with async_session_maker() as session:
        for message in messages:
            message_dict = json.loads(message)

            task = TaskCreateSchema(
                assigned_user_id=UUID(message_dict.get("assigned_user_id")),
                task_id=UUID(message_dict.get("id")),
            )

            results = await session.execute(
                insert(BookkeepingBoard)
                .values(**task.dict(exclude_unset=True))
                .returning(BookkeepingBoard)
                .options()
            )
            r = results.scalar_one()
            create_tasks.append(r)

        logger.info(f"Created {len(r)} records in BookkeepingBoard.")
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

        logger.info(f"Created {len(accounts_bulling)} records in BookkeepingBoard.")

        await session.commit()

    # TODO Отправить письмо

    # TODO Выполнить начисление


async def message_process_task_to_billing(message_dict):
    if (
        message_dict.get("version")
        and message_dict.get("body")
        and message_dict.get("version") == 1
    ):
        await message_process_task_to_billing_v1(message_dict.get("body"))


async def message_process(message):
    message_dict = json.loads(message.value)

    if message.topic == "topic.task_to_billing":
        await message_process_task_to_billing(message_dict)


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
            await message_process(message=message)
    finally:
        await consumer.stop()
