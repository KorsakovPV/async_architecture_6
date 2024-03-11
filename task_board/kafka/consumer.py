from aiokafka import AIOKafkaConsumer
import asyncio

from core.config import app_settings


async def consume():
    consumer = AIOKafkaConsumer(
        "my_topic",
        "my_other_topic",
        bootstrap_servers=app_settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="my-group",
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
