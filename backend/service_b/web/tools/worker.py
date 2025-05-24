import asyncio
import logging

from tools import bootstrap


logger = logging.getLogger(__name__)


async def listen_messages():
    try:
        await bootstrap.bootstrap.consumer.connect()
        await bootstrap.bootstrap.repo.connect()

        while True:
            await bootstrap.bootstrap.service.listen_for_result()
    except Exception as e:
        logger.error(e)
    finally:
        await bootstrap.bootstrap.consumer.disconnect()
        await bootstrap.bootstrap.repo.disconnect()


def listen_messages_sync_wrapper():
    asyncio.run(listen_messages())
