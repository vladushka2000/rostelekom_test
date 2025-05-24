import dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class AppConfig(BaseSettings):
    """
    Класс настроек для приложения
    """

    app_name: str = Field(description="Название проекта")
    app_version: str = Field(description="Версия API")

    app_host: str = Field(description="Хост сервиса")
    app_port: int = Field(description="Порт сервиса")


app_config = AppConfig()
