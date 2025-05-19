import flask

from web.entrypoints import equipment, index


def register_routes(app: flask.Flask) -> None:
    """
    Зарегистрировать эндпоинты
    :param app: приложение Flask
    """

    app.register_blueprint(equipment.router)
    app.register_blueprint(index.router)
