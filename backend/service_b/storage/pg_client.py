import uuid
from typing import Iterable

import asyncpg

from config import pg_config
from interfaces import i_client

config = pg_config.pg_config


class PGClient(i_client.IClient):
    """
    Клиент для работы с Postgres
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        """
        Соединиться с БД
        """

        self._pool = await asyncpg.create_pool(
            dsn=str(config.pg_dsn),
            min_size=1,
            max_size=10,
            command_timeout=60
        )

    async def disconnect(self):
        """
        Отключиться от БД
        """

        if not self._pool:
            raise ValueError("Соединение не инициализировано")

        await self._pool.close()

    async def create(self, table: str, data: dict) -> asyncpg.Record:
        """
        Создать запись в указанной таблице
        """

        columns = ", ".join(data.keys())
        placeholders = ", ".join(f"${i + 1}" for i in range(len(data)))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"

        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query, *data.values())

    async def retrieve(self, table: str, id_: uuid.UUID) -> asyncpg.Record | None:
        """
        Получить запись по ID
        """

        query = f"SELECT * FROM {table} WHERE id = $1"
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query, id_)

    async def list(self, *args, **kwargs) -> Iterable:
        """
        Получить список записей с пагинацией
        """

        return super().list(*args, **kwargs)

    async def update(self, table: str, id_: uuid.UUID, data: dict) -> asyncpg.Record:
        """
        Обновить запись
        """

        set_clause = ", ".join(f"{key} = ${i + 2}" for i, key in enumerate(data.keys()))
        query = f"UPDATE {table} SET {set_clause} WHERE id = $1 RETURNING *"

        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query, id_, *data.values())

    async def delete(self, *args, **kwargs) -> None:
        """
        Удалить запись
        """

        super().delete(*args, **kwargs)

    async def _execute(self, query: str, *args) -> str:
        """
        Выполненить произвольный SQL-запрос
        """

        async with self._pool.acquire() as conn:
            return await conn.execute(query, *args)
