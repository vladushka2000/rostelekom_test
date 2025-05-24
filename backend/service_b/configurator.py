import asyncio
import datetime
import logging
import uuid
from multiprocessing import Pool
import sys
from http import HTTPStatus

from config import rabbitmq_config
from dto import broker_message_dto, configuration_result_dto, http_dto
from tools import bootstrap, enums

logger = logging.getLogger(__name__)
config = rabbitmq_config.rabbitmq_config


async def configure() -> None:
    """
    Запустить скрипт конфигурации
    """

    try:
        await bootstrap.bootstrap.consumer.connect()
        await bootstrap.bootstrap.producer.connect()

        while True:
            rmq_message = await bootstrap.bootstrap.consumer.retrieve(config.to_configure_queue)
            http_body = http_dto.HTTPRequestDTO(
                url=f"http://localhost:7777/api/v1/equipment/cpe/{rmq_message.body['id']}",
                payload=rmq_message.body
            )

            response = await bootstrap.bootstrap.http_client.create(http_body)

            if response.status == HTTPStatus.OK:
                status = enums.TaskStatusEnum.SUCCESS.id_
            else:
                status = enums.TaskStatusEnum.ERROR.id_

            result_rmq_message = broker_message_dto.BrokerMessageDTO(
                id=uuid.uuid4(),
                body=dict(
                    configuration_result_dto.ConfigurationResultDTO(
                        id=rmq_message.id,
                        eq_id=rmq_message.body["id"],
                        status=status
                    )
                ),
                date=datetime.datetime.now()
            )

            await bootstrap.bootstrap.producer.produce(
                config.exchange, config.configured_key, result_rmq_message
            )
    except KeyboardInterrupt:
        await bootstrap.bootstrap.consumer.disconnect()
        await bootstrap.bootstrap.producer.disconnect()
    except Exception as e:
        logger.error(e)


def sync_wrapper() -> None:
    """
    Синхронная обертка над воркером
    """

    asyncio.run(configure())


if __name__ == "__main__":
    workers_num = 4

    with Pool(processes=workers_num) as pool:
        try:
            results = [pool.apply_async(sync_wrapper) for _ in range(workers_num)]

            for result in results:
                result.get()

        except KeyboardInterrupt:
            pool.terminate()
        finally:
            pool.close()
            pool.join()

            sys.exit(0)
