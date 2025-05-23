from typing import Iterable

from interfaces import i_repository


# Тестовая in-memory БД
_EQP_DB = {
    "aaa001": ...,
    "aaa002": ...,
    "aaa003": ...,
    "aaa004": ...,
    "aaa005": ...
}


class EqpRepository(i_repository.IRepository):
    """
    Репозиторий для работы с БД оборудования
    """

    def create(self, *args, **kwargs) -> any:
        """
        Создать запись
        """

        return super().create(*args, **kwargs)

    def retrieve(self, id_: str) -> str | None:
        """
        Получить id устройства
        :param id_: серийный номер устройства
        return: id устройства или None в случае отсутствия
        """

        return _EQP_DB.get(id_)

    def list(self, *args, **kwargs) -> Iterable[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    def update(self, *args, **kwargs) -> any:
        """
        Обновить запись
        """

        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs) -> any:
        """
        Удалить запись
        """

        return super().delete(*args, **kwargs)
