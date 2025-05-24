import uuid

from pydantic import Field

from interfaces import base_model


class ConfigurationModel(base_model.BaseModel, base_model.ConfigMixin):
    """
    БД модель для таблицы configuration
    """

    id: uuid.UUID = Field(description="Идентификатор сообщения")
    eq_id: str = Field(description="Идентификатор устройства")
    status: uuid = Field(description="Статус задачи")
