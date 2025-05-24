from fastapi import FastAPI

from config import app_config
from web.entrypoints import equipment, index

app_config = app_config.app_config


def register_routers(app: FastAPI) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    """

    app.include_router(equipment.router, prefix=f"/api/{app_config.app_version}")
    app.include_router(index.router, prefix=f"/api/{app_config.app_version}")
