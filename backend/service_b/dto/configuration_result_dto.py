import uuid

from pydantic import Field

from interfaces import base_model


class ConfigurationResultDTO(base_model.BaseModel, base_model.ConfigMixin):
    """
    Результат конфигурации
    """

    id: uuid.UUID = Field(description="Идентификатор сообщения")
    eq_id: str = Field(description="Идентификатор устройства")
    status: uuid.UUID = Field(description="Статус задачи")