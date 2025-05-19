from http import HTTPStatus

import flask

from config import app_config
from tools import bootstrap
from web.schemas import body_validator
from web.schemas import equipment_schema

config = app_config.app_config

router = flask.Blueprint("equipment", __name__, url_prefix=f"/api/{config.app_version}/equipment")


@router.route("/cpe/<int:id_>", methods=("POST",))
@body_validator.validate_request(equipment_schema.EquipmentSchema)
def configure(id_: int, data: equipment_schema.EquipmentSchema):
    """
    Конфигурировать устройство
    :param id_: id устройства
    :param data: данные устройства
    :return: информация о сервисе
    """

    bootstrap.Bootstrap.service.configure(id_)

    return flask.jsonify(
        {
            "code": HTTPStatus.OK,
            "message": "success"
        }
    ), HTTPStatus.OK
