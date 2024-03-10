import asyncio
import json
import logging
import time
from logging.config import dictConfig

from aiokafka import AIOKafkaProducer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import parse_obj_as

from core.config import app_settings
from core.logs import LOGGER_CONFIG
from db.base import async_session_maker
from sqlalchemy import delete, insert, select, update, and_, or_

from db.model import TaskBoard
from schemas.task_schemas import TaskReadSchema

dictConfig(LOGGER_CONFIG)

logger = logging.getLogger('root')

scheduler = AsyncIOScheduler()



async def push_done_tasks():
    print('push_done_jobs')

    #TODO Пометить таски как переданные в биллинг
    async with (async_session_maker() as session):
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

        # session.commit()

    #TODO Передать таски в биллинг


    producer = AIOKafkaProducer(bootstrap_servers=app_settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        for billing_task in billing_tasks:
            task_json = parse_obj_as(TaskReadSchema, billing_task).json()
            body_json = json.dumps(
                {
                    'version': 1,
                    'body': task_json
                }
            )
            await producer.send_and_wait("topic.task_to_billing", body_json.encode())
    finally:
        await producer.stop()


if __name__ == '__main__':
    logger.info('Start push_done_jobs')
    logger.info(f'Runs every days in 00:00')

    scheduler.add_job(
        push_done_tasks,
        # trigger='cron',
        # hour=0,
        # minute=0,
        trigger='interval',
        seconds=10
    )

    scheduler.start()

    asyncio.get_event_loop().run_forever()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        scheduler.shutdown()
