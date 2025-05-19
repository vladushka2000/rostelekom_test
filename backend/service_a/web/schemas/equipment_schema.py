from pydantic import Field

from interfaces import base_schema


class Parameters(base_schema.BaseWebSchema):
    """
    Параметры
    """

    username: str = Field(description="Имя пользователя")
    password: str = Field(description="Пароль")
    vlan: int | None = Field(description="vlan", default=None)
    interfaces: list[int] = Field(description="Интерфейсы")


class EquipmentSchema(base_schema.BaseWebSchema):
    """
    Схема данных для запроса на конфигурацию устройства
    """

    timeoutInSeconds: int = Field(description="Максимальное время ожидания ответа на запрос")
    parameters: Parameters = Field(description="Параметры")
