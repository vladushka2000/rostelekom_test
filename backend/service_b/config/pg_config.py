import dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class PostgresConfig(BaseSettings):
    """
    Класс настроек для БД
    """

    user: str = Field(alias="POSTGRES_USER", description="Имя пользователя БД")
    password: str = Field(alias="POSTGRES_PASSWORD", description="Пароль пользователя БД")
    host: str = Field(alias="POSTGRES_HOST", description="Хост подключения к БД")
    port: int = Field(alias="POSTGRES_PORT", description="Порт подключения к БД")
    db_name: str = Field(alias="POSTGRES_DB", description="Имя БД")
    connection_pool_size: int = Field(alias="POOL_SIZE", description="Размер пула соединений")

    @property
    def pg_dsn(self) -> PostgresDsn:
        """
        Получение url для подключения к Postgres
        :return: dsn
        """

        return PostgresDsn.build(
            scheme="postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db_name,
        )


pg_config = PostgresConfig()
