import uvicorn

from config import app_config
from web.tools import initializer

config = app_config.app_config
app = initializer.app


if __name__ == "__main__":
    uvicorn.run(app, host=config.app_host, port=config.app_port)
