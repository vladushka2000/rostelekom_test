import logging
import re
import uuid
from http import HTTPStatus

from fastapi import APIRouter

from config import app_config
from dto import equipment_dto
from tools import bootstrap, enums, exceptions
from web.schemas import equipment_schema, response_schema

router = APIRouter(prefix="/equipment", tags=["equipment"])

logger = logging.getLogger(__name__)
app_config = app_config.app_config


def _is_id_valid(id_: str) -> bool:
    """
    Проверить id устройства на корректность
    :param id_: id устройства
    :return: True, если id валидный, иначе False
    """

    pattern = r"^[a-zA-Z0-9]{6,}$"

    if not re.fullmatch(pattern, id_):
        return False

    return True


@router.post("/cpe/{id_}")
async def configurate(
    id_: str,
    data: equipment_schema.EquipmentSchema
) -> response_schema.ResponseSchema:
    """
    Сконфигурировать устройства
    :param id_: идентификатор устройства
    :param data: данные об устройстве
    :return: статус отправки задачи на конфигурацию
    """

    if not _is_id_valid(id_):
        return response_schema.ResponseSchema(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Incorrect id"
        )

    try:
        equipment_data = equipment_dto.EquipmentDTO(
            id=id_,
            timeout_in_seconds=data.timeout_in_seconds,
            parameters=equipment_dto.ParametersDTO(
                username=data.parameters.username,
                password=data.parameters.password,
                vlan=data.parameters.vlan,
                interfaces=data.parameters.interfaces
            )
        )

        await bootstrap.bootstrap.service.configure(equipment_data)

        return response_schema.ResponseSchema(status=HTTPStatus.OK, message="sent to configuration")
    except Exception as e:
        logger.error(e)

        return response_schema.ResponseSchema(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="send error"
        )


@router.get("/cpe/{id_}/task/{task_id}")
async def get_result(
    id_: str,
    task_id: uuid.UUID
) -> response_schema.ResponseSchema:
    """
    Сконфигурировать устройства
    :param id_: идентификатор устройства
    :param task_id: идентификатор задачи
    :return: статус задачи на конфигурацию
    """

    if not _is_id_valid(id_):
        return response_schema.ResponseSchema(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Incorrect id"
        )

    try:
        status = await bootstrap.bootstrap.service.get_result(id_, task_id)

        if status == enums.TaskStatusEnum.SUCCESS:
            return response_schema.ResponseSchema(
                status=HTTPStatus.OK,
                message="completed"
            )

        if status == enums.TaskStatusEnum.PENDING:
            return response_schema.ResponseSchema(
                status=HTTPStatus.OK,
                message="Task is still running"
            )

        if status == enums.TaskStatusEnum.ERROR:
            return response_schema.ResponseSchema(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Internal provisioning exception"
            )
    except exceptions.EquipmentNotFoundError:
        return response_schema.ResponseSchema(
            status=HTTPStatus.NOT_FOUND,
            message="The requested equipment is not found"
        )
    except exceptions.TaskNotFoundError:
        return response_schema.ResponseSchema(
            status=HTTPStatus.NOT_FOUND,
            message="The requested task is not found"
        )
    except Exception as e:
        logger.error(e)

        return response_schema.ResponseSchema(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Internal provisioning exception"
        )
