import random
import time

from tools import bootstrap


class ConfiguratorService:
    """
    Конфигуратор устройств
    """

    def configure(self, id_: int) -> None:
        """
        Сконфигурировать устройство
        :param id_: id устройства
        """

        eqp_id = bootstrap.Bootstrap.repo.retrieve(id_)

        if eqp_id is None:
            raise ValueError("Устройство не было найдено")

        # эмулируем возможность появления ошибки при конфигурации
        rand_int = random.randint(1, 4)

        if rand_int == 4:
            raise RuntimeError("Произошла ошибка при конфигурации")

        time.sleep(60)
