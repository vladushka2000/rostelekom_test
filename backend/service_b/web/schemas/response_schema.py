from http import HTTPStatus

from pydantic import Field

from interfaces import base_model


class ResponseSchema(base_model.BaseModel):
    """
    Ответ webAPI
    """

    status: HTTPStatus = Field(description="Статус ответа")
    message: str = Field(description="Сообщение")
