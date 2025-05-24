import aio_pika

from config import rabbitmq_config
from dto import broker_message_dto
from interfaces import i_message_broker

config = rabbitmq_config.rabbitmq_config


class RMQProducer(i_message_broker.IProducer):
    """
    Producer RabbitMQ
    """

    def __init__(
        self,
        model_type: type[broker_message_dto.BrokerMessageDTO] = broker_message_dto.BrokerMessageDTO,
    ) -> None:
        """
        Инициализировать переменные
        :param model_type: тип модели для передачи данных
        """

        self._model_type = model_type
        self._dsn = str(config.rabbit_mq_dsn)
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None

    async def produce(
        self, exchange_name: str, routing_key: str, message: broker_message_dto.BrokerMessageDTO
    ) -> None:
        """
        Отправить сообщение в обменник
        :param exchange_name: название обменника
        :param routing_key: ключ маршрутизации
        :param message: сообщение
        """

        if not self._connection:
            raise ValueError("Соединение с RabbitMQ не инициализировано")

        if not isinstance(message, self._model_type):
            raise ValueError("Несоответствие типа сообщения; сообщение не отправлено")

        channel = await self._connection.channel()

        message = aio_pika.Message(message.model_dump_json(by_alias=True).encode("utf-8"))
        exchange = await channel.get_exchange(exchange_name)

        await exchange.publish(message, routing_key)
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
