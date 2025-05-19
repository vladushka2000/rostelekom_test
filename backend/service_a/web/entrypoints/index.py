from flask import Blueprint

from config import app_config

config = app_config.app_config

router = Blueprint("index", __name__, url_prefix=f"/api/{config.app_version}")


@router.route("/")
def index() -> str:
    """
    Получить основную информацию о сервисе
    :return: информация о сервисе
    """

    return f"{config.app_name} - {config.app_version}"
