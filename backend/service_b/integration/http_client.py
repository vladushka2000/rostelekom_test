from typing import Iterable

import httpx

from dto import http_dto
from interfaces import i_client


class HTTPClient(i_client.IClient):
    """
    Клиент для HTTP-запросов
    """

    def __init__(self) -> None:
        """
        Инициализировать переменны
        """

        self._client = httpx.AsyncClient(timeout=None)

    def connect(self) -> None:
        """
        Установить соединение
        """

        pass

    async def disconnect(self) -> None:
        """
        Разорвать соединение
        """

        await self._client.aclose()

    async def create(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать POST-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        response = await self._client.post(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params,
            json=request_params.payload,
            data=request_params.form_data,
        )

        return http_dto.HTTPResponseDTO(
            status=response.status_code,
            headers=response.headers,
            payload=response.json()
        )

    async def retrieve(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать GET-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        response = await self._client.get(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params
        )

        return http_dto.HTTPResponseDTO(
            status=response.status_code,
            headers=response.headers,
            payload=response.json()
        )

    async def list(self, *args, **kwargs) -> Iterable[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    async def update(self, *args, **kwargs) -> httpx.Response:
        """
        Сделать PATCH-запрос
        """

        return super().update(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> httpx.Response:
        """
        Сделать DELETE-запрос
        """

        return super().delete(*args, **kwargs)
