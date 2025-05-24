import abc


class IProducer(abc.ABC):
    """
    Интерфейс для продюсера
    """

    @abc.abstractmethod
    async def produce(self, *args, **kwargs):
        """
        Отправить сообщение брокеру
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def connect(self, *args, **kwargs) -> any:
        """
        Установить соединение с брокером
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def disconnect(self, *args, **kwargs) -> any:
        """
        Разорвать соединение с брокером
        """

        raise NotImplementedError


class IConsumer(abc.ABC):
    """
    Интерфейс для асинхронного консюмера
    """

    @abc.abstractmethod
    async def retrieve(self, *args, **kwargs):
        """
        Прочитать одно сообщение из брокера
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def connect(self, *args, **kwargs) -> any:
        """
        Установить соединение с брокером
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def disconnect(self, *args, **kwargs) -> any:
        """
        Разорвать соединение с брокером
        """

        raise NotImplementedError