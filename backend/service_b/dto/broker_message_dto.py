import datetime
import uuid

from pydantic import Field

from interfaces import base_model


class BrokerMessageDTO(base_model.BaseModel, base_model.ConfigMixin):
    """
    DTO, содержащий сообщение для брокера
    """

    id: uuid.UUID = Field(
        description="Идентификатор сообщения", default_factory=lambda: uuid.uuid4()
    )
    body: dict = Field(description="Тело сообщения")
    date: datetime.datetime = Field(
        description="Дата создания сообщения",
        default_factory=lambda: datetime.datetime.now(),
    )
