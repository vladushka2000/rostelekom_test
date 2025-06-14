from fastapi import APIRouter

from config import app_config

router = APIRouter(tags=["index"])

app_config = app_config.app_config


@router.get("/")
async def index() -> str:
    return f"{app_config.app_name} - {app_config.app_version}"
