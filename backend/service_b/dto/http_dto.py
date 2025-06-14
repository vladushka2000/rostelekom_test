from pydantic import Field

from interfaces import base_model


class HTTPRequestDTO(base_model.BaseModel):
    """
    DTO, содержащий информацию для HTTP-запроса
    """

    url: str = Field(description="URL запроса")
    headers: dict | None = Field(description="Заголовки", default=None)
    query_params: dict | None = Field(description="Параметры запроса", default=None)
    payload: dict | list | None = Field(description="Body запроса", default=None)
    form_data: dict | None = Field(description="Данные из html-формы", default=None)


class HTTPResponseDTO(base_model.BaseModel):
    """
    DTO, содержащий информацию ответа HTTP-запроса
    """

    status: int = Field(description="Статус ответа")
    headers: dict | None = Field(description="Заголовки", default=None)
    payload: dict | list[dict] | None = Field(description="Body ответа", default=None)
