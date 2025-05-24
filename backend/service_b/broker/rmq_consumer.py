import asyncio
import json

import aio_pika

from config import rabbitmq_config
from dto import broker_message_dto
from interfaces import i_message_broker

config = rabbitmq_config.rabbitmq_config


class RMQConsumer(i_message_broker.IConsumer):
    """
    Consumer RabbitMQ
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self._queue: asyncio.Queue[aio_pika.abc.AbstractIncomingMessage] = asyncio.Queue()
        self._dsn = str(config.rabbit_mq_dsn)
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None

    async def retrieve(
        self, queue_name: str, prefetch_count: int = 1
    ) -> broker_message_dto.BrokerMessageDTO:
        """
        Прочитать сообщение из очереди
        :param queue_name: название очереди
        :param prefetch_count: количество сообщений, посылаемое брокером, за раз
        :return: прочитанное сообщение
        """

        if not self._connection:
            raise ValueError("Соединение с RabbitMQ не инициализировано")

        channel = await self._connection.channel()

        await channel.set_qos(prefetch_count=prefetch_count)

        queue = await channel.get_queue(queue_name)
        await queue.consume(self._queue.put)

        message = await self._queue.get()
        await message.ack()

        try:
            decoded = json.loads(message.body)
            return broker_message_dto.BrokerMessageDTO(
                id=decoded["id"], body=decoded["body"], date=decoded["date"]
            )
        except json.JSONDecodeError:
            raise
        finally:
            await channel.close()

    async def connect(self) -> None:
        """
        Установить соединение с брокером
        """

        self._connection = await aio_pika.connect_robust(self._dsn)

    async def disconnect(self) -> None:
        """
        Разорвать соединение с брокером
        """

        await self._connection.close()
