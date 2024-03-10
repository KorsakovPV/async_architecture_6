from aiokafka import AIOKafkaProducer
import asyncio

from core.config import app_settings


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers=app_settings.KAFKA_BOOTSTRAP_SERVERS)
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("my_topic", b"Super message")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

if __name__ == '__main__':
    asyncio.run(send_one())
