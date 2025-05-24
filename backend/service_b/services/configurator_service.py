import datetime
import logging
import uuid

from config import rabbitmq_config
from dto import broker_message_dto, configuration_result_dto, equipment_dto
from storage import configuration_model
from tools import bootstrap, enums, exceptions

config = rabbitmq_config.rabbitmq_config
logger = logging.getLogger(__name__)


class ConfiguratorService:
    """
    Конфигуратор устройств
    """

    async def configure(self, equipment_data: equipment_dto.EquipmentDTO) -> None:
        """
        Сконфигурировать устройство
        :param equipment_data: данные об устрйостве
        """

        task_id = uuid.uuid4()
        message = broker_message_dto.BrokerMessageDTO(
            id=task_id,
            body=dict(equipment_data),
            date=datetime.datetime.now()
        )

        await bootstrap.bootstrap.repo.create(
            "configuration",
            dict(
                configuration_model.ConfigurationModel(
                    id=task_id,
                    eq_id=equipment_data.id,
                    status=enums.TaskStatusEnum.PENDING.id_
                )
            )
        )
        await bootstrap.bootstrap.producer.produce(
            config.exchange, config.to_configure_key, message
        )

    async def get_result(self, eq_id: str, task_id: uuid.UUID) -> enums.TaskStatusEnum:
        """
        Получить информацию о выполнении задачи на конфигурацию
        :param eq_id: идентификатор устройства
        :param task_id: идентификатор задачи
        :return: статус выполнения задачи
        """

        try:
            db_data = await bootstrap.bootstrap.repo.retrieve("configuration", task_id)

            if not db_data:
                raise ValueError("Запись не найдена")
        except Exception:
            raise exceptions.TaskNotFoundError()

        if db_data["eq_id"] != eq_id:
            raise exceptions.EquipmentNotFoundError()

        status = enums.TaskStatusEnum.get_by_id(db_data["status"])

        return status

    async def listen_for_result(self) -> None:
        """
        Слушать очередь результатов конфигурации
        """

        try:
            while True:
                message = await bootstrap.bootstrap.consumer.retrieve(config.configured_queue)
                configration_info = configuration_result_dto.ConfigurationResultDTO(
                    id=message.body["id"],
                    eq_id=message.body["eq_id"],
                    status=message.body["status"]
                )

                status = enums.TaskStatusEnum.get_by_id(configration_info.status).name_
                new_status = enums.TaskStatusEnum.SUCCESS.id_

                if status == enums.TaskStatusEnum.ERROR:
                    new_status = enums.TaskStatusEnum.ERROR.id_

                await bootstrap.bootstrap.repo.update(
                    "configuration",
                    configration_info.id,
                    dict(
                        configuration_model.ConfigurationModel(
                            id=configration_info.id,
                            eq_id=configration_info.eq_id,
                            status=new_status
                        )
                    )
                )
        except Exception as e:
            logger.error(e)
