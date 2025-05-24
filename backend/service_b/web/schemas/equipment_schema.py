from pydantic import Field

from interfaces import base_model


class Parameters(base_model.BaseModel):
    """
    Параметры
    """

    username: str = Field(description="Имя пользователя")
    password: str = Field(description="Пароль")
    vlan: int | None = Field(description="vlan", default=None)
    interfaces: list[int] = Field(description="Интерфейсы")


class EquipmentSchema(base_model.BaseModel, base_model.ConfigMixin):
    """
    Схема данных для запроса на конфигурацию устройства
    """

    timeout_in_seconds: int = Field(
        description="Максимальное время ожидания ответа на запрос",
        alias="timeoutInSeconds"
    )
    parameters: Parameters = Field(description="Параметры")
