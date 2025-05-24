from pydantic import Field

from interfaces import base_model


class ParametersDTO(base_model.BaseModel):
    """
    Параметры
    """

    username: str = Field(description="Имя пользователя")
    password: str = Field(description="Пароль")
    vlan: int | None = Field(description="vlan", default=None)
    interfaces: list[int] = Field(description="Интерфейсы")


class EquipmentDTO(base_model.BaseModel, base_model.ConfigMixin):
    """
    Данные на конфигурацию устройства
    """

    id: str = Field(description="Идентификатор устройства")
    timeout_in_seconds: int = Field(
        description="Максимальное время ожидания ответа на запрос",
        alias="timeoutInSeconds"
    )
    parameters: ParametersDTO = Field(description="Параметры")
