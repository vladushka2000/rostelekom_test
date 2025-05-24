from broker import rmq_consumer, rmq_producer
from integration import http_client
from services import configurator_service
from storage import pg_client


class Bootstrap:
    """
    DI-контейнер на минималках
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self.consumer = rmq_consumer.RMQConsumer()
        self.producer = rmq_producer.RMQProducer()
        self.service = configurator_service.ConfiguratorService()
        self.repo = pg_client.PGClient()
        self.http_client = http_client.HTTPClient()

bootstrap = Bootstrap()
