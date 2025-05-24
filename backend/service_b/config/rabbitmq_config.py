import dotenv
from pydantic import AmqpDsn, Field, computed_field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class RabbitMQConfig(BaseSettings):
    """
    Класс настроек для приложения
    """

    rmq_host: str = Field(description="Хост брокера")
    rmq_port: int = Field(description="Порт брокера")

    rmq_user: str = Field(description="Имя пользователя")
    rmq_password: str = Field(description="Пароль")

    exchange: str = Field(description="Название обменника сообщениями")
    to_configure_queue: str = Field(description="Название очереди на конфигурацию")
    configured_queue: str = Field(description="Название очереди отконфигурированных устройств")
    to_configure_key: str = Field(description="Ключ маршрутизации для очереди конфигурации")
    configured_key: str = Field(description="Ключ маршрутизации для очереди результатов")

    @computed_field
    @property
    def rabbit_mq_dsn(self) -> AmqpDsn:
        return AmqpDsn.build(
            host=self.rmq_host,
            port=self.rmq_port,
            username=self.rmq_user,
            password=self.rmq_password,
            scheme="amqp",
        )


rabbitmq_config = RabbitMQConfig()
