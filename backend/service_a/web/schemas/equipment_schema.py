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


class EquipmentSchema(base_schema.BaseWebSchema, base_schema.ConfigMixin):
    """
    Схема данных для запроса на конфигурацию устройства
    """

    timeout_in_seconds: int = Field(
        description="Максимальное время ожидания ответа на запрос",
        alias="timeoutInSeconds"
    )
    parameters: Parameters = Field(description="Параметры")
