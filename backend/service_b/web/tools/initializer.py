from multiprocessing import Process

import fastapi

from config import app_config
from tools import bootstrap
from web.tools import middlewares, router_registrator, worker

app_config = app_config.app_config


async def lifespan(_)-> None:  # noqa
    process = Process(target=worker.listen_messages_sync_wrapper, daemon=True)
    process.start()

    await bootstrap.bootstrap.consumer.connect()
    await bootstrap.bootstrap.producer.connect()
    await bootstrap.bootstrap.repo.connect()

    yield

    await bootstrap.bootstrap.consumer.disconnect()
    await bootstrap.bootstrap.producer.disconnect()
    await bootstrap.bootstrap.repo.disconnect()

    process.terminate()


def initiliaze_app() -> fastapi.FastAPI:
    """
    Инициализировать приложение FastAPI
    """

    fastapi_app = fastapi.FastAPI(
        title=app_config.app_name,
        version=app_config.app_version,
        default_response_class=fastapi.responses.JSONResponse,
        lifespan=lifespan
    )

    return fastapi_app


app = initiliaze_app()
app.add_middleware(middlewares.SetResponseStatusMiddleware)
router_registrator.register_routers(app)
